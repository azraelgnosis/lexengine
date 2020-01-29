import os
from flask import Flask

def create_app():
    app = Flask(__name__)

    # ensures there's an instance folder
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import lexengine
    app.register_blueprint(lexengine.bp)

    return app