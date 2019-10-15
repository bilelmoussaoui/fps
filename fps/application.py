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
import multiprocessing
import os

import github

from fps.config import CACHE_DIR, GITHUB_TOKEN, IGNORE_REPOS, PER_PAGE, logger
from fps.repository import Repository
from fps.utils import update_repo


class Application:

    def __init__(self, db):
        self._db = db

    @property
    def total_repos(self) -> int:
        return len(os.listdir(str(CACHE_DIR)))

    def load_repos_page(self, current_page: int):
        offset = (current_page - 1) * PER_PAGE

        query = f"SELECT * from apps LIMIT {PER_PAGE} OFFSET {offset}"

        rows = self._db.fetch(query)

        return [Repository.from_row(row) for row in rows]

    def load_repos_per_runtime(self, runtime_id):
        if runtime_id == "undefined":
            query = f"SELECT * from apps WHERE runtime IS NULL"

            rows = self._db.fetch(query)
        else:
            query = f"SELECT * from apps WHERE runtime=?"

            rows = self._db.fetch(query, (runtime_id, ))

        return [Repository.from_row(row) for row in rows]

    def load_repos_per_base(self, base_id):
        if base_id != "undefined":
            query = f"SELECT * from apps WHERE base=?"

            rows = self._db.fetch(query, (base_id, ))

            return [Repository.from_row(row) for row in rows]

    def refresh_cache(self):
        logger.info("Refreshing repositories cache...")
        gh = github.Github(GITHUB_TOKEN)
        org = gh.get_organization("flathub")
        repositories = org.get_repos('public', 'full_name', 'asc')
        _repos = []

        for gh_repo in repositories:
            if gh_repo.name not in IGNORE_REPOS:
                _repos.append(gh_repo)
                # Clone the repository
            else:
                logger.debug(f"Ignoring {gh_repo.name}")

        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        pool.map(update_repo, _repos)
        pool.close()

    def search(self, search_term):
        query = "SELECT * FROM apps WHERE app_id LIKE ? OR runtime LIKE ? OR base LIKE ? ORDER BY app_id ASC"

        rows = self._db.fetch(query, ['%' + search_term + '%'] * 3)

        return [Repository.from_row(row) for row in rows]

    def get_runtimes(self):
        query = "SELECT DISTINCT runtime FROM apps ORDER BY runtime ASC"

        runtimes = self._db.fetch(query)
        return [runtime[0] if runtime[0] else "undefined" for runtime in runtimes]

    def get_bases(self):
        query = "SELECT DISTINCT base FROM apps ORDER BY base ASC"

        bases = self._db.fetch(query)
        return [base[0] if base[0] else "undefined" for base in bases]

    def get_runtimes_usage(self):
        query = "SELECT DISTINCT runtime, COUNT(runtime) FROM apps WHERE archived=0 GROUP BY runtime ORDER BY runtime ASC"

        runtimes = self._db.fetch(query)
        runtimes_usages = [(runtime[0], runtime[1])
                           for runtime in runtimes if runtime[0]]

        gnome_runtimes = ["org.gnome.Platform", "org.gnome.Sdk"]
        kde_runtimes = ["org.kde.Platform", "org.kde.Sdk"]
        fdo_runtimes = ["org.freedesktop.Platform", "org.freedesktop.Sdk"]

        gnome_runtimes_usages = {}
        kde_runtimes_usages = {}
        fdo_runtimes_usages = {}

        for runtime, usage_count in runtimes_usages:
            runtime_name, runtime_version = runtime.split("::")
            if runtime_name in gnome_runtimes:
                gnome_runtimes_usages[runtime_version] = gnome_runtimes_usages.get(
                    runtime_version, 0) + usage_count
            elif runtime_name in kde_runtimes:
                kde_runtimes_usages[runtime_version] = kde_runtimes_usages.get(
                    runtime_version, 0) + usage_count
            elif runtime_name in fdo_runtimes:
                fdo_runtimes_usages[runtime_version] = fdo_runtimes_usages.get(
                    runtime_version, 0) + usage_count

        return (runtimes_usages, gnome_runtimes_usages, kde_runtimes_usages, fdo_runtimes_usages)

    def get_bases_usage(self):
        query = "SELECT DISTINCT base, COUNT(base) FROM apps WHERE archived=0 GROUP BY base ORDER BY base ASC"

        bases = self._db.fetch(query)
        return [(base[0], base[1]) for base in bases if base[0]]

    def run_server(self):
        import fps.server
