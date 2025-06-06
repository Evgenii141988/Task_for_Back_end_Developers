import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '5c3e84ea039ee9dbe43be1d63e47946f24a65c2a'
    MONGO_URI = 'mongodb://localhost:27017/flask_mongo_db'
