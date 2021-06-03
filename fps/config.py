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
import logging
import os
import sys
from pathlib import Path

import logzero
from dotenv import load_dotenv

load_dotenv(verbose=True)

PER_PAGE = int(os.environ.get('PER_PAGE', 30))
CACHE_DIR = Path(os.environ.get('CACHE_DIR', '.cache')).resolve()
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
DB_FILE = 'apps.db'
MIGRATIONS_DIR = './fps/migrations'
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'dev')


IGNORE_REPOS = [
    "ansible-playbook", "ansible-role-zerotier",
    "flatpak-external-data-checker", "buildbot", "flathub",
    "buildbot", "buildbot-config", "buildbot-flathub",
    "shared-modules", "linux-store-frontend", "flathub.org",
    "linux-store-backend", "flathub-stats",
    "rpm-nginx", "blog", "electron-sample-app", "backend", "frontend", "actions"
]


if not GITHUB_TOKEN:
    print("GITHUB_TOKEN environment variable is not set")
    sys.exit(1)

if not CACHE_DIR.exists():
    CACHE_DIR.mkdir(exist_ok=True)


# Logging
if ENVIRONMENT == "dev":
    level = logging.DEBUG
else:
    level = logging.ERROR

log_format = '%(color)s[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d]%(end_color)s %(message)s'
formatter = logzero.LogFormatter(fmt=log_format)
logger = logzero.setup_logger(name="fps", level=level, formatter=formatter)
