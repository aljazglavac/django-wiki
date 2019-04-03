from django.db import models as m


class Writer(m.Model):
    first_name = m.CharField('Writers first name', max_length=10)
    last_name = m.CharField('Writers last name', max_length=20)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

class Article(m.Model):
    title = m.CharField('Article title', max_length=30)
    body = m.TextField('Article body text', max_length=400)
    pub_on = m.DateTimeField('Date this article was published.')
    pub_by = m.ForeignKey(Writer, on_delete=m.CASCADE)

    def __str__(self):
        return '{} by {}'.format(self.title, self.pub_by)
