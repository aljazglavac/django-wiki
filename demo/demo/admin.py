from django.contrib import admin
from wiki.admin import WikiModelAdmin, WikiInlineModelForm
from .models import Book, Author


class BookInline(admin.StackedInline):
    model = Book
    form = WikiInlineModelForm
    extra = 0


@admin.register(Author)
class AuthorAdmin(WikiModelAdmin):
    inlines = [BookInline]


@admin.register(Book)
class BookAdmin(WikiModelAdmin):
    pass
