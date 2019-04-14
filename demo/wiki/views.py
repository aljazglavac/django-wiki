from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, F
from django.contrib.auth.models import User
from django.contrib import auth
from .support_functions import model_has_relation, link_to_change_obj, list_of_models
from .options import SYS_DEF

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


def get_wiki_entries(request):
    models = list_of_models()
    is_not_wiki = (~Q(pk=F("wiki_id")) | Q(wiki_id__isnull=True))
    all_model_wikis = []

    for model in models:
        if model is None:
            continue
        if model_has_relation(model):
            continue
        for wiki in model.objects.filter(is_not_wiki).distinct():
            text = "{} in {}".format(str(wiki), model.__name__)
            change_link = link_to_change_obj(wiki, text)
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
