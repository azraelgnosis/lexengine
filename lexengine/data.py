# import sqlite3
# import click
# from flask import current_app, g
# from flask.cli import with_appcontext

# from lexengine.models import Row, Language, Word

# class_map = {
#     "languages": Language
# }

# def get_db() -> sqlite3.Connection:
#     if 'db' not in g:
#         g.db = sqlite3.connect(
#             current_app.config['DATABASE'],
#             detect_types=sqlite3.PARSE_DECLTYPES
#         )
#         g.db.row_factory = Row

#     return g.db

# def _where(condition, pk="id", val="val") -> str:
#     """
#     If `condition` is an int, returns '`pk` = `condition`'.
#     If `condition` is a str without spaces, returns '`name` = `condition`'
#     If `condition` is a str with spaces, returns `condition` as is.
#     If `condition` is a 1-dimensional list of size 2, returns 'elem[0] = elem[1]'
#     If `condition` is a 1-dimensional list of size 3, returns 'elem[0] elem[1] elem[2]',
#         assuming elem[1] is a comparison operator.
#     If `condition` is a multi-dimensional list, returns a series of condtions conjoined
#         by 'AND'.
#     """

#     if not condition: return

#     clause = ""
#     try:
#         condition = int(condition)
#         clause += f"{pk} = {condition}"
#     except ValueError:
#         if isinstance(condition, str):
#             clause += f"{val} = '{condition}'"
#     except TypeError:
#         if isinstance(condition, list):
#             if isinstance(condition[0], list):
#                 clause += " AND ".join([_where(case, pk, val) for case in condition])
#             elif len(condition) == 2:
#                 clause += "=".join(str(elem) for elem in condition) # f"{condition[0]} = {condition[1]}"            
#             elif len(condition) == 3:
#                 clause += " ".join(condition)

#     return clause

# def select(table:str, where:dict=None, columns:list=["*"], coerce=False) -> list:
#     """
#     SELECT `columns` FROM `table` [WHERE `where`];

#     If `coerce`, converts each row into the appropriate data type.
#     """
#     db = get_db()

#     columns_str = ", ".join([f"{table}.{column}" for column in columns])
#     query = f"SELECT {columns_str} FROM {table}"
#     if where:
#         WHERE = _where(where)
#         query += f" WHERE {WHERE};"

#     results = db.execute(query).fetchall()

#     if coerce and (Class := class_map.get(table)):
#         results = [Class.from_row(row) for row in results]

#     return results

# #? will probaly need to add validation
# def select_one(table:str, where:dict, columns:list=['*'], coerce=False):
#     return select(table, where, columns, coerce)[0]

# #TODO
# def insert(table:str, values:list) -> None:
#     """INSERT INTO `table` VALUES `values`;"""

#     db = get_db()
#     placeholders = ", ".join("?" * len(values))
#     query = f"INSERT INTO {table} VALUES (NULL, {placeholders});"
#     db.execute(query, values)
#     db.commit()

# def update(table:str, values:dict, where:dict) -> None:
#     """
#     UPDATE `table`
#         SET `values`
#         WHERE `where`
#     """

#     db = get_db()

#     SET = ", ".join([f"{column}=?" for column in values.keys()])
#     WHERE = _where(where)

#     query = f"UPDATE `{table}` SET {SET} WHERE {WHERE}"
#     db.execute(query, list(values.values()))
#     db.commit()

# def delete(table:str, where:dict) -> None:
#     """
#     DELETE FROM `table` WHERE `where`;
#     """

#     db = get_db()
#     WHERE = _where(where)
#     query = f"DELETE FROM {table} WHERE {WHERE};"
#     db.execute(query)
#     db.commit()

# def get_languages(where:dict=None) -> list:
#     """
#     """

#     db = get_db()
    
#     SELECT = "SELECT languages.id, languages.val AS name, eng_name, ancestors.val AS ancestor, iso_639_1, iso_639_2, iso_639_3"
#     FROM = "FROM `languages`"
#     JOIN = "LEFT JOIN (SELECT id, val FROM languages) AS ancestors ON ancestors.id = languages.ancestor_id"
#     query = " ".join([SELECT, FROM, JOIN])            
            
#     if where:
#         WHERE = _where(where)
#         query += f" WHERE `languages`.{WHERE};"

#     results = db.execute(query).fetchall()
#     languages = [Language.from_row(row) for row in results]

#     return languages

# def get_language(language) -> Language:
#     return get_languages(where=language)[0]

# def get_lexicon(language_id) -> list:
#     WHERE = _where(["language_id", language_id])
#     query = f"SELECT * FROM words WHERE {WHERE}"

#     words = get_db().execute(query).fetchall()
#     words = [Word.from_row(word) for word in words]

#     return words

# def close_db(e=None):
#     db = g.pop('db', None)

#     if db is not None:
#         db.close()

# def init_db():
#     db = get_db()

#     with current_app.open_resource('schema.sql') as f:
#         db.executescript(f.read().decode('utf8'))

# @click.command('init-db')
# @with_appcontext
# def init_db_command():
#     """Create new tables."""
#     init_db()
#     click.echo('Initialized the database.')

# def init_app(app):
#     app.teardown_appcontext(close_db)
#     app.cli.add_command(init_db_command)