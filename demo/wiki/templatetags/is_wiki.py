from django import template
from django.contrib.contenttypes.models import ContentType
from wiki.support_functions import is_obj_wiki

register = template.Library()

@register.filter(name='is_wiki')
def is_wiki(path):
    try:
        model_str = path.split('/')[-4]
        ct = ContentType.objects.get(model=model_str)
        model = ct.model_class()
    except: return False
    try:
        p_id = int(path.split('/')[-3])
        return is_obj_wiki(model.objects.get(pk=p_id))
    except:
        return False
