from pymongo import MongoClient
from app.log import logger

def connect_mongo():
    conn = MongoClient('localhost', 27017)

    return conn


def save_mongo(database, collection, data):
    conn = connect_mongo()
    db = conn[database] 
    col = db[collection]

    if type(data) is list:
        col.insert_many(data)
        for i in data:
            if verify_exists(col, i) == False:
                logger.info("Salvando no Banco")
                try:
                    col.insert_one(data)
                except:
                    breakpoint()

    if type(data) is dict:
        if verify_exists(col, data) == False:
            logger.info("Salvando no Banco")
            try:
                col.insert_one(data)
            except:
                breakpoint()
    conn.close()


def read_mongo(database, collection):
    conn = connect_mongo()
    db = conn[database] 
    data = db[collection].find()

    return data


def search_mongo(database, collection, field, value_field):
    conn = connect_mongo()
    db = conn[database] 
    data = db[collection].find({field: value_field}, no_cursor_timeout=True)

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

def delete_register(database, collection, data):
    logger.info(f"Deletando registro {data}")
    conn = connect_mongo()
    db = conn[database]
    db[collection].delete_one(data)