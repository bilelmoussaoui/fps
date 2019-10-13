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
"""

"""
from yoyo import step


steps = [
    step('''
         CREATE TABLE "apps" (
            "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
            "app_id" VARCHAR NOT NULL UNIQUE,
            "archived" BOOLEAN NOT NULL DEFAULT 0,
            "updated_at" VARCHAR NOT NULL,
            "pending_invitations" INT NOT NULL DEFAULT 0,
            "runtime" VARCHAR NULL,
            "base" VARCHAR NULL,
            "status_message" VARCHAR NULL
            )''',
         'DROP TABLE "apps"',
         ignore_errors='apply')
]
