from flask import (
    Blueprint, render_template
)

from .data import get_db, select

bp = Blueprint('lexengine', __name__)

@bp.route('/', methods=('GET', 'POST'))
def index():
    return render_template("index.html")

@bp.route('/languages/')
def languages():
    return render_template('languages.html', languages=select("languages", coerce=True))

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