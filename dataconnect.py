import os

from pymongo import MongoClient

DATABASE_URL = os.getenv("DATABASE_URL")
client = MongoClient(DATABASE_URL, ssl=True)


def put_to_database(dict,time):
    db = client["kurs_valut"]
    collections_kurs = db['kurs']
    document = {
        "kurs": dict,
        "timestamp": time

    }
    collections_kurs.insert_one(document)

