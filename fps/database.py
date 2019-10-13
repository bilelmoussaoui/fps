import sqlite3

from yoyo import get_backend, read_migrations

from fps.config import DB_FILE, MIGRATIONS_DIR


class Database:
    instance = None

    @staticmethod
    def get_default():
        if Database.instance is None:
            Database.instance = Database()
        return Database.instance

    def __init__(self):
        backend = get_backend(f'sqlite:///{DB_FILE}')
        migrations = read_migrations(MIGRATIONS_DIR)
        with backend.lock():
            backend.apply_migrations(backend.to_apply(migrations))
        self._conn = sqlite3.connect(DB_FILE)

    def insert(self, query, values):
        cursor = self._conn.cursor()
        cursor.execute(query, values)
        _id = cursor.lastrowid
        cursor.close()
        self._conn.commit()
        return _id

    def fetch(self, query, values=()):
        cursor = self._conn.cursor()
        cursor.execute(query, values)
        rows = cursor.fetchall()
        cursor.close()
        return rows
