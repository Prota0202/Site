from pymongo import MongoClient
from django.conf import settings

client = MongoClient('localhost', 27017)  # ou l'URL de connexion de MongoDB
db = client[settings.MONGO_DB_NAME]


def get_db():
    return db
