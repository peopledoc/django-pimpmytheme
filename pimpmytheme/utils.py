import importlib
from django.conf import settings


def get_lookup_class():
    mod_string, cls_string = settings.CUSTOM_THEME_LOOKUP_OBJECT.rsplit('.', 1)
    klass = getattr(importlib.import_module(mod_string), cls_string)
    return klass
