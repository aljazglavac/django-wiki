import sys
from django.contrib.auth.models import User, Group, Permission
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from wiki.support_functions import list_of_models
from wiki.options import PERMISSIONS


class Command(BaseCommand):
    help = 'Create admin group for model. '

    def add_arguments(self, parser):

        if len(sys.argv) == 2:
            self.stdout.write(
                "Please specify if you want to create  admin or annoymous user."
            )
            self.stdout.write("Options:")
            self.stdout.write("\t*admin")
            self.stdout.write("\t*anno")
            exit()

        elif len(sys.argv) == 3:
            self.stdout.write("Please specify model. ")
            models = list_of_models()
            groups = [str(g) for g in Group.objects.all()]
            self.stdout.write("Available models:")
            for model in models:
                name = model.__name__.lower()
                exist = '*' if Group.objects.filter(
                    name__icontains=name).exists() else ''
                self.stdout.write("\t{}{}".format(name, exist))
            self.stdout.write("*: Already created. ")
            exit()

        parser.add_argument('args', nargs='+', type=str)

    def handle(self, *args, **options):

        GROUP = args[0].upper()
        MODELS = args[1:]

        group_all, created = Group.objects.get_or_create(name=GROUP)

        try:
            user = User.objects.get(username=GROUP)
            self.stdout.write("User {} already exists.".format(GROUP))
        except:
            self.stdout.write("Creating {} user with user name: {}.".format(
                GROUP.lower(), GROUP))
            user = User(username=GROUP)
            user.is_staff = True
            user.save()
            pass

        for model in MODELS:

            try:
                ContentType.objects.get(model=model).model_class()
                self.stdout.write("Model {} found in database.".format(model))
            except:
                self.stdout.write("Wrong model! ({}) \nExiting.".format(model))
                return

            group, created = \
                Group.objects.get_or_create(name=GROUP+'_GROUP_'+model)

            self.stdout.write("Creating {} group for model {}.".format(
                GROUP.lower(), model))
            for permission in PERMISSIONS:
                codename = '{}_{}'.format(permission, model)
                permission = Permission.objects.get(codename=codename)
                group.permissions.add(permission)
                group_all.permissions.add(permission)

            try:
                user = User.objects.get(username="{}-{}".format(GROUP, model))
                self.stdout.write("User {} for {} already exists.".format(
                    GROUP.lower(), model))
            except:
                self.stdout.write(
                    "Creating {} user with user name: {}-{}.".format(
                        GROUP.lower(), GROUP, model))
                user = User(username="{}-{}".format(GROUP, model))
                user.is_staff = True
                user.save()
                pass

            group.user_set.add(user)

        group_all.user_set.add(user)

        self.stdout.write("Created {} user successfully.".format(GROUP.lower()))
