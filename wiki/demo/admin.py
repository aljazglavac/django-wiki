from django.contrib.auth.models import Group
from django.forms.models import model_to_dict
from django.contrib import admin
from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'pub_on', 'pub_by')
    readonly_fields = ('wiki_id',)

    def save_model(self, request, obj, form, change):
        try:
            user_group = Group.objects.filter(user=request.user)[0].name
        except:
            user_group = None
        if user_group == 'ANNO':
            is_wiki = obj.pk != obj.wiki_id or obj.wiki_id == None
            if change and not is_wiki:
                copy_of_obj = dict(model_to_dict(obj))
                copy_of_obj['id'] = None
                wiki = Article(**copy_of_obj)
                wiki.save()
            elif change and is_wiki:
                obj.save()
            else:
                obj.wiki_id = None
                obj.save()
        else:
            obj.save()
            obj.wiki_id = obj.pk
            obj.save(update_fields=["wiki_id"])
