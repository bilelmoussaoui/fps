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
    app.refresh_cache()


@run.command(help="Runs the web server")
@click.pass_context
def server(ctx):
    app = ctx.obj['app']
    app.run_server()
