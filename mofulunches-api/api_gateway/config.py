class Config:
    DEBUG = True
    ALIMENTOS_SERVICE_URL = 'http://localhost:5001'
    PEDIDOS_SERVICE_URL = 'http://localhost:5002'
    USUARIOS_SERVICE_URL = 'http://localhost:5003'

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
