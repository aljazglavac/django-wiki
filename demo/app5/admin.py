from django.contrib import admin
from wiki.admin import WikiModelAdmin, WikiInlineModelForm
from .models import Knjiga, Oseba 


class KnjigaInline(admin.StackedInline):
    model = Knjiga 
    form = WikiInlineModelForm
    extra = 0
    readonly_fields = ["wiki_id"]


@admin.register(Oseba)
class OsebaAdmin(WikiModelAdmin):
    inlines = [KnjigaInline]


@admin.register(Knjiga)
class KnjigaAdmin(WikiModelAdmin):
    pass
