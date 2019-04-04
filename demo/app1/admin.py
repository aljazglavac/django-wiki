from django.contrib import admin
from wiki.admin import WikiModelAdmin # USER ADD
from .models import Person

@admin.register(Person)
class PersonAdmin(WikiModelAdmin): # USER ADD
    list_display = ('first_name', 'last_name')
