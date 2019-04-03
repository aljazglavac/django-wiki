from django.contrib.auth.models import User, Group, Permission
from django.core.management.base import BaseCommand
from django.apps import apps

GROUP = 'ANNO'

PERMISSIONS = [
    'add',
    'change',
    'view',
]

APPS = [
    'demo',
]


def get_apps_models(user_apps):
    m = []
    for app in user_apps:
        m.extend([x for x in apps.all_models[app]])
    return m


class Command(BaseCommand):
    help = 'Create anonymous user and anonymous group.'

    def handle(self, *args, **kwargs):
        self.create_ANNO_group()
        self.create_ANNO_user()

    def create_ANNO_group(self, *args, **kwargs):
        anno_group, created = Group.objects.get_or_create(name=GROUP)
        MODELS = get_apps_models(APPS)

        if created:
            self.stdout.write("Creating ANNO group.")
            for model in MODELS:
                for permission in PERMISSIONS:
                    codename = '{}_{}'.format(permission, model)
                    permission = Permission.objects.get(codename=codename)
                    anno_group.permissions.add(permission)
        else:
            self.stdout.write("Group ANNO already exists.")

    def create_ANNO_user(self, *args, **kwargs):
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
