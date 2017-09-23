import logging
import os
import sys
import yaml

from newspaper import Article

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'scrapers'))

#import cnn_news_scraper
from cloudAMQP_client import CloudAMQPClient

with open('../configuration/news_pipeline_conf.yaml', 'r') as stream:
    try:
        config = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)

dedupe_news_queue_client = CloudAMQPClient(config['news_fecher']['DEDUPE_NEWS_TASK_QUEUE_URL'], 
                                           config['news_fecher']['DEDUPE_NEWS_TASK_QUEUE_NAME'])
scrape_news_queue_client = CloudAMQPClient(config['news_fecher']['SCRAPE_NEWS_TASK_QUEUE_URL'], 
                                           config['news_fecher']['SCRAPE_NEWS_TASK_QUEUE_NAME'])


def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        print 'message is broken'
        return
    
    task = msg
    text = None

    article = Article(task['url'])
    article.download()
    article.parse()

    task['text'] = article.text.encode('utf-8')

    '''if task['source'] == 'cnn':
        print 'scraping CNN news'
        text = cnn_news_scraper.extract_news(task['url'])
    else:
        print 'news source [%s] is not supported' % task['source'] 

    task['text'] = text '''
    # print 'message numbers:' + dedupe_news_queue_client.getMessage_count()
    dedupe_news_queue_client.sendMessage(task)

    logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s%(message)s',
                datefmt='%a %d %b %Y %H:%M:%S' + ',',
                filename='../logging/news_pipeline.log',
                filemode='a')
    logging.info(', ' +
                 'event_name : ' + 'get_news_text_from_source' + ', ' + 
                 'queue_name : ' + str(config['news_fecher']['SCRAPE_NEWS_TASK_QUEUE_NAME']) + ', ' +
                 'news_id : ' + str(task['digest']))


while True:
    if scrape_news_queue_client is not None:
        msg = scrape_news_queue_client.getMessage()
        if msg is not None:
            try:
                handle_message(msg)
            except Exception as e:
                print 
                pass
        scrape_news_queue_client.sleep(config['news_fecher']['SLEEP_TIME_IN_SECONDS'])