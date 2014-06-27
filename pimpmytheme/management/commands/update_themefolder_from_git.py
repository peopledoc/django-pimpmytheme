# -*- coding: utf-8 -*-
import os

from optparse import make_option

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from django.conf import settings


PIMPMYTHEME_FOLDER_SETTINGS_ERROR = """To target the expected theme folder you
need to speficy it in your current django settings with the PIMPMYTHEME_FOLDER
variable or in your command line as bellow:

    python manage.py update_themefolder_from_git --folder <~/some/where>

"""


PIMPMYTHEME_GIT_REPOSITORY_SETTINGS_ERROR = """To clone or update a git
repository of themes you need to speficy it in your current django settings
with the PIMPMYTHEME_GIT_REPOSITORY or in your command line as bellow:

    python manage.py update_themefolder_from_git --git_repository git@github.com:<you>/<your_folder>.git

"""  # noqa


GIT_IMPORT_ERROR = """To update pimpmytheme folder from a git repository you
need to install the `gitpython` library, for example be typing the following
command:

    pip install gitpython

"""


class Command(BaseCommand):

    args = "[--folder] [--git_repository]"

    help = """Clones or updates pimpmytheme folder."""

    option_list = BaseCommand.option_list + (
        make_option(
            '--folder',
            action='store',
            dest='folder',
            help='Overrides PIMPMYTHEME_FOLDER settings value.'
        ),
        make_option(
            '--git_repository',
            action='store',
            dest='git_repository',
            help='Overrides PIMPMYTHEME_GIT_REPOSITORY settings value.'
        ),
    )

    def handle(self, *args, **options):

        # get folder where to clone from command line or settings
        folder = options.get('folder')\
            or getattr(settings, 'PIMPMYTHEME_FOLDER', None)

        # not set
        if not folder:
            raise CommandError(PIMPMYTHEME_FOLDER_SETTINGS_ERROR)

        # get git repository to clone or update from command line or settings
        git_repository = options.get('git_repository')\
            or getattr(settings, 'PIMPMYTHEME_GIT_REPOSITORY', None)

        # not set
        if not git_repository:
            raise CommandError(PIMPMYTHEME_GIT_REPOSITORY_SETTINGS_ERROR)

        # check python git lib requirement
        try:
            import git
        except ImportError:
            raise CommandError(GIT_IMPORT_ERROR)

        # git clone
        try:
            os.makedirs(folder)
            git.Git().clone(git_repository, folder)

        # git update if folder already exist
        except OSError:
            repo = git.Repo(folder)
            repo.git.pull()
