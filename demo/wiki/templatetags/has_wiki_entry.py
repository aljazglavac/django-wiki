from django import template
from django.contrib.contenttypes.models import ContentType

register = template.Library()

@register.filter(name='has_wiki_entry')
def has_wiki_entry(path):
    try:
        model_str = path.split('/')[-4]
        ct = ContentType.objects.get(model=model_str)
        model = ct.model_class()
    except: return False
    try:
        p_id = int(path.split('/')[-3])
    except: return False
    return model.objects.exclude(pk=p_id).filter(wiki_id=p_id).exists()
