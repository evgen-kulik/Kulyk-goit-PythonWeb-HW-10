from django.urls import path

from . import views  # наші представлення

app_name = "quotes"  # даємо назву нашому застосунку

urlpatterns = [
    path("", views.main, name="root"),
    path("<int:page>", views.main, name="root_paginate"),
]
# "" - вказуємо на корінь проєкту; root - ім'я для маршруту
