import logging
import sys
from pathlib import Path
import os

from dotenv import load_dotenv
import multiprocessing_logging

import logzero

load_dotenv(verbose=True)

PER_PAGE = int(os.environ.get('PER_PAGE', 30))
CACHE_DIR = Path(os.environ.get('CACHE_DIR', '.cache')).resolve()
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
DB_FILE = 'apps.db'
MIGRATIONS_DIR = './fps/migrations'
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'dev')


IGNORE_REPOS = ["ansible-playbook", "buildbot", "flathub",
                "buildbot", "buildbot-config", "buildbot-flathub",
                "shared-modules", "linux-store-frontend", "flathub.org",
                "linux-store-backend", "flathub-stats",
                "rpm-nginx", "electron-sample-app"]


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
