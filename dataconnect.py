import datetime

from pymongo import MongoClient
client = MongoClient("mongodb+srv://vi280708ovv:l20nfH2au0qg63ml@cluster0.h1bqaam.mongodb.net/kurs_valut", ssl=True)


def put_to_database(dict,time):
    db = client["kurs_valut"]
    collections_kurs = db['kurs']
    document = {
        "kurs": dict,
        "timestamp": time

    }
    collections_kurs.insert_one(document)

