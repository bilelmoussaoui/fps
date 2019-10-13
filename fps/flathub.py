import os
import sys
from pathlib import Path

import github

from fps.config import logger, GITHUB_TOKEN, IGNORE_REPOS
from fps.repository import Repository


class Flathub:

    @staticmethod
    def refresh_cache():
        fl = Flathub()

        repositories = fl.org.get_repos('public', 'full_name', 'asc')
        for gh_repo in repositories:

            if gh_repo.name not in IGNORE_REPOS:
                pending_invitations = gh_repo.get_pending_invitations().totalCount
                updated_at = gh_repo.updated_at
                app_id = gh_repo.name
                archived = gh_repo.archived
                clone_url = gh_repo.clone_url

                repo = Repository.new(
                    ** {
                        'pending_invitations': pending_invitations,
                        'app_id': app_id,
                        'updated_at': updated_at,
                        'archived': archived,
                        'clone_url': clone_url
                    }
                )
                # Clone the repository
            else:
                logger.debug(f"Ignoring {gh_repo.name}")

    def __init__(self):
        gh = github.Github(GITHUB_TOKEN)
        self.org = gh.get_organization("flathub")
