import os
from flask import Flask, render_template


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'lexengine.sqlite'),
    )

    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_pyfile('config.py', silent=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from lexengine import db
    db.LexLoreKeeper.init_app(app)

    from . import lexengine
    app.register_blueprint(lexengine.bp)

    @app.route('/templates/<string:filename>/')
    def templates(filename):
        return render_template(f"{filename}")

    return app
