from flask import Blueprint, g, redirect, url_for
import functools

from lexengine.db import LexLoreKeeper

bp = Blueprint("admin", __name__, url_prefix="/admin")
lk = LexLoreKeeper()

def admin_privileges(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user and 'admin' in g.user.roles:
            return view(**kwargs)
        return redirect(url_for('auth.login'))

@bp.route("/")
@admin_privileges
def portal():
    return "Adminstrative Portal"

@bp.route("/tables/")
def tables():
    tables = None