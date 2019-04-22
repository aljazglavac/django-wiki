import sys
from django.contrib.auth.models import User, Group, Permission
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from wiki.support_functions import list_of_models
from wiki.options import PERMISSIONS


class Command(BaseCommand):
    help = 'Create or list admin and anno groups.'

    def list_all_models(self):
        self.stdout.write("List of all models:")
        for model in list_of_models():
            self.stdout.write("\t{}".format(model.__name__))

        self.stdout.write("")
        self.stdout.write("Models with admin:")
        groups = Group.objects.all()
        for group in groups.filter(name__icontains='ADMIN'):
            if group.name != 'ADMIN':
                self.stdout.write("\t" + group.name.split('_')[2].capitalize())

        self.stdout.write("")
        self.stdout.write("Models with anno:")
        for group in groups.filter(name__icontains='ANNO'):
            if group.name != 'ANNO':
                self.stdout.write("\t" + group.name.split('_')[2].capitalize())

        exit()

    def list_models_info(self, model):
        perms = []
        for group in Group.objects.filter(name__icontains=model.lower()):
            perms.append(group.name.split('_')[0].lower())
        if len(perms) > 0:
            self.stdout.write("{} has {}.".format(model.capitalize(),
                                                  ', '.join(perms)))
        else:
            self.stdout.write("Wrong model ({}).".format(model))
        exit()

    def create_top_level_admin(self):
        username = 'wikiadmin'
        try:
            user = User.objects.get(username=username)
            self.stdout.write("User {} already exists.".format(username))
        except:
            self.stdout.write(
                "Creating wiki admin user with user name: {} and password: {}."
                .format(username, username))
            user = User(username=username)
            user.set_password(username)
            user.is_staff = True
            user.is_superuser = True
            user.save()
        exit()

    def create_top_level_anno(self):
        GROUP = 'ANNO'
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
        for model in list_of_models():
            self.stdout.write("Creating {} group for model {}.".format(
                GROUP.lower(), model.__name__))
            for permission in PERMISSIONS:
                codename = '{}_{}'.format(permission, model.__name__.lower())
                permission = Permission.objects.get(codename=codename)
                group_all.permissions.add(permission)
        self.stdout.write("Adding ANNO user to all ANNO groups.")
        group_all.user_set.add(user)
        exit()

    def add_arguments(self, parser):

        print(sys.argv)
        if len(sys.argv) == 2:
            self.stdout.write(
                "Please specify if you want to create or list admin or annoymous user."
            )
            self.stdout.write("Usage:")
            self.stdout.write("\t./manage.py wiki create|list")
            exit()
        elif len(sys.argv) == 3:
            control = sys.argv[2]
            if control == 'list':
                self.list_all_models()
            elif control == 'create':
                self.stdout.write("Do you want to create admin or anno user?")
                self.stdout.write("Usage:")
                self.stdout.write("\t./manage.py wiki create admin|anno")
            elif control == 'user':
                self.stdout.write(
                    "Creating top level annonimous and admin user")
                self.create_top_level_admin()
                self.create_top_level_anno()
            else:
                self.stdout.write("Wrong operation.")
                self.stdout.write("Usage:")
                self.stdout.write("\t./manage.py wiki create|list")
            exit()
        elif len(sys.argv) == 4:
            control = sys.argv[2]
            operation = sys.argv[3]
            if operation in ['admin', 'anno'] and control == 'create':
                self.stdout.write("Specify a model.")
                self.stdout.write("List all models with:")
                self.stdout.write("\t ./manage.py wiki list")
                exit()
            elif operation not in ['admin', 'anno'] and control == 'list':
                models = sys.argv[3:]
                for model in models:
                    self.list_models_info(model)
            exit()

        parser.add_argument('args', nargs='+', type=str)

    def handle(self, *args, **options):

        GROUP = args[2].upper()
        MODELS = args[2:]
        print(GROUP, MODELS)

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

        self.stdout.write("Created {} user successfully.".format(
            GROUP.lower()))
