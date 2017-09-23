import news_topic_modeling_service_client as client

def test_basic():
    newsTitle = 'Trump stayed mostly indoors during his visit to the state on Tuesday, where he received briefings on the disaster relief efforts from federal, state and local officials -- an itinerary aimed at avoiding the worst-hit areas so as not to pull emergency responder resources from ongoing search-and-rescue operations.'
    topic = client.classify(newsTitle)
    assert topic == 'Politics & Government'
    print 'test_basic passed!'

if __name__ == '__main__':
    test_basic()