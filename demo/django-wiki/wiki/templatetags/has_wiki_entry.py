from django import template
from django.contrib.contenttypes.models import ContentType
from wiki.support_functions import obj_model_from_name

register = template.Library()


@register.filter(name='has_wiki_entry')
def has_wiki_entry(path):
    path = path.split('/')
    try:
        model_name = path[-4]
        model = obj_model_from_name(model_name)
    except:
        return False
    try:
        p_id = int(path[-3])
    except:
        return False
    return model.objects.exclude(pk=p_id).filter(wiki_id=p_id).exists()
