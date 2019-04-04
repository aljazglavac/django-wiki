from django.db import models as m


class Person(m.Model):
    first_name = m.CharField('Name', max_length=30)
    last_name = m.CharField('Surename', max_length=30)
    # wiki
    wiki_id = m.IntegerField(null=True) # USER ADD

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)
