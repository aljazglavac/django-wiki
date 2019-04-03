from django import template
import core.models as m

register = template.Library()

@register.filter(name='is_wiki')
def is_wiki(path):
    try:
        p_id = int(path.split('/')[-3])
        p_wiki_id = m.Article.objects.get(pk=p_id).wiki_id
        return p_wiki_id != p_id or p_wiki_id == None
    except:
        return False

