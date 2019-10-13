import json
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
