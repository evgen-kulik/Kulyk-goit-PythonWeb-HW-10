from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from .models import Author
# Create your views here.
from .utils import get_mongodb
from bson.objectid import ObjectId


def main(request, page=1):
    db = get_mongodb()  # зробили конект до БД
    quotes = db.quotes.find()  # знайшли всі quotes, прокидуємо їх в context=
    per_page = 10  # виводиметься по 10 елементів на сторінці
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)  # тут список всіх елементів розбивається по сторінках
    return render(request, 'quotes/index.html', context={'quotes': quotes_on_page})


def about(request, pic_id):
    description = Author.objects.filter(pk=pic_id).first()
    print(description)
    return render(request, 'quotes/description.html', context={'authors': description})


