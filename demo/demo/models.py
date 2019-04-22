from django.db import models
from wiki.models import WikiModel


class Author(WikiModel):
    name = models.CharField(max_length=100)


class Book(WikiModel):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
