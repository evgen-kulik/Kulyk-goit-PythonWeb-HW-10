"""Обробляє quotes.json для додавання в БД. Під авторами записує реферальні посилання."""

import json
from bson.objectid import ObjectId

from pymongo import MongoClient


client = MongoClient("mongodb://localhost")

db = client.hw_10

with open("quotes.json", "r", encoding="utf-8") as fd:
    quotes = json.load(fd)

for quote in quotes:
    author = db.authors.find_one({"fullname": quote["author"]})
    # це повна одиниця колекції authors, яка вже зберігається в БД
    # тут знаходимо елемент в БД, який відповідає елементу в quotes.json
    if author:  # якщо така одиниця є
        db.quotes.insert_one(
            {
                "quote": quote["quote"],
                "tags": quote["tags"],
                "author": ObjectId(
                    author["_id"]
                ),  # посилання на відповідний елемент в БД
            }
        )
