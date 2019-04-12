from django.db import models
from wiki.models import WikiModel


class Fish(WikiModel):
    fish_name = models.CharField(max_length=30)

    def __str__(self):
        return self.fish_name
