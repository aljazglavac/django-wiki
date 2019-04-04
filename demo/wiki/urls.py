from django.urls import path
from .views import anno_login

urlpatterns = [
    path('', anno_login),
]
