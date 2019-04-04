from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import auth


def anno_login(request):
    try:
        anno = User.objects.get(username="ANNO")
    except User.DoesNotExist:
        return redirect('/admin/login')
    auth.login(request, anno)
    return redirect('/admin/')

