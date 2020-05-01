import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

from lexengine.models import Row, Language

class_map = {
    "languages": Language
}

def get_db() -> sqlite3.Connection:
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = Row

    return g.db

def select(table:str, columns:list=["*"], coerce=None) -> list:
    db = get_db()

    columns_str = ", ".join([f"{table}.{column}" for column in columns])

    query = f"SELECT {columns_str} FROM {table}"

    results = db.execute(query).fetchall()

    if coerce and (Class := class_map.get(table)):
        results = [Class.from_row(row) for row in results]

    return results

def get_language(language) -> Language: pass

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)