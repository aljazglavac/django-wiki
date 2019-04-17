from django.db import models as m
from wiki.models import WikiModel


class Person(WikiModel):
    first_name = m.CharField('Name', max_length=30)
    last_name = m.CharField('Surename', max_length=30)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)
