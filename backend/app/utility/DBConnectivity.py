from pprint import pprint
from pymongo import MongoClient

# def create_mongo_connection(database_name = conf.mongoconfig.get('database_name')):
#     mongo = MongoClient(conf.mongoconfig.get('connection_url'), maxPoolSize=200)
#     return mongo[database_name]

def create_mongo_connection(database_name = "smartqr"):
    mongo = MongoClient("mongodb+srv://seema:LZ24HejZcsad4EAZ@seema-test-db.olbxs76.mongodb.net/", maxPoolSize=200)
    return mongo[database_name]

# def create_mongo_connection(database_name = "smartqr"):
#     password = "Fkljspq0RNUdJMLC"
#     username = "shaikhseemaar"
#     conn_str = f"mongodb+srv://{username}:{password}@smart-prod.1vmpufs.mongodb.net/"
#     mongo = MongoClient(conn_str, maxPoolSize=200)
#     return mongo[database_name]

