"""Доступ до БД hw_10 для виводу даних на сайт"""


from pymongo import MongoClient

def get_mongodb():
    client = MongoClient("mongodb://localhost")

    db = client.hw_10
    return db