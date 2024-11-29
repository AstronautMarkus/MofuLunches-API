from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    DEBUG = False
    ALIMENTOS_SERVICE_URL = os.getenv('ALIMENTOS_SERVICE_URL')
    PEDIDOS_SERVICE_URL = os.getenv('PEDIDOS_SERVICE_URL')
    USUARIOS_SERVICE_URL = os.getenv('USUARIOS_SERVICE_URL')
    MONGODB_URI = os.getenv('MONGODB_URI')

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
