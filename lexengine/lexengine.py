from collections import OrderedDict
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)

from lexengine.db import LexLoreKeeper
from .models import Language

bp = Blueprint('lexengine', __name__)
lk = LexLoreKeeper()


@bp.route('/', methods=('GET', 'POST'))
def index():
    return render_template("index.html")

@bp.route('/languages/', methods=['GET'])
def languages():
    return render_template('languages.html', languages=lk.get_languages())

@bp.route('/languages/add/', methods=['POST'])
def language_add():
    values = {key:(val or None) for key, val in request.form.items()}
    values['ancestor_id'] = None

    error = None
    if not values['name']:
        error = "Name cannot be empty."
    if lk.select("languages", where=values['name']):
        error = "Language already exists in database."
    
    if ancestor_name := values['ancestor']:
        try:
            ancestor = lk.select("languages", where=ancestor_name, coerce=True)[0]
        except IndexError:
            lk.insert("languages", values=[ancestor_name, ancestor_name, None, None, None, None])
            ancestor = lk.select("languages", where=ancestor_name, coerce=True)[0]
        values['ancestor_id'] = ancestor.id

    if error:
        flash(error)
    else:
        lk.insert("languages", values=[values[col] for col in Language.columns])

    return redirect(url_for('lexengine.languages'))

@bp.route('/languages/edit/', methods=['POST'])
def language_edit():
    values = {key:(val or None) for key, val in request.form.items()}

    if values['col'] == 'ancestor':
        ancestor_name = values['val']
        try:
            ancestor = lk.select("languages", where=ancestor_name, coerce=True)[0]
        except IndexError:
            lk.insert("languages", values=[ancestor_name, ancestor_name, None, None, None, None])
            ancestor = lk.select("languages", where=ancestor_name, coerce=True)[0]
        finally:
            values['col'] = 'ancestor_id'
            values['val'] = ancestor.id
        
    error = None
    if values['col'] == 'eng_name' and not values['val']:
        error = "Name cannot be empty."
    
    if error:
        flash(error)
    else:
        lk.update("languages", values={values['col']: values['val']}, where=values['id'])

    return redirect(url_for('lexengine.languages'))

@bp.route('/languages/delete/', methods=['POST'])
def language_delete():
    language_id = request.form['id']
    lk.delete('languages', language_id)
    return redirect(url_for('lexengine.languages'))

@bp.route('/languages/<string:language_name>/')
def language(language_name:str):
    language = lk.get_language(language_name) # select("languages", where=language_name, coerce=True)
    
    error = None
    if not language:
        error = "No such language."

    if not error:
        return render_template('language.html', language=language)

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
