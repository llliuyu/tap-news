import datetime
import logging
import os
import sys
import yaml

from dateutil import parser
from sklearn.feature_extraction.text import TfidfVectorizer

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common')) 
 
import mongodb_client
import news_topic_modeling_service_client
from cloudAMQP_client import CloudAMQPClient

with open('../configuration/news_pipeline_conf.yaml', 'r') as stream:
    try:
        config = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)

cloudAMQP_client = CloudAMQPClient(config['news_deduper']['DEDUPE_NEWS_TASK_QUEUE_URL'], 
                                   config['news_deduper']['DEDUPE_NEWS_TASK_QUEUE_NAME'])

def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        return
    task = msg
    text = task['text']
    if text is None:
        return
    
    ''' get news from database with similar time '''
    published_at = parser.parse(task['publishedAt'])
    published_at_day_begin = datetime.datetime(published_at.year, published_at.month, published_at.day, 0, 0, 0, 0)
    published_at_day_end = published_at_day_begin + datetime.timedelta(days=1)

    db = mongodb_client.get_db()
    same_day_news_list = list(db[config['news_deduper']['NEWS_TABLE_NAME']].find(
        {'publishedAt': {'$gte': published_at_day_begin,
                         '$lt': published_at_day_end}}))

    if same_day_news_list is not None and len(same_day_news_list) > 0:
        documents = [news['text'] for news in same_day_news_list]
        documents.insert(0, text)

        tfidf = TfidfVectorizer().fit_transform(documents)
        pairwise_sim = tfidf * tfidf.T

        print pairwise_sim

        rows, _ = pairwise_sim.shape

        for row in range(1, rows):
            if pairwise_sim[row, 0] > config['news_deduper']['SAME_NEWS_SIMILARITY_THRESHOLD']:
                print 'Duplicated news. Ignore.'
                return

    task['publishedAt'] = parser.parse(task['publishedAt'])
   
    # classify news
    description = task['description']
    source = task['source']

    if source == 'bbc-sport' or source == 'espn' or source == 'fox-sports' or source == 'talksport':
        task['class'] = 'Sports'
    elif source == 'entertainment-weekly' or source == 'mtv-news':
        task['class'] = 'Entertainment'
    elif source == 'techcrunch' or 't3n' or source == 'recode' or source == 'techradar' or source == 'new-scientist':
        task['class'] = 'Technology'
    elif source == 'the-lad-bible':
        task['class'] = 'Religion'
    elif source == 'the-wall-street-journal' or source == 'the-economist':
        task['class'] = 'Economic & Corp'
    elif source == 'new-york-magazine':
        task['class'] = 'Magazine'
    elif source == 'ign':
        task['class'] = 'Media'
    else description is not None:
        topic = news_topic_modeling_service_client.classify(description)
        task['class'] = topic

    db[config['news_deduper']['NEWS_TABLE_NAME']].replace_one({'digest': task['digest']}, task, upsert=True)


    logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s%(message)s',
                datefmt='%a %d %b %Y %H:%M:%S' + ',',
                filename='../logging/news_pipeline.log',
                filemode='a')
    logging.info(', ' +
                 'event_name : ' + 'news_dedupe' + ', ' + 
                 'queue_name : ' + str(config['news_deduper']['DEDUPE_NEWS_TASK_QUEUE_NAME']) + ', ' +
                 'news_id : ' + str(task['digest']))

while True:
    if cloudAMQP_client is not None:
        msg = cloudAMQP_client.getMessage()
        if msg is not None:
            # Parse and process the task
            try:
                handle_message(msg)
            except Exception as e:
                print e
                pass

        cloudAMQP_client.sleep(config['news_deduper']['SLEEP_TIME_IN_SECONDS'])
