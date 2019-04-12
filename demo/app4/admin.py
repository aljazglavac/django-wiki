from django.contrib import admin
from .models import Fish 
from wiki.admin import WikiModelAdmin # USER ADD

@admin.register(Fish)
class FishAdmin(WikiModelAdmin): # USER ADD
    list_display = ('fish_name',)
