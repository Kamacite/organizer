import os
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager

# Resource Imports
from resources.auth import *
from resources.schedule import *
from resources.project import *

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# Setup CORS to only allow requests from same origin
CORS(app, origins=["http://127.0.0.1:5000"], supports_credentials=True )
# Configure SQLAlchemy db location
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'organizer.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Configure JWT to use cookies and csrf. Change cookie to secure when not developing.
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_SESSION_COOKIE'] = False
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_SECRET_KEY'] = 'change me'

api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)

### AUTH Routes ###
api.add_resource(Login, '/login',
    resource_class_kwargs={ 'db': db })
api.add_resource(Refresh, '/refresh')
api.add_resource(Logout, '/logout')

### Project Routes ###
api.add_resource(Projects, '/projects',
    resource_class_kwargs={ 'db': db })
api.add_resource(Project, '/project/<int:project_id>',
    resource_class_kwargs={ 'db': db })
api.add_resource(Section, '/section/<int:section_id>',
    resource_class_kwargs={ 'db': db })
api.add_resource(Task, '/task/<int:task_id>',
    resource_class_kwargs={ 'db': db })


### SCHEDULE Routes ###
api.add_resource(Item, '/item/<int:item_id>', '/item',
    resource_class_kwargs={ 'db': db })
api.add_resource(Day, '/day/<string:get_date>',
    resource_class_kwargs={ 'db': db })
api.add_resource(Today, '/today',
    resource_class_kwargs={ 'db': db })
api.add_resource(Week, '/week', '/week/<string:get_date>',
    resource_class_kwargs={ 'db': db })

if __name__ == '__main__':
    app.run(debug=True, port=5001)