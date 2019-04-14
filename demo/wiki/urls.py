from django.contrib.contenttypes.models import ContentType
from django.urls import path
from .views import anno_login, get_wiki_entries
from .support_functions import list_of_models

urlpatterns = [
    path('', anno_login),
    path('entries', get_wiki_entries),
]

try:
    extrapatterns = []
    for model in list_of_models():
        extrapatterns.append(path(model.__name__.lower(), anno_login))

    urlpatterns.extend(extrapatterns)
except:
    pass
