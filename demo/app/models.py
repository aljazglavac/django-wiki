from django.db import models as m
from wiki.models import WikiModel


class Article(WikiModel):
    title = m.CharField('Article title', max_length=30)
    body = m.TextField('Article body text', max_length=400)
    pub_on = m.DateTimeField('Date this article was published')
    pub_by = m.CharField('Writer that wrote this article', max_length=40)

    def __str__(self):
        return '{} by {}'.format(self.title, self.pub_by)
