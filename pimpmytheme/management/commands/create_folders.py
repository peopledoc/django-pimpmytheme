from django.core.management import call_command
from django.core.management.base import BaseCommand
from pimpmytheme.folder_management import create_folders
from pimpmytheme.utils import get_lookup_class


class Command(BaseCommand):

    def handle(self, *args, **options):
        objects = get_lookup_class().objects.all()

        for elem in objects:
            create_folders(elem)
        call_command('collectstatic', interactive=False)
