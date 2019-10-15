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
import git
import jinja2

from fps.config import CACHE_DIR, logger
from fps.database import Database
from fps.utils import InvalidManifest, find_manifest, get_latest_build_status


class App:

    @staticmethod
    def new(**kwargs):
        pending_invitations = kwargs.get("pending_invitations")
        updated_at = kwargs.get("updated_at")
        app_id = kwargs.get("app_id")
        archived = kwargs.get("archived")
        runtime = kwargs.get("runtime")
        base = kwargs.get("base")
        status_message = kwargs.get("status_message")
        query = "INSERT INTO apps (app_id, archived, updated_at, pending_invitations, runtime, base, status_message) VALUES (?, ?, ?, ?, ?, ?, ?)"

        _id = Database.get_default().insert(
            query, (app_id, archived, updated_at, pending_invitations, runtime, base, status_message))
        return App(_id, app_id, archived, updated_at, pending_invitations, runtime, base, status_message)

    @staticmethod
    def from_app_id(app_id):
        query = "SELECT * FROM apps WHERE app_id=?"
        rows = Database.get_default().fetch(query, (app_id, ))
        if rows:
            row = rows[0]
            return App(*row)

    def __init__(self, _id, app_id, archived, updated_at, pending_invitations, runtime, base, status_message):
        self.id = _id
        self.app_id = app_id
        self.updated_at = updated_at
        self.pending_invitations = pending_invitations
        self.archived = archived
        self.runtime = runtime
        self.base = base
        self.status_message = status_message


class Repository:

    @staticmethod
    def new(**kwargs):
        app_id = kwargs.get("app_id")
        repo_cache = CACHE_DIR.joinpath(app_id)

        if not repo_cache.exists():
            logger.debug(f"Cloning {app_id}")
            git.Git(CACHE_DIR).clone(kwargs.get("clone_url"), depth=1)
        elif kwargs.get("refresh-cache"):
            logger.debug(f"Pulling latest changes {app_id}")
            git.Repo(str(repo_cache)).remote('origin').pull()

        app = App.from_app_id(app_id)
        if not app:
            try:
                manifest = find_manifest(app_id, repo_cache)
                kwargs["runtime"] = f"{manifest['runtime']}::{manifest['runtime-version']}"
                if manifest.get('base'):
                    kwargs["base"] = f"{manifest.get('base')}::{manifest.get('base-version')}"
            except InvalidManifest as e:
                kwargs["status_message"] = jinja2.Markup(
                    f'<div class="text-danger">{e}</div>')

            if not kwargs.get("status_message"):
                kwargs["status_message"] = get_latest_build_status(app_id)

            app = App.new(**kwargs)

            logger.debug(f"Updating {app_id}")

        return Repository(app)

    @staticmethod
    def from_row(row):
        app = App(*row)
        return Repository(app)

    def __init__(self, app: App):
        self._app = app
        self._repo_dir = CACHE_DIR.joinpath(app.app_id)

        self._git_repo = git.Repo(str(self._repo_dir))

    @property
    def is_eol(self):
        return self._app.archived

    @property
    def status_message(self):
        return self._app.status_message

    @property
    def runtime(self):
        return self._app.runtime

    @property
    def name(self):
        """The repository name."""
        return self._app.app_id

    @property
    def updated_at(self):
        """Returns a datetime.datetime."""
        return self._app.updated_at

    @property
    def pending_invitations(self):
        """The number of pending invitations."""
        return self._app.pending_invitations

    @property
    def is_valid(self):
        if self.archived:
            return False

        return len(self.name.split(".")) >= 3
