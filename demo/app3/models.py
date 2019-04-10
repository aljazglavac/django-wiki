from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    # wiki
    wiki_id = models.IntegerField(null=True)  # USER ADD


class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    # wiki
    wiki_id = models.IntegerField(null=True)  # USER ADD
