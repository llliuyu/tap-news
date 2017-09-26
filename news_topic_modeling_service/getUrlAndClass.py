import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
import news_topic_modeling_service_client


if __name__ == '__main__':
    db = mongodb_client.get_db()
    news_cursor = db['news-test'].find({})
    with open ('./training_data/url.csv', 'w') as n:
        for news in news_cursor:
            if news.get('class'):
                if news.get('text'):
                    n.write(news.get('class').encode('utf-8') + ',"' + news.get('text').encode('utf-8').replace('\n','').replace(',','') + '",' + news.get('source').encode('utf-8') + "\n")
                else:
                    n.write(news.get('class').encode('utf-8') + ',"' + news.get('description').encode('utf-8').replace('\n','').replace(',','') + '",' + news.get('source').encode('utf-8') + "\n")
    '''n=0
    for news in news_cursor:
        
        source = news['source'] 
        
        if source == 'espn' or source == 'bbc-sport' or source == 'fox-sports' or source =='talksport':
            news['class'] = 'Sports'
            db['news-test'].replace_one({'digest': news['digest']}, news, upsert=True)

        elif source == 'entertainment-weekly' or source == 'mtv-news':
            news['class'] = 'Entertainment'
            db['news-test'].replace_one({'digest': news['digest']}, news, upsert=True)
            
        elif source == 'techcrunch' or source == 't3n' or source == 'recode' or source == 'techradar' or source == 'new-scientist':
            news['class'] = 'Technology'
            db['news-test'].replace_one({'digest': news['digest']}, news, upsert=True)
            
        elif source == 'the-lad-bible':
            news['class'] = 'Religion'
            db['news-test'].replace_one({'digest': news['digest']}, news, upsert=True)
            
        elif source == 'the-wall-street-journal' or source == 'the-economist':
            news['class'] = 'Economic & Corp'
            db['news-test'].replace_one({'digest': news['digest']}, news, upsert=True)
            
        elif source == 'new-york-magazine':
            news['class'] = 'Magazine'
            db['news-test'].replace_one({'digest': news['digest']}, news, upsert=True)
        elif source == 'ign':
            news['class'] = 'Media'
            db['news-test'].replace_one({'digest': news['digest']}, news, upsert=True)
        n += 1
    print n'''

    