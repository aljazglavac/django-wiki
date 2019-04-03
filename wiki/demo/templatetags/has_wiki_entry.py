from django import template
import demo.models as m

register = template.Library()

@register.filter(name='has_wiki_entry')
def has_wiki_entry(path):
    try:
        p_id = int(path.split('/')[-3])
    except: return False
    return m.Article.objects.exclude(pk=p_id).filter(wiki_id=p_id).exists()

