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
import datetime
from pathlib import Path

import git
from fps.config import CACHE_DIR, logger
import jinja2
import requests
import yaml
from jsoncomment import JsonComment


class InvalidManifest(Exception):
    pass


def find_manifest(app_id, repo_dir) -> Path:
    supported_exts = ["json", "yml", "yaml"]

    for supported_ext in supported_exts:
        manifest_path = Path(repo_dir).joinpath(f"{app_id}.{supported_ext}")
        if manifest_path.exists():
            break
    if not manifest_path.exists():
        raise InvalidManifest("Manifest not found")
    return parse_manifest(manifest_path)


def parse_manifest(manifest_path: Path):
    with open(str(manifest_path), 'r') as stream:
        if manifest_path.suffix == '.json':
            json = JsonComment()
            try:
                manifest = json.load(stream)
            except Exception as exc:
                raise InvalidManifest(exc)
        else:
            try:
                manifest = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                raise InvalidManifest(exc)
    return manifest


def update_repo(gh_repo):
    app_id = gh_repo.name
    refresh_cache = True # TODO: compute this with the latest updated time
    repo_cache = CACHE_DIR.joinpath(app_id)
    try:
        if not repo_cache.exists():
            logger.debug(f"Cloning {app_id}")
            git.Git(CACHE_DIR).clone(gh_repo.clone_url, depth=1)
        elif refresh_cache:
            logger.debug(f"Pulling latest changes {app_id}")
            git.Repo(str(repo_cache)).remote('origin').pull()
    except ValueError as e:
        logger.error(f"Failed to update cached repository {app_id}: {e}")
def get_latest_build_status(app_id):
    builds_uri = f"https://flathub.org/builds/api/v2/builds?flathub_name={app_id}"

    response = requests.get(builds_uri)
    status_message = None
    if response.status_code == 200:
        builds = response.json()["builds"]
        if builds:
            builds = list(filter(lambda build: build['complete'], builds))
            builds.sort(key=lambda build: build["complete_at"], reverse=True)
            latest_build = builds[0]
            started_at = datetime.datetime.fromtimestamp(
                latest_build["started_at"])
            state_str = latest_build["state_string"]

            has_errors = state_str != 'build successful'
            buildid = latest_build['number']
            builderid = latest_build['builderid']

            status_message = f"<a href='https://flathub.org/builds/#/builders/{builderid}/builds/{buildid}'>Started at: {started_at}<br/>{state_str}</a>"

    if not status_message:
        status_message = "Never built"
        has_errors = True

    if has_errors:
        return jinja2.Markup(f'<div class="text-danger">{status_message}</div>')
    else:
        return jinja2.Markup(f'<div class="text-success">{status_message}</div>')
