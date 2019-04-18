from django.contrib.contenttypes.models import ContentType
from django.urls import path
from .views import wiki_login, get_wiki_entries
from .support_functions import list_of_models

urlpatterns = [
    path('', wiki_login),
    path('entries', get_wiki_entries),
]

try:
    extrapatterns = []
    for model in list_of_models():
        extrapatterns.append(path(model.__name__.lower(), wiki_login))
        extrapatterns.append(path(model.__name__.lower()+'/admin', wiki_login))

    urlpatterns.extend(extrapatterns)
except:
    pass
