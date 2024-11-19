from pymongo import MongoClient
from config import Config

# Mongo connection
def get_db():
    client = MongoClient(Config.MONGO_URI)
    db = client["mofulunches"]
    return db
