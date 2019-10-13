import os
import sys
from pathlib import Path

import github

from fps.config import GITHUB_TOKEN, IGNORE_REPOS, logger
from fps.repository import Repository


class Flathub:

    @staticmethod
    def refresh_cache():
        fl = Flathub()

        repositories = fl.org.get_repos('public', 'full_name', 'asc')
        _repos = []
        for gh_repo in repositories:

            if gh_repo.name not in IGNORE_REPOS:
                _repos.append(gh_repo)
                # Clone the repository
            else:
                logger.debug(f"Ignoring {gh_repo.name}")
        return _repos

    def __init__(self):
        gh = github.Github(GITHUB_TOKEN)
        self.org = gh.get_organization("flathub")
