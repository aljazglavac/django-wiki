from django.contrib import admin
from .models import Article
from wiki.admin import WikiModelAdmin

@admin.register(Article)
class ArticleAdmin(WikiModelAdmin):
    list_display = ('title', 'body', 'pub_on', 'pub_by')
    readonly_fields = ('wiki_id',)
    change_form_template = 'demo/custom_change_form.html'

