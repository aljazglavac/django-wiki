from django.contrib.contenttypes.models import ContentType
from django.urls import path
from .views import anno_login

urlpatterns = [
    path('', anno_login),
]


SYS_DEF = [
    'log entry', 'permission', 'group', 'user', 'content type', 'session'
]
all_content = ContentType.objects.all()
str_content = [str(c) for c in all_content if str(c) not in SYS_DEF]

extrapatterns = []
for model in str_content:
    extrapatterns.append(path(model, anno_login))

urlpatterns.extend(extrapatterns)
