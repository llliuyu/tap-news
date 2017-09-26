import logging
import json
import operator
import os
import pickle
import random
import redis
import sys

from bson.json_util import dumps
from datetime import datetime

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
import news_recommendation_service_client

from cloudAMQP_client import CloudAMQPClient

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

NEWS_TABLE_NAME = 'news-test'
CLICK_LOGS_TABLE_NAME = 'click_logs'
PREFERENCE_MODEL_TABLE_NAME = 'user_preference_model'

NEWS_LIMIT = 100
NEWS_LIST_BATCH_SIZE = 10
USER_NEWS_TIME_OUT_IN_SECONDS = 60

LOG_CLICKS_TASK_QUEUE_URL = 'amqp://zylpcqxg:s5PL0DqsrTDwjtFym_nVZSW8-CBzVjE0@donkey.rmq.cloudamqp.com/zylpcqxg'
LOG_CLICKS_TASK_QUEUE_NAME = 'tap-news-log-clicks-task-queue'

redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT, db=0)
cloudAMQP_client = CloudAMQPClient(LOG_CLICKS_TASK_QUEUE_URL, LOG_CLICKS_TASK_QUEUE_NAME)


def getNewsSummariesForUser(user_id, page_num, user_ip):
    page_num = int(page_num)
    begin_index = (page_num - 1) * NEWS_LIST_BATCH_SIZE
    end_index = page_num * NEWS_LIST_BATCH_SIZE

# The final list of news to be returned.
    sliced_news = []

    # Get preference for the user
    preference = news_recommendation_service_client.getPreferenceForUser(user_id) 
   
    topPreference = None

    if preference is not None and len(preference) > 0:
        topPreference = preference[0]

    print topPreference

    if redis_client.get(user_id) is not None:
        # news_digests = pickle.loads(redis_client.get(user_id))
        news_class_digests = pickle.loads(redis_client.get(user_id))

        news_digests = sortNews(news_class_digests, preference)
        # If begin_index is out of range, this will return empty list;
        # If end_index is out of range (begin_index is within the range), this
        # will return all remaining news ids.

        sliced_news_digests = news_digests[begin_index:end_index]
        
        print 'redis_client.get(user_id) is not None'
        
        db = mongodb_client.get_db()
        sliced_news = list(db[NEWS_TABLE_NAME].find({'digest': {'$in': sliced_news_digests}}))
    else:
        db = mongodb_client.get_db()
        total_news = list(db[NEWS_TABLE_NAME].find().sort([('publishedAt', -1)]).limit(NEWS_LIMIT))

        # total_news_digests = map(lambda x: x['digest'], total_news)
        total_news_class_digests = map(lambda x: [x.get('class'),x['digest']], total_news)
        print 'redis_client.get(user_id) is None'
        # redis_client.set(user_id, pickle.dumps(total_news_digests))
        redis_client.set(user_id, pickle.dumps(total_news_class_digests))
        redis_client.expire(user_id, USER_NEWS_TIME_OUT_IN_SECONDS)

        sliced_news = total_news[begin_index:end_index]

    

    for news in sliced_news:
        # Remove text field to save bandwidth.
        del news['text']
        if news.get('class') == topPreference:
            news['reason'] = 'Recommend'
        if news['publishedAt'].date() == datetime.today().date():
            news['time'] = 'today'

    return json.loads(dumps(sliced_news))

def getPreferenceForUser(user_id):
    db = mongodb_client.get_db()
    
    model = db[PREFERENCE_MODEL_TABLE_NAME].find_one({'userId': user_id})
    if model is None:
        return []

    sorted_tuples = sorted(model['preference'].items(), key=operator.itemgetter(1), reverse=True)

    print sorted_tuples
    #sorted_list = [x[0] for x in sorted_tuples]
    #sorted_value_list = [x[1] for x in sorted_tuples]

    # If the first preference is same as the last one, the preference makes
    # no sense.
    #if isclose(float(sorted_value_list[0]), float(sorted_value_list[-1])):
    #   return []
    return sorted_tuples

def sortNews(news_class_digests, preference):
    prefer = []
    rest = []
    num = 0
    for item in news_class_digests:
        num = num + 1
        print num
        if item[0] == preference[0]:
            prefer.append(item[1])
        else:
            rest.append(item[1])
        
    total = prefer + rest 

    return total

def logNewsClickForUser(user_id, news_id, user_ip):
    message = {'userId': user_id, 'newsId': news_id, 'timestamp': datetime.utcnow()}

    db = mongodb_client.get_db()
    db[CLICK_LOGS_TABLE_NAME].insert(message)

    # Send log task to machine learning service for prediction
    message = {'userId': user_id, 'newsId': news_id, 'timestamp': str(datetime.utcnow())}
    cloudAMQP_client.sendMessage(message)

    logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s%(message)s',
                datefmt='%a %d %b %Y %H:%M:%S' + ',',
                filename='../logging/user_requests.log',
                filemode='a')
    logging.info(', ' +
                 'event_name : ' + 'news_request' + ', ' + 
                 'user_id : ' + str(user_id) + ', ' +
                 'user_ip : ' + str(user_ip) + ', ' +
                 'news_id : ' + str(news_id)) 