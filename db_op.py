import flask_pymongo as pymongo
from flask_pymongo import MongoClient

MONGO_DB_NAME = 'recipes_api'
DB_USERNAME = 'matilde'
DB_PASS = '1234'
MONGODB_HOST = f'mongodb+srv://{DB_USERNAME}:{DB_PASS}@cluster0.kqtyo.mongodb.net/{MONGO_DB_NAME}?retryWrites=true&w=majority'

def db_connection():
    cluster = MongoClient(MONGODB_HOST)
    db = cluster[MONGO_DB_NAME]
    return db