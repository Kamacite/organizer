import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def create_app(test_config=None):
    # create and configure app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.instance_path, 'organizer.db')
    )

    db.init_app(app)

    if test_config is None:
        # Load instance config, if it exists whilst not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load test conf
        app.config.from_mapping(test_config)

    # check instance folder existence
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, World'

    return app