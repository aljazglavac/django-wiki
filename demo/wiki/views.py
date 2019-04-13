from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, F
from django.contrib.auth.models import User
from django.contrib import auth

SYS_DEF = [
    'log entry', 'permission', 'group', 'user', 'content type', 'session'
]


def anno_login(request):
    try:
        model = request.path.split('/')[2]
        anno = User.objects.get(username="ANNO-" + model)
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


def list_of_models():
    all_content = ContentType.objects.all()
    return [c.model_class() for c in all_content if str(c) not in SYS_DEF]


def get_wiki_entries(request):
    models = list_of_models()
    is_not_wiki = (~Q(pk=F("wiki_id")) | Q(wiki_id__isnull=True))
    all_model_wikis = []

    for model in models:
        if model is None:
            continue
        for wiki in model.objects.filter(is_not_wiki).distinct():
            change_link = "<a href='/admin/{}/{}/{}/change/'>{} in {}</a><br>".format(
                wiki._meta.app_label, model.__name__.lower(), wiki.pk,
                str(wiki), model.__name__)
            all_model_wikis.extend(change_link)

    if len(all_model_wikis) == 0:
        msg = "No new entry suggestions need to be reviewed. "
    else:
        msg = "You need to accept or reject the following entry suggestions. "

    json_wiki = {
        "message": msg,
        "wikis": all_model_wikis,
    }

    return JsonResponse(json_wiki, safe=False)
