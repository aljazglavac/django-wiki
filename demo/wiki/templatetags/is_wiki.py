from django import template
from django.contrib.contenttypes.models import ContentType
from wiki.support_functions import is_obj_wiki, obj_model_from_name

register = template.Library()


@register.filter(name='is_wiki')
def is_wiki(path):
    path = path.split('/')
    try:
        model_name = path[-4]
        model = obj_model_from_name(model_name)
    except:
        return False
    try:
        p_id = int(path[-3])
        return is_obj_wiki(model.objects.get(pk=p_id))
    except:
        return False
