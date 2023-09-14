from django.db import models
from django.urls import reverse


# Create your models here.


class Author(models.Model):
    fullname = models.CharField(max_length=50, unique=True)
    born_date = models.CharField(max_length=50)
    born_location = models.CharField(max_length=150)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fullname  # Для відображення на сторінці fullname, а не object_id


class Tag(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)

    def __str__(self):
        return (
            self.name
        )  # Для відображення на сторінці і в адмінці name, а не object_id


class Quote(models.Model):
    quote = models.TextField()
    tags = models.ManyToManyField(Tag)  # Django сам створить таблицю зв'язків
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, default=None, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.quote
