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
from flask import Flask, g, render_template, request

from fps.application import Application
from fps.database import Database

flask_app = Flask(__name__,
                  static_url_path='',
                  static_folder='templates/static',)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = Database()
    return db


@flask_app.route('/')
def main():
    app = Application(get_db())

    try:
        current_page = int(request.args.get("page", "1"))
    except ValueError:
        current_page = 1

    total_pages = app.total_repos
    start_pagination = max(1, current_page - 5)
    end_pagination = min(current_page + 5, total_pages)

    repos = app.load_repos_page(current_page)

    return render_template('repos.html', **{
        'current_page': current_page,
        'total_pages': total_pages,
        'repositories': repos,
        'start_pagination': start_pagination,
        'end_pagination': end_pagination
    })


@flask_app.route('/runtimes')
def runtimes():
    app = Application(get_db())

    runtimes = app.get_runtimes()
    bases = app.get_bases()

    return render_template('runtimes.html', ** {
        'runtimes': runtimes,
        'bases': bases
    })


@flask_app.route('/runtime/<runtime_id>')
def runtime(runtime_id):
    app = Application(get_db())

    repos = app.load_repos_per_runtime(runtime_id)

    return render_template('runtime.html', **{
        'repositories': repos,
    })


@flask_app.route('/base/<base_id>')
def base(base_id):
    app = Application(get_db())

    repos = app.load_repos_per_base(base_id)

    return render_template('base.html', **{
        'repositories': repos,
    })


@flask_app.route('/stats')
def stats():

    app = Application(get_db())

    runtimes_usage, gnome_usage, kde_usage, fdo_usage = app.get_runtimes_usage()
    bases_usage = app.get_bases_usage()

    return render_template('stats.html', **{
        'runtimes_usage': runtimes_usage,
        'fdo_usage': fdo_usage.items(),
        'gnome_usage': gnome_usage.items(),
        'kde_usage': kde_usage.items(),
        'bases_usage': bases_usage,
    })


@flask_app.route('/refresh-cache')
def refresh_cache():
    app = Application(get_db())

    app.refresh_cache()


@flask_app.route('/search')
def search():
    query = request.args.get("q")

    app = Application(get_db())
    results = app.search(query)

    return render_template('search.html', ** {
        'results': results,
        'query': query
    })


flask_app.run()
