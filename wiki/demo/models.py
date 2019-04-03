from django.db import models as m


class Article(m.Model):
    title = m.CharField('Article title', max_length=30)
    body = m.TextField('Article body text', max_length=400)
    pub_on = m.DateTimeField('Date this article was published')
    pub_by = m.CharField('Writer that wrote this article', max_length=40)
    # wiki
    wiki_id = m.IntegerField(null=True)

    def __str__(self):
        return '{} by {}'.format(self.title, self.pub_by)
