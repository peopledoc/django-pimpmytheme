import importlib
from django.db.models.signals import post_save
from django.dispatch import receiver
from .folder_management import create_folders
from django.conf import settings

module_string = '.'.join(
    settings.CUSTOM_THEME_LOOKUP_OBJECT.split('.')[:-1])
klass_string = settings.CUSTOM_THEME_LOOKUP_OBJECT.split('.')[-1]
klass = getattr(importlib.import_module(module_string), klass_string)


@receiver(post_save, sender=klass)
def my_handler(sender, instance, **kwargs):
    create_folders(instance)
