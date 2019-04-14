from django.forms.models import model_to_dict
from django.contrib.contenttypes.models import ContentType
from django.db.models import ForeignKey, OneToOneField
from .options import SYS_DEF


def model_has_relation(model):
    fields = model._meta.get_fields()
    for field in fields:
        if isinstance(field, ForeignKey):
            return True
    return False


def obj_has_foreignkey(obj):
    dict_obj = dict(model_to_dict(obj))
    for key, value in dict_obj.items():
        field_object = type(obj)._meta.get_field(key)
        if isinstance(field_object, ForeignKey) and not isinstance(
                field_object, OneToOneField):
            return True
    return False


def get_foreignkey_field_name(obj):
    dict_obj = dict(model_to_dict(obj))
    for key, value in dict_obj.items():
        field_object = type(obj)._meta.get_field(key)
        if isinstance(field_object, ForeignKey):
            return key
    return None


def get_model_of_foreignkey_field(obj):
    dict_obj = dict(model_to_dict(obj))
    for key, value in dict_obj.items():
        field_object = type(obj)._meta.get_field(key)
        if isinstance(field_object, ForeignKey):
            return type(getattr(obj, key))
    return None


def is_obj_wiki(obj):
    return ( obj.pk != obj.wiki_id ) \
          or ( obj.wiki_id == None and obj.pk != None )


def is_obj_new(obj):
    return obj.pk == None


def link_to_change_obj(obj, text):
    model = type(obj)
    change_link = "<a href='/admin/{}/{}/{}/change/'>{}</a><br>".format(
        obj._meta.app_label, model.__name__.lower(), obj.pk, text)
    return change_link


def list_of_models():
    all_content = ContentType.objects.all()
    return [c.model_class() for c in all_content if str(c) not in SYS_DEF]
