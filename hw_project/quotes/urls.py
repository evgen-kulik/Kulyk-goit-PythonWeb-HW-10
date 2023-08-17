from django.urls import path, include
from . import views  # наші представлення

app_name = "quotes"  # даємо назву нашому застосунку

urlpatterns = [
    path("", views.main, name="root"),
    path("<int:page>", views.main, name="root_paginate"),
    path("description/<int:quote_id>/", views.about, name="description"),
    path("tags/<str:tag_name>", views.authors_by_tags, name="tags")
]
# "" - вказуємо на корінь проєкту; root - ім'я для маршруту
# <int:auth_id> - пасс-параметр (№ id в БД) до якого ми маємо доступ
# path("description/<int:quote_id>/", views.about, name='description')
# <назва змінної> передається в якості назви аргументу в функцію  в vews.py!
