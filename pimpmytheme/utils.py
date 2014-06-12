import importlib
from django.conf import settings


def get_lookup_class():
    module_string = '.'.join(
        settings.CUSTOM_THEME_LOOKUP_OBJECT.split('.')[:-1])
    klass_string = settings.CUSTOM_THEME_LOOKUP_OBJECT.split('.')[-1]
    klass = getattr(importlib.import_module(module_string), klass_string)
    return klass
