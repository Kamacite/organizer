import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()

def create_app(test_config=None):
    # create and configure app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.instance_path, 'organizer.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
        JWT_TOKEN_LOCATION = ['cookies'],
        JWT_SESSION_COOKIE = False,
        JWT_COOKIE_SECURE = False,
        JWT_COOKIE_CSRF_PROTECT = True,
        JWT_SECRET_KEY = 'change me',
    )
    
    CORS(app, origins=["http://127.0.0.1:5000"], supports_credentials=True)
    
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

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

    # import resources and add url rules
    from .resources.auth import Login, Refresh, Logout, Register
    app.add_url_rule('/login', view_func=Login.as_view('login'))
    app.add_url_rule('/refresh', view_func=Refresh.as_view('refresh'))
    app.add_url_rule('/logout', view_func=Logout.as_view('logout'))
    app.add_url_rule('/register', view_func=Register.as_view('register'))
    
    from .resources.schedule import Item, Day, Today, Week
    item_view = Item.as_view('item')
    app.add_url_rule('/item', defaults={'item_id': 0}, view_func=item_view, methods=['GET','PUT',])
    app.add_url_rule('/item/<int:item_id>', view_func=item_view, methods=['GET', 'PUT', 'DELETE'])
    app.add_url_rule('/day/<string:get_date>', view_func=Day.as_view('day'))
    app.add_url_rule('/today', view_func=Today.as_view('today'))
    app.add_url_rule('/week/<string:get_date>', view_func=Week.as_view('week'))

    from .resources.project import Projects, Project, Section, Task
    app.add_url_rule('/projects', view_func=Projects.as_view('projects'))
    app.add_url_rule('/project/<int:project_id>', view_func=Project.as_view('project'))
    app.add_url_rule('/section/<int:section_id>', view_func=Section.as_view('section'))
    app.add_url_rule('/task/<int:task_id>', view_func=Task.as_view('task'))

    return app