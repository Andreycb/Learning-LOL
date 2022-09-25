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

def verify_exists(collection, data):
    if collection.count_documents(data) != 0:
        logger.info("Registro existe no banco")
        return True

    return False