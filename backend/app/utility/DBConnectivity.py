from pymongo import MongoClient
from app.conf.config import app

def create_mongo_connection(database_name = "smartqr"):
    mongo = MongoClient(app.config["DATABASE_URL"], maxPoolSize=200)
    return mongo[database_name]
