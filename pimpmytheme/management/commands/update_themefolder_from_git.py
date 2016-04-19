# -*- coding: utf-8 -*-
import logging
import os
import sys

from optparse import make_option

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from django.conf import settings
try:
    import git
except ImportError:
    sys.stderr.write("""To update pimpmytheme folder from a git repository you
need to install the `gitpython` library, for example be typing the following
command:

    pip install gitpython

""")
    sys.exit(1)

# Ensure compat between GitPython 0.1.x, 0.2.x and GitPython 1.0.x.
try:
    from git.exc import GitCommandError
except ImportError:
    from git.errors import GitCommandError


logger = logging.getLogger(__name__)


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

        try:
            self.update(folder, git_repository)
        except GitCommandError as e:
            logger.error("%r: \n%s", e, e.stderr)
            raise CommandError("Failed to update folder")

    def clone(self, folder, git_repository):
        """Ensures theme destination folder and clone git specified repo in it.

        :param git_repository: git url of the theme folder
        :param folder: path of the git managed theme folder
        """
        os.makedirs(folder)
        git.Git().clone(git_repository, folder)

    def update_git_repository(self, folder, git_repository):
        """Updates git remote for the managed theme folder if has changed.

        :param git_repository: git url of the theme folder
        :param folder: path of the git managed theme folder
        """

        # load repo object from path
        repo = git.Repo(folder)

        # keep local_head_name for to reset folder remote head later
        local_head_name = repo.head.ref.name

        # test if git repository url has changed
        remote = repo.remote('origin')
        if remote.url == git_repository:
            return

        # remove/add new remote repository origin
        remote.remove(repo, 'origin')
        origin = remote.add(repo, 'origin', git_repository)

        # fetch available branches
        origin.fetch()

        # get remote head according previously store local head name
        remote_head = getattr(origin.refs, local_head_name)
        # reset repository tracking branch according deduced remote head
        repo.create_head(local_head_name, remote_head)\
            .set_tracking_branch(remote_head)

    def pull(self, folder):
        """Pulls git modification to the theme folder.

        :param folder: path of the git managed theme folder
        """
        git.Repo(folder).git.pull()

    def update(self, folder, git_repository):
        """Creates or updates theme folder according given git repository.

        :param git_repository: git url of the theme folder
        :param folder: path of the git managed theme folder
        """
        # git clone
        try:
            self.clone(folder, git_repository)
        # git update if folder already exist
        except OSError:
            self.update_git_repository(folder, git_repository)
            self.pull(folder)
