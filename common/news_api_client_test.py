import news_api_client as client

NEWS_SOURCES = [
    'bbc-news',
    'bbc-sport',
    'bloomberg',
    'cnn',
    'entertainment-weekly',
    'espn',
    'ign',
    'techcrunch',
    'the-new-york-times',
    'the-wall-street-journal',
    'the-washington-post',
    'reddit-r-all',
    'cbs',
    'abc',
    'usa-today',
    'time',
    'polygon',
    'hacker-news',
    'engadget',
    'reuters',
    'google-news',
    'cnbc',
    'fortune',
    'focus',
    'recode'
]


def test_basic():
    news = client.getNewsFromSource()
    print news
    assert len(news) > 0
    news = client.getNewsFromSource(sources=[NEWS_SOURCES], sortBy='top')


if __name__ == '__main__':
    test_basic()