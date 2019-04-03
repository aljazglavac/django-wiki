from django.contrib import admin
from .models import Writer, Article


@admin.register(Writer)
class WriterAdmin(admin.ModelAdmin):
    pass


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'pub_on', 'pub_by')
