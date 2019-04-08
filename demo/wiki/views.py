from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import auth


def anno_login(request):
    try:
        model = request.path.split('/')[2]
        anno = User.objects.get(username="ANNO-"+model)
        auth.login(request, anno)
        return redirect('/admin/')
    except:
        try:
            anno = User.objects.get(username="ANNO")
        except User.DoesNotExist:
            return redirect('/admin/login')
        auth.login(request, anno)
        return redirect('/admin/')
    return redirect('/admin/login')

