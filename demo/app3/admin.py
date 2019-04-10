from django.contrib import admin
from wiki.admin import WikiModelAdmin  # USER ADD
from .models import Book, Author


class BookInline(admin.StackedInline):
    model = Book
    extra = 0
    readonly_fields = ["wiki_id"]


@admin.register(Author)
class AuthorAdmin(WikiModelAdmin):
    inlines = [BookInline]
    readonly_fields = ["wiki_id"]


@admin.register(Book)
class BookAdmin(WikiModelAdmin):
    readonly_fields = ["wiki_id"]
