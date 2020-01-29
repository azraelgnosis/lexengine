import os
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'lexengine.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensures there's an instance folder
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import data
    data.init_app(app)

    from . import lexengine
    app.register_blueprint(lexengine.bp)

    return app