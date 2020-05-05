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

def _where(condition, pk="id", name="name") -> str:
    """
    If `condition` is an int, returns '`pk` = `condition`'.
    If `condition` is a str without spaces, returns '`name` = `condition`'
    If `condition` is a str with spaces, returns `condition` as is.
    If `condition` is a 1-dimensional list of size 2, returns 'elem[0] = elem[1]'
    If `condition` is a 1-dimensional list of size 3, returns 'elem[0] elem[1] elem[2]',
        assuming elem[1] is a comparison operator.
    If `condition` is a multi-dimensional list, returns a series of condtions conjoined
        by 'AND'.
    """

    clause = ""
    try:
        condition = int(condition)
        clause += f"{pk} = {condition}"
    except ValueError:
        if isinstance(condition, str):
            if len(condition.split(" ")) == 1:
                clause += f"{name} = '{condition}'"
            else:
                clause = condition
        elif isinstance(condition, list):
            if isinstance(condition[0], list):
                clause += " AND ".join([_where(case, pk, name) for case in condition])
            elif len(condition) == 2:
                clause += "=".join(str(elem) for elem in condition) # f"{condition[0]} = {condition[1]}"            
            elif len(condition) == 3:
                clause += " ".join(condition)

    return clause

def select(table:str, columns:list=["*"], id=None, name=None, coerce=False) -> list:
    """
    SELECT `columns` FROM `table`
        [WHERE `table`.id = `id`]
        [WHERE `table`.name = `name`]
    ;

    If `coerce`, converts each row into the appropriate data type.
    """
    db = get_db()

    columns_str = ", ".join([f"{table}.{column}" for column in columns])
    query = f"SELECT {columns_str} FROM {table}"
    if id: query += f" WHERE {table}.id = {id};"
    elif name: query += f" WHERE {table}.name = '{name}';"

    results = db.execute(query).fetchall()

    if coerce and (Class := class_map.get(table)):
        results = [Class.from_row(row) for row in results]

    return results

def insert(table:str, values:list) -> None:
    """INSERT INTO `table` VALUES `values`;"""

    db = get_db()
    placeholders = ", ".join("?" * len(values))
    query = f"INSERT INTO {table} VALUES (NULL, {placeholders});"
    db.execute(query, values)
    db.commit()

def update(table:str, values:dict, where:dict) -> None:
    """
    UPDATE `table`
        SET `values`
        WHERE `where`
    """

    db = get_db()

    SET = ", ".join([f"{column}='{value}'" for column, value in values.items()])
    WHERE = _where(where)

    query = f"UPDATE `{table}` SET {SET} WHERE {WHERE}"
    db.execute(query)
    db.commit()

def get_languages() -> list:
    """
    """

    db = get_db()
    query = """
        SELECT languages.id, languages.name, eng_name, ancestors.name AS ancestor, iso_639_1, iso_639_2, iso_639_3
            FROM `languages`
            LEFT JOIN (SELECT id, name FROM languages) AS ancestors ON ancestors.id = languages.ancestor_id;
        """
    results = db.execute(query).fetchall()
    languages = [Language.from_row(row) for row in results]

    return languages

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