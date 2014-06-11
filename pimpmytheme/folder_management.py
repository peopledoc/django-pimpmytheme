import os
from django.utils.importlib import import_module
from django.conf import settings
from django.core.management import call_command

mod = import_module("pimpmytheme")
project_name = settings.SETTINGS_MODULE.split(".")[0]


def create_folders(instance):
    curent_dir = os.path.join(os.path.dirname(mod.__file__), project_name,
                              instance.name, "static", "css")
    if not os.path.exists(curent_dir):
        os.makedirs(curent_dir)
    custom_less = os.path.join(curent_dir, "custom.less")
    if not os.path.exists(custom_less):
        f = open(custom_less, "w")
        f.close()
    call_command('collectstatic', interactive=False)
