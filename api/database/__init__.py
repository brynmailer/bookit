import os
import pymongo

client = pymongo.MongoClient('ds351455.mlab.com', 51455, retryWrites=False)
db = client['bookit']
db.authenticate(os.environ['DB_USER'], os.environ['DB_PASSWORD'])