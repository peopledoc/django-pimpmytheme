import importlib
from django.core.management.base import BaseCommand
from django.conf import settings
from custom_theme.folder_management import create_folders


class Command(BaseCommand):

    def handle(self, *args, **options):
        module_string = '.'.join(
            settings.CUSTOM_THEME_LOOKUP_OBJECT.split('.')[:-1])
        klass_string = settings.CUSTOM_THEME_LOOKUP_OBJECT.split('.')[-1]
        module = importlib.import_module(
            module_string, [klass_string])
        klass = getattr(module, klass_string)
        objects = klass.objects.all()
        for elem in objects:
            create_folders(elem)
