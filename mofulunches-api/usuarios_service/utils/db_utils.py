from pymongo import MongoClient
from config import Config

# Inicializa la conexión con MongoDB
def get_db():
    client = MongoClient(Config.MONGO_URI)
    db = client.get_default_database()  
    return db
