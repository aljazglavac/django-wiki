from django.contrib import admin
from django.contrib.auth.models import Group
from django.forms.models import model_to_dict


admin.site.index_template = 'wiki/admin/index.html'


class WikiModelAdmin(admin.ModelAdmin):
    readonly_fields = ('wiki_id', )
    change_form_template = 'wiki/custom_change_form.html'

    def is_wiki(self, obj):
        return obj.pk != obj.wiki_id or obj.wiki_id is None

    def save_model(self, request, obj, form, change):
        try:
            user_group = Group.objects.filter(user=request.user)[0].name
        except:
            user_group = ''
        if 'ANNO' in user_group:
            is_wiki = obj.pk != obj.wiki_id or obj.wiki_id == None
            if change and not is_wiki:
                copy_of_obj = dict(model_to_dict(obj))
                copy_of_obj['id'] = None
                wiki = type(obj)(**copy_of_obj)
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

    def save_formset(self, request, form, formset, change):
        try:
            user_group = Group.objects.filter(user=request.user)[0].name
        except:
            user_group = ''
        instances = formset.save(commit=False)
        for instance in instances:
            if 'ANNO' in user_group:
                wiki_parent_id = request.session['TODO']
                wiki_parent = type(obj).objects.get(pk=int(wiki_parent_id))
                is_wiki = instance.pk != instance.wiki_id or instance.wiki_id == None
                if change and not is_wiki:
                    copy_of_obj = dict(model_to_dict(instance))
                    copy_of_obj['wiki_id'] = copy_of_obj['id']
                    copy_of_obj['id'] = None
                    copy_of_obj['TODO'] = wiki_parent
                    wiki = type(obj)(**copy_of_obj)
                    wiki.save()
                elif change and is_wiki:
                    instance.poi = wiki_parent
                    instance.save()
                else:
                    instance.wiki_id = None
                    instance.poi = wiki_parent
                    instance.save()
            else:
                instance.save()
                instance.wiki_id = instance.pk
                instance.save(update_fields=["wiki_id"])