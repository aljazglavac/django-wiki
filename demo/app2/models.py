from django.db import models


class Reporter(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    # wiki
    wiki_id = models.IntegerField(null=True) # USER ADD

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Post(models.Model):
    headline = models.CharField(max_length=100)
    pub_date = models.DateField()
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)
    # wiki
    wiki_id = models.IntegerField(null=True) # USER ADD

    def __str__(self):
        return self.headline

    class Meta:
        ordering = ('headline', )
