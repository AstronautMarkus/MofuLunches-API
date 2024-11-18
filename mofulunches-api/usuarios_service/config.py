import os

class Config:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://reyesandfriends.cl:27017/mofulunches")
