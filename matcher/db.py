import sqlite3

import click
from flask import current_app, g as app_context
from flask.cli import with_appcontext


def get_db():
    if 'db' not in app_context:
        app_context.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        app_context.db.row_factory = sqlite3.Row

    return app_context.db


def close_db(e=None):
    db = app_context.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as file:
        db.executescript(file.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
