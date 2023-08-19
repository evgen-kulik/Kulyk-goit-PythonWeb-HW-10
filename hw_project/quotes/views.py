from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.views import View

from .forms import AuthorForm, QuoteForm
from .models import Author, Tag, Quote


def main(request, page=1):
    quotes = Quote.objects.select_related('author').prefetch_related('tags').all().order_by('created_at')
    # quotes = Quote.objects.all()  # другий робочий варіант вибірки даних
    per_page = 10  # виводиметься по 10 елементів на сторінці
    paginator = Paginator(quotes, per_page)
    quotes_on_page = paginator.page(
        page
    )  # тут список всіх елементів розбивається по сторінках
    return render(request, "quotes/index.html", context={"quotes": quotes_on_page})


def about(request, quote_id):
    """Перехід по кнопці 'about'"""

    description = Author.objects.filter(pk=quote_id)
    return render(request, "quotes/description.html", context={"authors": description})


def authors_by_tags(request, tag_name):
    """Перехід по тегу"""

    tags = Tag.objects.filter(name=tag_name).first()
    quotes = tags.quote_set.all()
    return render(request, "quotes/tags.html", context={"quotes": quotes})


class AuthorView(View):
    """Додавання автора"""

    template_name = 'quotes/add_author.html'
    form_class = AuthorForm
    model = Author

    def get(self, request):
        """Повертає рендеринг сторінки"""
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request):
        """Логіка роботи з полями автора"""

        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()  # Запис у БД
            return redirect(to='quotes:root')

        return render(request, self.template_name, {"form": form})
        # у випадку неуспішності валідації юзер залишається на тій самій сторінці


class QuoteView(View):
    """Додавання цитати"""

    template_name = 'quotes/add_quote.html'
    form_class = QuoteForm
    model = Quote

    def get(self, request):
        """Повертає рендеринг сторінки"""
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request):
        """Логіка роботи з полями автора"""

        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()  # Запис у БД
            return redirect(to='quotes:root')

        return render(request, self.template_name, {"form": form})
        # у випадку неуспішності валідації юзер залишається на тій самій сторінці

