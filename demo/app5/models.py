from django.db import models
from wiki.models import WikiModel

# Create your models here.

class Oseba(WikiModel):
    ime = models.CharField(max_length=100)


class Knjiga(WikiModel):
    oseba = models.ForeignKey(Oseba, on_delete=models.CASCADE)
    naslov = models.CharField(max_length=100)
