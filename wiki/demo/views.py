from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.shortcuts import render


def anno_login(request):
    try:
        anno = User.objects.get(username="ANNO")
    except User.DoesNotExist:
        return redirect('/admin/')
    auth.login(request, anno)
    return redirect('/admin/demo/article')
