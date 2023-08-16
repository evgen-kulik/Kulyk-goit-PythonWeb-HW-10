"""Отримання авторів з БД за id"""


from bson.objectid import ObjectId

from django import template

from ..utils import get_mongodb  # '..' означає вийти на рівень вище

register = template.Library()


def get_author(id_):
    db = get_mongodb()
    author = db.authors.find_one({"_id": ObjectId(id_)})
    return author["fullname"]


# реєструємо авторів
register.filter("author", get_author)
# є 'author', для його отримання використовується get_author
