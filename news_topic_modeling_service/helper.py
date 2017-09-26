import os
import sys

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
import news_topic_modeling_service_client

if __name__ == '__main__':
    db = mongodb_client.get_db()
    news_cursor = db['news-test'].find({})
    count = 0
    one = 0
    two = 0
    three = 0
    four = 0
    five = 0
    six = 0
    seven = 0
    eight = 0
    nine = 0
    ten = 0
    eleven = 0
    twlve = 0
    thirteen = 0
    fourteen = 0
    fifteen = 0
    sixteen = 0
    seventeen = 0

    for news in news_cursor:
        count += 1
        print count
        if news.get('class') == 'Colleges & Schools':
            one += 1
        if news.get('class') == 'Environmental':
            two += 1
        if news.get('class') == 'World':
            three += 1
        if news.get('class') == 'Entertainment':
            four += 1
        if news.get('class') == 'Media':
            five += 1
        if news.get('class') == 'Politics & Government':
            six += 1
        if news.get('class') == 'Regional News':
            seven += 1
        if news.get('class') == 'Religion':
            eight += 1
        if news.get('class') == 'Sports':
            nine += 1
        if news.get('class') == 'Technology':
            ten += 1
        if news.get('class') == 'Traffic':
            eleven += 1
        if news.get('class') == 'Weather':
            twlve += 1
        if news.get('class') == 'Economic & Corp':
            thirteen += 1
        if news.get('class') == 'Advertisements':
            fourteen += 1
        if news.get('class') == 'Crime':
            fifteen += 1
        if news.get('class') == 'Other':
            sixteen += 1
        if news.get('class') == 'Magazine':
            seventeen += 1

    print count
    print 'one ' + str(one)
    print two 
    print three 
    print 'four '  + str(four) 
    print five 
    print six 
    print seven 
    print 'eight ' + str(eight) 
    print nine 
    print ten 
    print eleven 
    print 'twlve '+ str(twlve) 
    print thirteen 
    print fourteen 
    print fifteen 
    print 'sixteen ' + str(sixteen)
    print seventeen 
        