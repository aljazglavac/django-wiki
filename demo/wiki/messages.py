from django.contrib import messages
from django.utils.html import format_html
from .support_functions import link_to_change_obj


def accept_message_handler(request, obj):
    messages.add_message(
        request, messages.SUCCESS,
        format_html(('Successfully accepted suggestion. %(link)s') %
                    {'link': link_to_change_obj(obj, 'See it here. ', '')}))


def reject_message_handler(request, obj):
    messages.add_message(request, messages.SUCCESS,
                         'You have rejecred a suggestion.')


def save_message_handler(request, obj):
    messages.add_message(
        request, messages.SUCCESS,
        format_html(('Successfully saved suggestion. %(link)s') %
                    {'link': link_to_change_obj(obj, 'See it here. ', '')}))


def submit_message_handler(request, obj):
    messages.add_message(
        request, messages.SUCCESS,
        format_html(('Successfully submited suggestion. %(link)s') %
                    {'link': link_to_change_obj(obj, "See it here. ", "")}))
