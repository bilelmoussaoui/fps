import datetime
import os
from pathlib import Path

import git
import jinja2
import requests

from fps.config import logger, CACHE_DIR
from fps.database import Database
from fps.utils import InvalidManifest, find_manifest, parse_manifest


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
            query, (app_id, archived, updated_at, pending_invitations, runtime, base, status_message ))
        return App(_id, app_id, archived, updated_at, pending_invitations, runtime, base, status_message)

    @staticmethod
    def from_app_id(app_id):
        query = "SELECT * FROM apps WHERE app_id=?"
        rows = Database.get_default().fetch(query, (app_id, ))
        if rows:
            row = rows[0]
            return App(row[0], row[1], row[2], row[3], row[4], row[5], row[6])

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

        app = App.from_app_id(app_id)
        if not app:
            try:
                manifest = find_manifest(app_id, repo_cache)
                kwargs["runtime"] = f"{manifest['runtime']}::{manifest['runtime-version']}"
                if manifest.get('base'):
                    kwargs["base"] = f"{manifest.get('base')}::{manifest.get('base-version')}"
            except InvalidManifest as e:
                kwargs["status_message"] = str(e)
            app = App.new(**kwargs)

            logger.debug(f"Updating {app_id}")


        return Repository(app)

    @staticmethod
    def from_row(row):
        app = App(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        return Repository(app)

    def __init__(self, app: App):
        self._app = app
        repo_cache = CACHE_DIR.joinpath(app.app_id)

        self._git_repo = git.Repo(str(repo_cache))

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
    def latest_build(self):
        builds_uri = f"https://flathub.org/builds/api/v2/builds?flathub_name={self.name}"

        response = requests.get(builds_uri)
        builds = response.json()["builds"]
        if builds:
            builds.sort(key=lambda build: build["started_at"], reverse=True)
            latest_build = builds[0]
            started_at = datetime.datetime.fromtimestamp(
                latest_build["started_at"])
            state_str = latest_build["state_string"]

            has_errors = state_str != 'build successful'

            response = f"Started at: {started_at}<br/>{state_str}"

        else:
            response = "Never built"
            has_errors = True
        if has_errors:
            return jinja2.Markup(f'<div class="text-danger">{response}</div>')
        else:
            return jinja2.Markup(f'<div class="text-success">{response}</div>')

    @property
    def pending_invitations(self):
        """The number of pending invitations."""
        return self._app.pending_invitations

    @property
    def is_valid(self):
        if self.archived:
            return False

        return len(self.name.split(".")) >= 3
