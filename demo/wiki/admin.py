from django.contrib import admin
from django.contrib.auth.models import Group
from django.forms.models import model_to_dict
from django.db.models import ForeignKey

admin.site.index_template = 'wiki/admin/index.html'


class WikiModelAdmin(admin.ModelAdmin):
    readonly_fields = ('wiki_id', )

    #change_form_template = 'wiki/custom_change_form.html'

    def is_wiki(self, obj):
        return obj.pk != obj.wiki_id or obj.wiki_id is None

    def get_foreignkey_field_name(self, obj):
        dict_obj = dict(model_to_dict(obj))
        for key, value in dict_obj.items():
            field_object = type(obj)._meta.get_field(key)
            if isinstance(field_object, ForeignKey):
                return key
        return None

    def get_model_of_foreignkey_field(self, obj):
        dict_obj = dict(model_to_dict(obj))
        for key, value in dict_obj.items():
            field_object = type(obj)._meta.get_field(key)
            if isinstance(field_object, ForeignKey):
                return type(getattr(obj, key))
        return None

    def save_model(self, request, obj, form, change):
        try:
            user_group = Group.objects.filter(user=request.user)[0].name
        except:
            user_group = ''
        if 'ANNO' in user_group:
            is_wiki = ( instance.pk != instance.wiki_id ) \
                      or ( instance.wiki_id == None and instance.pk != None )
            is_new = instance.pk == None
            if not is_wiki:
                copy_of_obj = dict(model_to_dict(obj))
                copy_of_obj['id'] = None
                obj = type(obj)(**copy_of_obj)
                obj.save()
            elif is_wiki:
                obj.save()
            elif is_new:
                obj.wiki_id = None
                obj.save()
            request.session['parent'] = obj.pk
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
                wiki_parent_id = request.session['parent']
                parent_model = self.get_model_of_foreignkey_field(instance)
                wiki_parent = parent_model.objects.get(pk=int(wiki_parent_id))
                parent = self.get_foreignkey_field_name(instance)
                is_wiki = ( instance.pk != instance.wiki_id ) \
                          or ( instance.wiki_id == None and instance.pk != None )
                is_new = instance.pk == None
                if not is_wiki:
                    copy_of_obj = dict(model_to_dict(instance))
                    copy_of_obj['wiki_id'] = copy_of_obj['id']
                    copy_of_obj['id'] = None
                    copy_of_obj[parent] = wiki_parent
                    wiki = type(instance)(**copy_of_obj)
                    wiki.save()
                elif is_wiki:
                    instance.save()
                elif is_new:
                    instance.wiki_id = None
                    instance.save()
            else:
                instance.save()
                instance.wiki_id = instance.pk
                instance.save(update_fields=["wiki_id"])
