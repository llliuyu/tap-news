import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
import news_topic_modeling_service_client


if __name__ == '__main__':
    db = mongodb_client.get_db()
    news_cursor = db['user_preference_model'].find({})

    for news in news_cursor:
    	print news['preference']
    	for c,v in news['preference'].items():
    		print v
    	break