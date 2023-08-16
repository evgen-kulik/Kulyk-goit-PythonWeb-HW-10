from django.http import HttpResponse

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from .models import Author

# Create your views here.
from .utils import get_mongodb
from bson.objectid import ObjectId
import psycopg2


# імпортувати з папки utils не виходить, тому прописано тут
def make_total_list_from_postgres():
    """
    Повертає список словників зі всією інформацією для сайту з бази даних postgres
    :return:
    """

    conn = psycopg2.connect(
        dbname="hw_10_postgres", user="postgres", password="567234", host="127.0.0.1"
    )  # зробили конект до БД
    cursor = conn.cursor()
    # сформуємо список даних по авторах (поки без тегів)
    cursor.execute(
        "SELECT qa.id, qa.fullname, qa.born_date, qa.born_location, qa.description, qq.quote, q.name "
        "FROM quotes_tag AS q JOIN quotes_quote_tags AS qt ON q.id = qt.quote_id "
        "JOIN quotes_quote AS qq ON qq.id = qt.quote_id "
        "JOIN quotes_author AS qa ON qa.id = qq.author_id ORDER BY qa.id"
    )

    # одразу приберемо повторення зі списку
    author_postgres = list(set(cursor.fetchall()))
    # print(len(author_postgres))  # [0] - id, [1]-name, [2]-date, [3]-location, [4]-bio, [5]-quote, [6]-tag

    # Зробимо загальний список словників
    total_list = []
    for i in author_postgres:
        dct = {}
        dct["id"] = i[0]
        dct["author"] = i[1]
        dct["born_date"] = i[2]
        dct["born_location"] = i[3]
        dct["description"] = i[4]
        dct["quote"] = i[5]
        dct["tags"] = [i[6]]
        total_list.append(dct)
    # print(total_list)
    # print(len(total_list))

    # отримаємо списки тегів для id авторів
    cursor.execute(
        "SELECT qa.id, q.name "
        "FROM quotes_tag AS q JOIN quotes_quote_tags AS qt ON q.id = qt.quote_id "
        "JOIN quotes_quote AS qq ON qq.id = qt.quote_id "
        "JOIN quotes_author AS qa ON qa.id = qq.author_id ORDER BY qa.id"
    )

    author_postgres = cursor.fetchall()
    tags_dct = {}
    for i in author_postgres:
        if i[0] not in tags_dct.keys():
            tags_dct[i[0]] = [i[1]]
        else:
            if i[1] not in tags_dct[i[0]]:
                tags_dct[i[0]].append(i[1])
    # print(tags_dct)
    # print(len(tags_dct))

    # додамо списки тегів в загальний список словників
    for i in total_list:
        # print(i)
        for key in tags_dct:
            if i["id"] == key:
                i["tags"] = tags_dct[key]
    # print(len(total_list))
    # print(total_list)
    return total_list


def main(request, page=1):
    total_list = make_total_list_from_postgres()
    print(total_list)
    per_page = 10  # виводиметься по 10 елементів на сторінці
    paginator = Paginator(total_list, per_page)
    quotes_on_page = paginator.page(
        page
    )  # тут список всіх елементів розбивається по сторінках
    return render(request, "quotes/index.html", context={"quotes": quotes_on_page})

    # -------------------------------
    # db = get_mongodb()  # зробили конект до БД
    # quotes = db.quotes.find()  # знайшли всі quotes, прокидуємо їх в context=
    # print(list(quotes))
    # per_page = 10  # виводиметься по 10 елементів на сторінці
    # paginator = Paginator(list(quotes), per_page)
    # quotes_on_page = paginator.page(page)  # тут список всіх елементів розбивається по сторінках
    # # print('---------------', list(quotes_on_page))
    # return render(request, 'quotes/index.html', context={'quotes': quotes_on_page})
    # -------------------------------


def about(request, quote_id):
    # description =

    description = Author.objects.filter(pk=quote_id)
    # description = Author.objects.filter(pk=pic_id)
    # # description = Author.objects.all().filter(pk=pic_id).first()
    # # description = Author.objects.all().filter(pk=pic_id)
    # # description = Author.objects.all()
    #
    print(list(description))
    print("About done!")
    return render(request, "quotes/description.html", context={"authors": description})
