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
