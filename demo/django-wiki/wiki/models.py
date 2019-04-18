from django.db import models as m


class CustomManager(m.Manager):
    def valid(self):
        return self.filter(pk=m.F("wiki_id"))

    def invalid(self):
        return self.filter(~m.Q(pk=m.F("wiki_id")) | m.Q(wiki_id__isnull=True))


class WikiModel(m.Model):
    wiki_id = m.IntegerField(null=True, default=None, editable=False)
    objects = CustomManager()

    class Meta:
        abstract = True
