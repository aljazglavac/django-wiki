from django.db import models as m


class Writer(m.Model):
    first_name = m.CharField('Writers first name', max_length=10)
    last_name = m.CharField('Writers last name', max_length=20)


class Article(m.Model):
    title = m.CharField('Article title', max_length=30)
    body = m.CharField('Article body text', max_length=400)
    pub_on = m.DateTimeField('Date this article was published.')
    pub_by = m.ForeignKey(Writer, on_delete=m.CASCADE)
