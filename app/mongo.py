from pymongo import MongoClient
from app.log import logger

def connect_mongo():
    conn = MongoClient('localhost', 27017)

    return conn


def save_mongo(database, collection, data):
    conn = connect_mongo()
    db = conn[database] 
    col = db[collection]
    if verify_exists(col, data) == False:
        logger.info("Salvando no Banco")
        col.insert_one(data)

    conn.close()


def read_mongo(database, collection):
    conn = connect_mongo()
    db = conn[database] 
    data = db[collection].find()

    return data


def search_mongo(database, collection, field, value_field):
    conn = connect_mongo()
    db = conn[database] 
    data = db[collection].find({field: value_field})

    if len(list(data)) != 0:
        return True

    return False


def distinct_mongo(database, collection, field):
    conn = connect_mongo()
    db = conn[database] 
    data = db[collection].distinct(field)

    return data


def verify_exists(collection, data):
    if collection.count_documents(data) != 0:
        logger.info("Registro existe no banco")
        return True

    return False