import os
import shutil
from django.test import TestCase
from django.conf import settings
from django.contrib.sites.models import Site

project_name = settings.SETTINGS_MODULE.split(".")[0]


class SiteTestCase(TestCase):
    """
    Ensure that, when a site is added, the folders are created too
    """

    def test_folder_creation(self):
        Site.objects.create(name="something",
                            domain="something.com")
        DIR = os.path.dirname(os.path.dirname(__file__))
        current_dir = os.path.join(DIR, "custom_theme", project_name,
                                   "something", "static", "css")
        self.assertTrue(os.path.exists(current_dir))
        custom_less = os.path.join(current_dir, "custom.less")
        self.assertTrue(os.path.exists(custom_less))
        shutil.rmtree(os.path.join(DIR, "custom_theme",
                                   project_name, "something"))
        self.assertFalse(os.path.exists(current_dir))
