from collections import OrderedDict
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)

from lexengine.const import *
from lexengine.db import LexLoreKeeper, Table
from lexengine.models import Language

bp = Blueprint('lexengine', __name__)
lk = LexLoreKeeper()


@bp.route('/', methods=('GET', 'POST'))
def index():
    return render_template("index.html")

@bp.route('/tables/<string:table_name>/', methods=('GET'))
def tables(table_name):
    table = Table(table_name, lk.db)

    return render_template('_table.html')


@bp.route('/languages/', methods=['GET'])
def languages():
    return render_template('languages.html', languages=lk.get_languages())

@bp.route('/languages/add/', methods=['POST'])
def language_add():
    values = {key:(val or None) for key, val in request.form.items()}
    values['ancestor_id'] = None

    error = None
    if not values['language_val']:
        error = "Name cannot be empty."
    if lk.select(TABLES.LANGUAGE, where=values['language_val']):
        error = "Language already exists in database."
    
    if ancestor_name := values['ancestor']:
        try:
            ancestor = lk.select(TABLES.LANGUAGE, where=ancestor_name, datatype=True)[0]
        except IndexError:
            lk.insert(TABLES.LANGUAGE, values=[ancestor_name, ancestor_name, None, None, None, None])
            ancestor = lk.select(TABLES.LANGUAGE, where=ancestor_name, datatype=True)[0]
        values['ancestor_id'] = ancestor.language_id

    if error:
        flash(error)
    else:
        lk.insert(TABLES.LANGUAGE, values={col: values[col] for col in Language.columns})
        new_language = lk.get_language(values['language_val'])
        lk.insert(TABLES.DIALECT, values={COLUMNS.DIALECT_VAL: new_language.language_val, 
                                          COLUMNS.LANGUAGE_ID: new_language.language_id})

    return redirect(url_for('lexengine.languages'))

@bp.route('/languages/edit/', methods=['POST'])
def language_edit():
    values = {key:(val or None) for key, val in request.form.items()}

    if values['col'] == 'ancestor':
        ancestor_name = values['val']
        try:
            ancestor = lk.select("languages", where=ancestor_name, datatype=True)[0]
        except IndexError:
            lk.insert(TABLES.LANGUAGE, values=[ancestor_name, ancestor_name, None, None, None, None])
            ancestor = lk.select(TABLES.LANGUAGE, where=ancestor_name, datatype=True)[0]
        finally:
            values['col'] = 'ancestor_id'
            values['val'] = ancestor.id
        
    error = None
    if values['col'] == 'eng_name' and not values['val']:
        error = "Name cannot be empty."
    
    if error:
        flash(error)
    else:
        lk.update(TABLES.LANGUAGE, values={values['col']: values['val']}, where=values['id'])

    return redirect(url_for('lexengine.languages'))

@bp.route('/languages/delete/', methods=['POST'])
def language_delete():
    language_id = request.form['id']
    lk.delete('languages', language_id)
    return redirect(url_for('lexengine.languages'))

@bp.route('/languages/<string:language_name>/')
def language(language_name:str):
    language = lk.get_language(language_name) # select("languages", where=language_name, coerce=True)
    dialects = lk.select(TABLES.DIALECT, where={COLUMNS.LANGUAGE_ID: language.language_id}, datatype=True)
    
    error = None
    if not language:
        error = "No such language."

    if not error:
        return render_template('language.html', language=language, dialects=dialects)

    flash(error)

    return redirect(url_for('lexengine.languages'))

@bp.route('/languages/<string:language_name>/lexicon/', methods=('GET', 'POST'))
def lexicon(language_name:str):
    if request.method == 'POST':
        values = {key:(val or None) for key, val in request.form.items()}

    language = lk.get_language(language_name)
    lexicon = lk.get_lexicon(language.id)

    return render_template('lexicon.html', language=language, lexicon=lexicon)

@bp.route('/tengwar/', methods=['GET', 'POST'])
def tengwar():
    import json
    from lexengine.tengwar.cymraeg_to_tengwar import conversion

    transcribed = 'empty'
    if request.method == 'POST':
        text = request.form['text']
        transcribed = conversion(text)
        return json.dumps({'status': 'OK', 'transcribed':transcribed})

    return render_template('tengwar.html', transcribed=transcribed)
