from django.contrib import admin
from wiki.admin import WikiModelAdmin  # USER ADD
from .models import Reporter, Post
from wiki.admin import WikiInlineModelForm


class PostInline(admin.StackedInline):
    model = Post
    form = WikiInlineModelForm
    extra = 0


@admin.register(Reporter)
class ReporterAdmin(WikiModelAdmin):  # USER ADD
    inlines = [PostInline]


@admin.register(Post)
class PostAdmin(WikiModelAdmin):
    pass
