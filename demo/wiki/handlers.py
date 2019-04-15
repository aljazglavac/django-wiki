from django.forms.models import model_to_dict
from .support_functions import (model_has_relation, get_foreignkey_field_name,
                                get_model_of_foreignkey_field, is_user_anno,
                                obj_status, set_relation_field)
from .options import DO_NOT_UPDATE


def handle_save(request, obj):
    obj.save()
    if not is_user_anno(request.user):
        setattr(obj, 'wiki_id', obj.pk)
        obj.save(update_fields=['wiki_id'])


def handle_submit(request, obj):
    is_wiki, is_new, has_wiki, has_foreignkey = obj_status(obj)

    if has_foreignkey:
        parent_model = get_model_of_foreignkey_field(obj)
        parent_field = get_foreignkey_field_name(obj)

        try:
            wiki_parent_id = request.session['parent']
            wiki_parent = parent_model.objects.get(pk=int(wiki_parent_id))
        except:
            has_foreignkey = False
            pass

    if not is_wiki:
        setattr(obj, 'id', None)
        if has_foreignkey:
            setattr(obj, parent_field, wiki_parent)

    obj.save()

    if not has_foreignkey:
        request.session['parent'] = obj.pk

    return obj


def handle_accept(request, obj):
    is_wiki, is_new, has_wiki, has_foreignkey = obj_status(obj)

    if not is_wiki:
        if not has_foreignkey:
            request.session['parent'] = obj.pk
        return obj

    if not has_wiki:
        setattr(obj, 'wiki_id', obj.pk)
        if has_foreignkey:
            r_field, r_obj = set_relation_field(request, obj)
            setattr(obj, related_field, related_obj)

        obj.save()
        return obj

    if has_foreignkey:
        foreignkey_name = get_foreignkey_field_name(obj)
        DO_NOT_UPDATE.add(foreignkey_name)

    parent = type(obj).objects.get(pk=obj.wiki_id)
    wiki_dict = dict(model_to_dict(obj))

    for field_name, value in wiki_dict.items():
        if field_name not in DO_NOT_UPDATE:
            setattr(parent, field_name, value)

    setattr(parent, 'wiki_id', parent.pk)

    if not has_foreignkey:
        request.session['parent'] = parent.pk
    else:
        r_field, r_obj = set_relation_field(request, parent)
        setattr(parent, r_field, r_obj)

    parent.save()
    obj.delete()

    return parent


def handle_reject(obj):
    obj.delete()
