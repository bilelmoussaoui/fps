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

    return render_template('runtimes.html', ** {
        'runtimes': runtimes
    })

@flask_app.route('/runtime/<runtime_id>')
def runtime(runtime_id):
    app = Application(get_db())

    repos = app.load_repos_per_runtime(runtime_id)

    return render_template('runtime.html', **{
        'repositories': repos,
    })

@flask_app.route('/stats')
def stats():

    app = Application(get_db())

    runtimes_usage = app.runtimes_stats()

    return render_template('stats.html', **{
        'runtimes_usage': runtimes_usage,
    })


@flask_app.route('/refresh-cache')
def refresh_cache():
    app = Application(get_db())

    app.refresh_cache()


flask_app.run()
