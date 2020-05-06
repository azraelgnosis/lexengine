from collections import OrderedDict
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)

from .data import get_db, select, insert, update, delete, get_languages
from .models import Language

bp = Blueprint('lexengine', __name__)

@bp.route('/', methods=('GET', 'POST'))
def index():
    return render_template("index.html")

@bp.route('/languages/', methods=('GET', 'POST'))
def languages():
    if request.method == 'POST':
        values = {key:(val or None) for key, val in request.form.items()}
        values['ancestor_id'] = None

        if ancestor_name := values['ancestor']:            
            try:
                ancestor = select("languages", name=ancestor_name, coerce=True)[0]
            except IndexError:
                insert("languages", values=[ancestor_name, ancestor_name, None, None, None, None])
                ancestor = select("languages", name=ancestor_name, coerce=True)[0]
            values['ancestor_id'] = ancestor.id

        error = None
        if not values['name']:
            error = "Name cannot be empty."
        if select("languages", name=values['name']):
            error = "Language already exists in database."

        if not error:
            insert("languages", values=[values[col] for col in Language.columns])
            return redirect(url_for('lexengine.languages'))

        flash(error)

    return render_template('languages.html', languages=get_languages())

@bp.route('/languages/edit/', methods=['GET', 'POST'])
def language_edit():
    if request.method == 'POST':
        values = {key:(val or None) for key, val in request.form.items()}

        if values['col'] == 'ancestor':
            ancestor_name = values['val']
            try:
                ancestor = select("languages", name=ancestor_name, coerce=True)[0]
            except IndexError:
                insert("languages", values=[ancestor_name, ancestor_name, None, None, None, None])
                ancestor = select("languages", name=ancestor_name, coerce=True)[0]
            finally:
                values['col'] = 'ancestor_id'
                values['val'] = ancestor.id
            
        error = None
        if values['col'] == 'eng_name' and not values['val']:
            error = "Name cannot be empty."
        
        if not error:
            update("languages", values={values['col']: values['val']}, where=values['id'])

        flash(error)
    
    return redirect(url_for('lexengine.languages'))

@bp.route('/languages/delete/', methods=['POST'])
def language_delete():
    language_id = request.form['id']
    delete('languages', language_id)
    return redirect(url_for('lexengine.languages'))

@bp.route('/<language>/lexicon/', methods=('GET', 'POST'))
def lexicon(language):
    db = get_db()
    lexicon = db.execute(
        'SELECT * FROM words ORDER BY word'
    ).fetchall()

    # dialects = db.execute(
    #     'SELECT * FROM dialects'
    #     'WHERE '
    # )

    return render_template('lexicon.html', lexicon=lexicon)
