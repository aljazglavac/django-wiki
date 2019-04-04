from django.contrib import admin
from .models import Article
from wiki.admin import WikiModelAdmin

@admin.register(Article)
class ArticleAdmin(WikiModelAdmin):
    list_display = ('title', 'body', 'pub_on', 'pub_by')
