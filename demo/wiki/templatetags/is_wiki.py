from django import template
from django.contrib.contenttypes.models import ContentType

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
        p_wiki_id = model.objects.get(pk=p_id).wiki_id
        return p_wiki_id != p_id or p_wiki_id == None
    except:
        return False
