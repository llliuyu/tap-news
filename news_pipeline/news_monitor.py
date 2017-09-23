import datetime
import hashlib
import logging
import redis
import os
import sys
import yaml

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import  news_api_client
from  cloudAMQP_client import CloudAMQPClient

with open('../configuration/news_pipeline_conf.yaml', 'r') as stream:
    try:
        config = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)

redis_client = redis.StrictRedis(config['news_monitor']['REDIS_HOST'], 
                                 int(config['news_monitor']['REDIS_PORT']))

cloudAMQP_client = CloudAMQPClient(config['news_monitor']['SCRAPE_NEWS_TASK_QUEUE_URL'], 
                                   config['news_monitor']['SCRAPE_NEWS_TASK_QUEUE_NAME'])

while True:
    news_list = news_api_client.getNewsFromSource(config['news_monitor']['NEWS_SOURCES'])

    num_of_news_news = 0

    for news in news_list:
        news_digest = hashlib.md5(news['title'].encode('utf-8')).digest().encode('base64')  # digest can be used as a unique ID

        if redis_client.get(news_digest) is None:
            '''new news coming in'''
            num_of_news_news = num_of_news_news + 1
            news['digest'] = news_digest

            if news['publishedAt'] is None:
                news['publishedAt'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

            redis_client.set(news_digest, 'True')
            redis_client.expire(news_digest, config['news_monitor']['NEWS_TIME_OUT_IN_SECONDS'])

            cloudAMQP_client.sendMessage(news)


    # print 'Fetched %d news.' % num_of_news_news

    cloudAMQP_client.sleep(config['news_monitor']['SLEEP_TIME_IN_SECONDS'])