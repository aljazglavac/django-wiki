from django.forms.models import model_to_dict
from .support_functions import (model_has_relation, obj_has_foreignkey,
                                get_foreignkey_field_name,
                                get_model_of_foreignkey_field, is_obj_wiki,
                                is_obj_new)

def handle_save(request, obj):
    obj.save()
    obj.wiki_id = obj.pk
    obj.save(update_fields=["wiki_id"])

def handle_submit(request, obj):
    is_wiki = is_obj_wiki(obj)
    is_new = is_obj_new(obj)
    has_foreignkey = obj_has_foreignkey(obj)

    if has_foreignkey:
        wiki_parent_id = request.session['parent']
        parent_model = get_model_of_foreignkey_field(obj)
        wiki_parent = parent_model.objects.get(pk=int(wiki_parent_id))
        parent_field = get_foreignkey_field_name(obj)

    if is_new:
        obj.wiki_id = None
        obj.save()
    elif is_wiki:
        obj.save()
    elif not is_wiki:
        copy_of_obj = dict(model_to_dict(obj))
        copy_of_obj['wiki_id'] = copy_of_obj['id']
        copy_of_obj['id'] = None
        if has_foreignkey:
            copy_of_obj[parent_field] = wiki_parent
        obj = type(obj)(**copy_of_obj)
        obj.save()

    if not has_foreignkey:
        request.session['parent'] = obj.pk

def handle_accept(request, obj):
    if obj.wiki_id is None:
        obj.wiki_id = obj.pk
        obj.save()
        return

    has_foreignkey = obj_has_foreignkey(obj)
    if has_foreignkey:
        foreignkey_name = get_foreignkey_field_name(obj)
        do_not_update.add(foreignkey_name)

    parent = type(obj).objects.get(pk=obj.wiki_id)
    wiki_dict = dict(model_to_dict(obj))

    for field_name, value in wiki_dict.items():
        if field_name not in do_not_update:
            setattr(parent, field_name, value)

    setattr(parent, 'wiki_id', parent.pk)

    if not has_foreignkey:
        request.session['parent'] = parent.pk
    else:
        foreignkey_model = get_model_of_foreignkey_field(parent)
        foreignkey_obj = foreignkey_model.objects.get(
            pk=int(request.session['parent']))
        setattr(parent, foreignkey_name, foreignkey_obj)

    parent.save()
    obj.delete()

def handle_reject(request, obj):
    obj.delete()
