from django.contrib import admin
from django.forms.models import ModelForm
from django.shortcuts import redirect
from django.db.models import ForeignKey
from .messages import (accept_message_handler, save_message_handler,
                       submit_message_handler, reject_message_handler)
from .handlers import (handle_save, handle_submit, handle_accept,
                       handle_reject)
from .support_functions import (clean_request_sesstion, obj_model_from_name,
                                )

admin.site.index_template = 'wiki/admin/index.html'


class WikiInlineModelForm(ModelForm):
    def has_changed(self):
        return True


class WikiModelAdmin(admin.ModelAdmin):

    change_form_template = 'wiki/custom_change_form.html'

    def message_user(self, *args, **kwargs):
        clean_request_sesstion(args[0], 'parent')
        pass

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        field_name = db_field.related_query_name()
        model = obj_model_from_name(field_name)
        fields = model._meta.get_fields()
        for f in fields:
            if isinstance(f, ForeignKey):
                kwargs["queryset"] = f.related_model.objects.valid()
                break
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if '_accept' in request.POST:
            sug = handle_accept(request, obj)
            accept_message_handler(request, sug)
        elif '_reject' in request.POST:
            handle_reject(obj)
            reject_message_handler(request, obj)
        elif '_save' in request.POST:
            handle_save(request, obj)
            save_message_handler(request, obj)
        elif '_submit' in request.POST:
            sug = handle_submit(request, obj)
            submit_message_handler(request, sug)
        return redirect('/admin/')

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if '_accept' in request.POST:
                handle_accept(request, instance)
            elif '_reject' in request.POST:
                handle_reject(instance)
            elif '_save' in request.POST:
                handle_save(request, instance)
            elif '_submit' in request.POST:
                handle_submit(request, instance)
        return redirect('/admin/')
