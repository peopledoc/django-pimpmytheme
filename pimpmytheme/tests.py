import os
import shutil
from django.test import TestCase
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management import call_command
from django.core.management.base import CommandError

from pimpmytheme.management.commands import update_themefolder_from_git as ufg


project_name = settings.SETTINGS_MODULE.split(".")[0]
BASE_FOLDER = settings.PIMPMYTHEME_FOLDER


class SiteTestCase(TestCase):
    """
    Ensure that, when a site is added, the folders are created too
    """

    def tearDown(self):
        settings.PIMPMYTHEME_FOLDER = BASE_FOLDER

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

    def test_update_themefolder_from_git_command(self):
        # invalidate PIMPMYTHEME_FOLDER variable
        settings.PIMPMYTHEME_FOLDER = None

        # no repo settings
        self.assertRaisesRegexp(CommandError,
                                ufg.PIMPMYTHEME_FOLDER_SETTINGS_ERROR,
                                call_command,
                                'update_themefolder_from_git')

        # no repo settings
        self.assertRaisesRegexp(CommandError,
                                ufg.PIMPMYTHEME_GIT_REPOSITORY_SETTINGS_ERROR,
                                call_command,
                                'update_themefolder_from_git', folder='.')

        # dummy repo
        try:
            import git
            self.assertRaisesRegexp(git.GitCommandError,
                                    'returned exit status 1',
                                    call_command,
                                    'update_themefolder_from_git', folder='.',
                                    git_repository='dummy')
        except ImportError:
            self.assertRaisesRegexp(CommandError,
                                    ufg.GIT_IMPORT_ERROR,
                                    call_command,
                                    'update_themefolder_from_git', folder='.',
                                    git_repository='dummy')
