import os
import pymongo

client = pymongo.MongoClient("mongodb://0.0.0.0:27017/")
db = client.bookit_db
