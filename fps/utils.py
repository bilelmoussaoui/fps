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
from jsoncomment import JsonComment
from pathlib import Path

import yaml


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
    from fps.repository import Repository

    pending_invitations = gh_repo.get_pending_invitations().totalCount
    updated_at = gh_repo.updated_at
    app_id = gh_repo.name
    archived = gh_repo.archived
    clone_url = gh_repo.clone_url

    Repository.new(
        ** {
            'pending_invitations': pending_invitations,
            'app_id': app_id,
            'updated_at': updated_at,
            'archived': archived,
            'clone_url': clone_url
        }
    )
