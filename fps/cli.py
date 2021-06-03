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
import click

from fps import Application
from fps.database import Database


@click.group()
@click.pass_context
def run(ctx):
    db = Database()
    app = Application(db)
    ctx.obj = {
        'app': app
    }


@run.command(help="Refresh packages cache")
@click.pass_context
def refresh(ctx):
    app = ctx.obj['app']
    # Reclones the repsitories if needed
    app.refresh_cache()
    app.update_database()

@run.command(help="Runs the web server")
@click.pass_context
def server(ctx):
    app = ctx.obj['app']
    app.run_server()
