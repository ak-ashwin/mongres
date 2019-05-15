from pymongo import MongoClient
from sqlalchemy import create_engine


def postgres_db_init():
    db = create_engine('postgresql://postgres:postgres@localhost:5432/test2')
    db.connect()


def mongo_db_init():
    client = MongoClient('mongodb://localhost:27017')
    return client
