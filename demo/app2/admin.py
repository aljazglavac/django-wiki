from django.contrib import admin
from wiki.admin import WikiModelAdmin  # USER ADD
from .models import Reporter, Post


class PostInline(admin.StackedInline):
    model = Post
    extra = 0
    readonly_fields = ["wiki_id"]


@admin.register(Reporter)
class ReporterAdmin(WikiModelAdmin):  # USER ADD
    inlines = [PostInline]
    readonly_fields = ["wiki_id"]


@admin.register(Post)
class PostAdmin(WikiModelAdmin):
    readonly_fields = ["wiki_id"]
