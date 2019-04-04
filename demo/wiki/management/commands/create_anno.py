import sys
from django.contrib.auth.models import User, Group, Permission
from django.core.management.base import BaseCommand
from django.apps import apps

GROUP = 'ANNO'

PERMISSIONS = [
    'add',
    'change',
    'view',
]


class Command(BaseCommand):
    help = 'Create anonymous user and anonymous group.'

    def add_arguments(self, parser):

        if len(sys.argv) == 2:
            self.stdout.write("Please specify model for annoymous user.")
            return

        parser.add_argument('model', nargs='+', type=str)

    def handle(self, *args, **options):

        anno_group, created = Group.objects.get_or_create(name=GROUP)

        for model in options['model']:
            self.stdout.write(
                "Creating ANNO group for model {}.".format(model))
            for permission in PERMISSIONS:
                codename = '{}_{}'.format(permission, model)
                permission = Permission.objects.get(codename=codename)
                anno_group.permissions.add(permission)

        try:
            User.objects.get(username='ANNO')
            self.stdout.write("User ANNO already exists.")
            return
        except:
            self.stdout.write("Creating anonymous user with user name: ANNO.")
            pass

        user = User(username='ANNO')
        user.is_staff = True
        user.save()

        try:
            ANNO_perm_group = Group.objects.get(name='ANNO')
        except:
            self.stdout.write("Creation faild. Could not find group ANNO.")
            self.stdout.write(
                "Please run 'python manage.py create_groups' first.")
            return

        ANNO_perm_group.user_set.add(user)

        self.stdout.write("Created anonymous user successfully.")
