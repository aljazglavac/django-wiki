from django.contrib import admin
from django.contrib.auth.models import Group
from django.forms.models import model_to_dict
from django.db.models import ForeignKey, OneToOneField
from django.forms.models import ModelForm
from django.shortcuts import redirect
import app3.models as m

admin.site.index_template = 'wiki/admin/index.html'

do_not_update = set(['id', 'wiki_id'])


class WikiInlineModelForm(ModelForm):
    def has_changed(self):
        return True


class WikiModelAdmin(admin.ModelAdmin):
    readonly_fields = ('wiki_id', )

    change_form_template = 'wiki/custom_change_form.html'

    def is_wiki(self, obj):
        return obj.pk != obj.wiki_id or obj.wiki_id is None

    def obj_has_foreignkey(self, obj):
        dict_obj = dict(model_to_dict(obj))
        for key, value in dict_obj.items():
            field_object = type(obj)._meta.get_field(key)
            if isinstance(field_object, ForeignKey) and not isinstance(
                    field_object, OneToOneField):
                return True
        return False

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

    def message_user(self, *args):
        pass

    def handle_save(self, request, obj):
        try:
            user_group = Group.objects.filter(user=request.user)[0].name
        except:
            user_group = ''
        if 'ANNO' in user_group:
            is_wiki = ( obj.pk != obj.wiki_id ) \
              or ( obj.wiki_id == None and obj.pk != None )
            is_new = obj.pk == None
            has_foreignkey = self.obj_has_foreignkey(obj)

            if has_foreignkey:
                wiki_parent_id = request.session['parent']
                parent_model = self.get_model_of_foreignkey_field(obj)
                wiki_parent = parent_model.objects.get(pk=int(wiki_parent_id))
                parent_field = self.get_foreignkey_field_name(obj)

            if is_new:
                obj.wiki_id = None
                obj.save()
            elif is_wiki:
                obj.save()
            elif not is_wiki:
                copy_of_obj = dict(model_to_dict(obj))
                copy_of_obj['wiki_id'] = copy_of_obj['id']
                copy_of_obj['id'] = None
                if has_foreignkey:
                    copy_of_obj[parent_field] = wiki_parent
                obj = type(obj)(**copy_of_obj)
                obj.save()

            if not has_foreignkey:
                request.session['parent'] = obj.pk
        else:
            obj.save()
            obj.wiki_id = obj.pk
            obj.save(update_fields=["wiki_id"])

    def handle_accept(self, request, obj):
        if obj.wiki_id is None:
            obj.wiki_id = obj.pk
            obj.save()
            return

        has_foreignkey = self.obj_has_foreignkey(obj)
        if has_foreignkey:
            foreignkey_name = self.get_foreignkey_field_name(obj)
            do_not_update.add(foreignkey_name)

        parent = type(obj).objects.get(pk=obj.wiki_id)
        wiki_dict = dict(model_to_dict(obj))

        for field_name, value in wiki_dict.items():
            if field_name not in do_not_update:
                setattr(parent, field_name, value)

        setattr(parent, 'wiki_id', parent.pk)

        if not has_foreignkey:
            request.session['parent'] = parent.pk
        else:
            foreignkey_model = self.get_model_of_foreignkey_field(parent)
            foreignkey_obj = foreignkey_model.objects.get(
                pk=int(request.session['parent']))
            setattr(parent, foreignkey_name, foreignkey_obj)

        parent.save()
        obj.delete()

    def handle_reject(self, obj):
        obj.delete()

    def save_model(self, request, obj, form, change):
        if '_accept' in request.POST:
            self.handle_accept(request, obj)
        elif '_reject' in request.POST:
            self.handle_reject(obj)
        elif '_save' in request.POST:
            self.handle_save(request, obj)
        return redirect('/admin/')

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if '_accept' in request.POST:
                self.handle_accept(request, instance)
            elif '_reject' in request.POST:
                self.handle_reject(i)
            elif '_save' in request.POST:
                self.handle_save(request, instance)
        return redirect('/admin/')
