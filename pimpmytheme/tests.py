import os
import shutil
from django.test import TestCase
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management import call_command
project_name = settings.SETTINGS_MODULE.split(".")[0]
BASE_FOLDER = settings.PIMPMYTHEME_FOLDER


class SiteTestCase(TestCase):
    """
    Ensure that, when a site is added, the folders are created too
    """

    def test_folder_creation(self):
        Site.objects.create(name="something",
                            domain="something.com")
        call_command("create_folders")
        current_dir = os.path.join(BASE_FOLDER, project_name,
                                   "something", "static", "css")
        self.assertTrue(os.path.exists(current_dir))
        custom_less = os.path.join(current_dir, "custom.less")
        self.assertTrue(os.path.exists(custom_less))
        shutil.rmtree(os.path.join(BASE_FOLDER, project_name, "something"))
        self.assertFalse(os.path.exists(current_dir))
