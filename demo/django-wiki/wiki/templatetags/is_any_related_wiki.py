from django import template
from django.contrib.contenttypes.models import ContentType
from wiki.support_functions import obj_model_from_name, model_has_relation, get_foreignkey_field_name

register = template.Library()


@register.filter(name='is_any_related_wiki')
def is_any_related_wiki(path):
    try:
        path = path.split('/')
        model_name = path[-4]
        p_id = int(path[-3])
        model = obj_model_from_name(model_name)
        obj = model.objects.get(pk=p_id)
        related_fields = [
            f for f in model._meta.get_fields()
            if f.auto_created and not f.concrete
        ]
        if len(related_fields) != 1:
            return False
        related_field_name = related_fields[0].field.related_query_name()
        forward = related_fields[0].field.get_forward_related_filter(obj)
        related_model = obj_model_from_name(related_field_name)
        return related_model.objects.invalid().filter(**forward).exists()
    except:
        return False
