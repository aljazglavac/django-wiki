from django.contrib import messages
from django.utils.html import format_html
from .support_functions import link_to_change_obj


def accept_message_handler(request, obj):
    messages.add_message(
        request, messages.SUCCESS,
        format_html(('Successfully accepted %(link) suggestion. ') %
                    {'link': link_to_change_obj(obj)}))


def reject_message_handler(request, obj):
    messages.add_message(request, messages.SUCCESS,
                         default_message.format('rejected a suggestion'))


def save_message_handler(request, obj):
    messages.add_message(
        request, messages.SUCCESS,
        format_html(('Successfully saved %(link) suggestion. ') %
                    {'link': link_to_change_obj(obj)}))


def submit_message_handler(request, obj):
    messages.add_message(
        request, messages.SUCCESS,
        format_html(('Successfully submited %(link) suggestion. ') %
                    {'link': link_to_change_obj(obj)}))
