import os

from fps.config import CACHE_DIR, PER_PAGE, logger
from fps.flathub import Flathub
from fps.repository import Repository


class Application:

    def __init__(self, db):
        self._db = db
        self._flathub = Flathub()

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

    def refresh_cache(self):
        logger.info("Refreshing repositories cache...")
        self._flathub.refresh_cache()

    def get_runtimes(self):
        query = "SELECT DISTINCT runtime FROM apps ORDER BY runtime ASC"

        runtimes = self._db.fetch(query)
        return [runtime[0] if runtime[0] else "undefined" for runtime in runtimes]

    def runtimes_stats(self):
        query = "SELECT DISTINCT runtime, COUNT(runtime) FROM apps GROUP BY runtime ORDER BY runtime ASC"

        runtimes = self._db.fetch(query)
        return [(runtime[0], runtime[1]) if runtime[0] else ("undefined", runtime[1]) for runtime in runtimes]

    def run_server(self):
        import fps.server
