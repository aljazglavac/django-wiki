from django.contrib import admin, messages
from django.contrib.auth.models import Group
from django.forms.models import model_to_dict, ModelForm
from django.db.models import ForeignKey, OneToOneField
from django.shortcuts import redirect
from .messages import (accept_message_handler, save_message_handler,
                       submit_message_handler, reject_message_handler)

admin.site.index_template = 'wiki/admin/index.html'

do_not_update = set(['id', 'wiki_id'])


def model_has_relation(model):
    fields = model._meta.get_fields()
    for field in fields:
        if isinstance(field, ForeignKey):
            return True
    return False

def obj_has_foreignkey(obj):
    dict_obj = dict(model_to_dict(obj))
    for key, value in dict_obj.items():
        field_object = type(obj)._meta.get_field(key)
        if isinstance(field_object, ForeignKey) and not isinstance(
                field_object, OneToOneField):
            return True
    return False


def get_foreignkey_field_name(obj):
    dict_obj = dict(model_to_dict(obj))
    for key, value in dict_obj.items():
        field_object = type(obj)._meta.get_field(key)
        if isinstance(field_object, ForeignKey):
            return key
    return None


def get_model_of_foreignkey_field(obj):
    dict_obj = dict(model_to_dict(obj))
    for key, value in dict_obj.items():
        field_object = type(obj)._meta.get_field(key)
        if isinstance(field_object, ForeignKey):
            return type(getattr(obj, key))
    return None

def is_obj_wiki(obj):
    return ( obj.pk != obj.wiki_id ) \
          or ( obj.wiki_id == None and obj.pk != None )

def is_obj_new(obj):
    return obj.pk == None

class WikiInlineModelForm(ModelForm):
    def has_changed(self):
        return True


class WikiModelAdmin(admin.ModelAdmin):
    readonly_fields = ('wiki_id', )

    change_form_template = 'wiki/custom_change_form.html'

    def message_user(self, *args):
        pass

    def handle_save(self, request, obj):
        try:
            user_group = Group.objects.filter(user=request.user)[0].name
        except:
            user_group = ''
        if 'ANNO' in user_group:
            submit_message_handler(request)
            is_wiki = is_obj_wiki(obj)
            is_new = is_obj_new(obj) 
            has_foreignkey = obj_has_foreignkey(obj)

            if has_foreignkey:
                wiki_parent_id = request.session['parent']
                parent_model = get_model_of_foreignkey_field(obj)
                wiki_parent = parent_model.objects.get(pk=int(wiki_parent_id))
                parent_field = get_foreignkey_field_name(obj)

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
            save_message_handler(request)

    def handle_accept(self, request, obj):
        accept_message_handler(request)
        if obj.wiki_id is None:
            obj.wiki_id = obj.pk
            obj.save()
            return

        has_foreignkey = obj_has_foreignkey(obj)
        if has_foreignkey:
            foreignkey_name = get_foreignkey_field_name(obj)
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
            foreignkey_model = get_model_of_foreignkey_field(parent)
            foreignkey_obj = foreignkey_model.objects.get(
                pk=int(request.session['parent']))
            setattr(parent, foreignkey_name, foreignkey_obj)

        parent.save()
        obj.delete()

    def handle_reject(self, request, obj):
        obj.delete()
        reject_message_handler(request)

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
                self.handle_reject(request, instance)
            elif '_save' in request.POST:
                self.handle_save(request, instance)
        return redirect('/admin/')
