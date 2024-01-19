from pymongo import MongoClient
from flask import Flask

app = Flask(__name__)

client = MongoClient("mongodb://admin:admin@localhost","27017")

db = client["yuval"]


if "githubRepos" not in db.list_collection_names():
    db.create_collection("githubRepos")

collection = db.get_collection("githubRepos")

collection.insert_one()