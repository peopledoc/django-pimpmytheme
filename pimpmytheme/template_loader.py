import os
from django.template.loaders.app_directories import Loader
from django.utils._os import safe_join
from django.conf import settings
from .utils import get_lookup_class
BASE_FOLDER = settings.PIMPMYTHEME_FOLDER
project_name = settings.SETTINGS_MODULE.split(".")[0]


class Loader(Loader):
    is_usable = True

    def get_template_sources(self, template_name, template_dirs=None):

        lookup = get_lookup_class().objects.get_current()

        # maybe we do not have current lookup so we just do not try to handle
        # template dir now
        if not lookup:
            return []

        if not template_dirs:
            template_dir = os.path.join(
                BASE_FOLDER,
                project_name,
                getattr(lookup,
                        settings.CUSTOM_THEME_LOOKUP_ATTR),
                'templates')

        try:
            return [safe_join(template_dir, template_name)]
        except UnicodeDecodeError:
            # The template dir name was a bytestring that wasn't
            # valid UTF-8.
            raise
        except ValueError:
            # The joined path was located outside of template_dir.
            pass
