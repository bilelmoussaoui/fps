#
# Copyright (c) 2019 Bilal Elmoussaoui.
#
# This file is part of Flathub Package Status
# (see https://github.com/bilelmoussaoui/fps).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
import github

from fps.config import GITHUB_TOKEN, IGNORE_REPOS, logger


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
