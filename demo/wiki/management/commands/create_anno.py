import sys
from django.contrib.auth.models import User, Group, Permission
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from wiki.support_functions import list_of_models

GROUP = 'ANNO'

PERMISSIONS = [
    'add',
    'change',
    'view',
]


class Command(BaseCommand):
    help = 'Create anonymous user and anonymous group.'

    def add_arguments(self, parser):

        if len(sys.argv) <= 2:
            self.stdout.write("Please specify model/s for annoymous user.")
            models = list_of_models()
            groups = [str(g) for g in Group.objects.all()]
            self.stdout.write("Available models:")
            for model in models:
                name = model.__name__.lower()
                exist = '*' if Group.objects.filter(name__icontains=name).exists() else ''
                self.stdout.write("\t{}{}".format(name, exist))
            self.stdout.write("already created => *")
            exit()

        parser.add_argument('model', nargs='+', type=str)

    def handle(self, *args, **options):

        anno_group_all, created = Group.objects.get_or_create(name=GROUP)

        try:
            annouser = User.objects.get(username='ANNO')
            self.stdout.write("User ANNO already exists.")
        except:
            self.stdout.write("Creating anonymous user with user name: ANNO.")
            annouser = User(username='ANNO')
            annouser.is_staff = True
            annouser.save()
            pass


        for model in options['model']:

            try:
                ContentType.objects.get(model=model).model_class()
                self.stdout.write(
                    "Model {} found in database.".format(model))
            except:
                self.stdout.write(
                    "Wrong model! ({}) \nExiting.".format(model))
                return

            anno_group, created = \
                Group.objects.get_or_create(name='ANNO_GROUP_'+model)

            self.stdout.write(
                "Creating ANNO group for model {}.".format(model))
            for permission in PERMISSIONS:
                codename = '{}_{}'.format(permission, model)
                permission = Permission.objects.get(codename=codename)
                anno_group.permissions.add(permission)
                anno_group_all.permissions.add(permission)

            try:
                user = User.objects.get(username='ANNO-'+model)
                self.stdout.write(
                    "User ANNO for {} already exists.".format(model))
            except:
                self.stdout.write(
                    "Creating anonymous user with user name: ANNO-{}.".format(model))
                user = User(username='ANNO-'+model)
                user.is_staff = True
                user.save()
                pass

            anno_group.user_set.add(user)


        anno_group_all.user_set.add(annouser)

        self.stdout.write("Created anonymous user successfully.")
