''' test database connection '''
import mongodb_client as client


def test_basic():
    ''' test database connection '''
    database = client.get_db('tap-news')
    database.testCollection.drop()
    assert database.testCollection.count() == 0
    database.testCollection.insert({'test': 1, 'hello': 'world'})
    assert database.testCollection.count() == 1
    database.testCollection.drop()
    assert database.testCollection.count() == 0
    print 'test_basic passed'


if __name__ == '__main__':
    test_basic()
