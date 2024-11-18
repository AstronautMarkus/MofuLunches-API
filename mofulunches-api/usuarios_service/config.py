import os

class Config:
    # MongoDB URI
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://reyesandfriends.cl:27017/mofulunches")
    
    # Flask secret key for session cookies and CSRF
    SECRET_KEY = os.getenv("SECRET_KEY", "clave_secreta_predeterminada")
    
    # JWT secret key
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "clave_jwt_secreta_predeterminada")
    
    # JWT expiration time
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 3600))  # default 1 hour
