from django.contrib import messages

default_success_message = 'Successfully {} suggestion'


def add_message_only_once(request, level, msg):
    if msg not in [m.message for m in messages.get_messages(request)]:
        messages.add_message(request, level, msg)


def accept_message_handler(request):
    messages.add_message(request, messages.SUCCESS,
                         default_success_message.format('accepted'))


def reject_message_handler(request):
    messages.add_message(request, messages.SUCCESS,
                         default_success_message.format('rejected'))


def save_message_handler(request):
    messages.add_message(request, messages.SUCCESS,
                         default_success_message.format('saved'))


def submit_message_handler(request):
    messages.add_message(request, messages.SUCCESS,
                         default_success_message.format('submited'))
