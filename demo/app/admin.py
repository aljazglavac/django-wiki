from django.contrib import admin
from .models import Article
from wiki.admin import WikiModelAdmin # USER ADD

@admin.register(Article)
class ArticleAdmin(WikiModelAdmin): # USER ADD
    list_display = ('title', 'body', 'pub_on', 'pub_by')
