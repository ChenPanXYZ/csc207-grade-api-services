from config import MONGO_DB_CONNECTION_STRING
from pymongo import MongoClient
client = MongoClient(MONGO_DB_CONNECTION_STRING)
db = client['grade-apis']
USER = db['users']
GRADE = db['grades']
TEAM = db['teams']