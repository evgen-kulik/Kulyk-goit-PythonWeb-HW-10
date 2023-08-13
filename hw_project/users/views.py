from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages  # зберігає до першого зчитування дані

from .forms import RegisterForm


class RegisterView(View):
    form_class = RegisterForm
    template_name = "users/signup.html"

    def get(self, request):
        """Повертає рендеринг сторінки"""
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request):
        """Логіка роботи з полями реєстрації користувача"""

        form = self.form_class(request.POST)
        if form.is_valid():
            print("VALID!ok!")
            form.save()  # Запис у БД
            print("SAVED in DB!")
            username = form.cleaned_data["username"]  # тут зберігається те, що пройшло валідацію
            messages.success(request, f'{username}, your account has been successfully created!')
            return redirect(to="users:login")  # адреса, куди перенаправиться юзер у випадку успішної валідації

        print('NOT valid!')
        return render(request, self.template_name, {"form": form})
        # у випадку неуспішності валідації юзер залишається на тій самій сторінці реєстрації
