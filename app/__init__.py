from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mongo = PyMongo(app)
db = mongo.db
users_collection = db.users

from app import routes
