from collections import OrderedDict
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)

from .data import get_db, select, insert, get_languages

bp = Blueprint('lexengine', __name__)

@bp.route('/', methods=('GET', 'POST'))
def index():
    return render_template("index.html")

@bp.route('/languages/', methods=('GET', 'POST'))
def languages():
    if request.method == 'POST':
        values = {key:val for key, val in request.form.items()}
        values['ancestor_id'] = None

        if ancestor_name := values['ancestor']:            
            try:
                ancestor = select("languages", name=ancestor_name, coerce=True)[0]
            except IndexError:
                insert("languages", values=[ancestor_name, ancestor_name, None, None, None, None])
                ancestor = select("languages", name=ancestor_name, coerce=True)[0]
            values['ancestor_id'] = ancestor.language_id

        error = None        
        if select("languages", name=values['name']):
            error = "Language already exists in database."

        if not error:
            columns = ['name', 'eng_name', 'ancestor_id', 'iso_639_1', 'iso_639_2', 'iso_639_3']
            insert("languages", values=[values[col] for col in columns])
            return redirect(url_for('lexengine.languages'))

        flash(error)

    return render_template('languages.html', languages=get_languages())

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