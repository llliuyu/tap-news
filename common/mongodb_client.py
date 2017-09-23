''' create a  mongodb client '''
from pymongo import MongoClient

MONGO_DB_HOST = 'localhost'
MONGO_DB_PORT = '27017'
DB_NAME = 'tap-news'


MONGO_CLIENT = MongoClient("%s:%s" % (MONGO_DB_HOST, MONGO_DB_PORT))


def get_db(database=DB_NAME):
    ''' return a mongodb client with name DB_NAME '''
    return MONGO_CLIENT[database]
