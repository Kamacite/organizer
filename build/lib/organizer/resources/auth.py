from flask import jsonify, request
from flask.views import MethodView
from flask_jwt_extended import (
    create_access_token,jwt_refresh_token_required, 
    create_refresh_token,set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies, get_jwt_identity
)
from passlib.apps import custom_app_context as pwd_context
from ..models.user_models import User
from organizer import db

class Login(MethodView):

    def post(self):
        content = request.json
        username = content['username']
        password = content['password']
        try:
            user = db.session.query(User).filter(User.username == username).one()
        except:
            resp = jsonify({'login': False})
            resp.status_code = 401
            return resp

        if user and pwd_context.verify(password, user.password_hash):
            
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            
            resp = jsonify({'login': True, 'roles': user.roles})
           
            set_access_cookies(resp, access_token)
            set_refresh_cookies(resp, refresh_token)
            
            return resp

        else:
            resp = jsonify({'login': False})
            resp.status_code = 401
            return resp

class Refresh(MethodView):
    @jwt_refresh_token_required
    def post(self):
        user_id = get_jwt_identity()
        access_token = create_access_token(identity=user_id)
        resp = jsonify({'refresh': True})
        resp.status_code = 200
        set_access_cookies(resp, access_token)
        return resp


class Logout(MethodView):
    def post(self):
        resp = jsonify({'logout': True})
        unset_jwt_cookies(resp)
        resp.status_code = 200
        return resp

class Register(MethodView):
    def post(self):
        
        new_user_data = request.json
        username = new_user_data['username']
        password = new_user_data['password']
        #check if username already exists
        try:
            user = db.session.query(User).filter(User.username == username).one()
        except:
            user = None
        #If yes return
        if(user is not None):
            resp = jsonify({'message': 'Username already in use.'})
            resp.status_code = 403
            return resp
        #else create user, hash password, return 200
        new_user = User()
        new_user.username = username
        new_user.password_hash = pwd_context.hash(password)
        new_user.roles = 'user'
        db.session.add(new_user)
        try:
            db.session.commit()
        except:
            abort(500)
        resp = jsonify({'message': 'User successfully registered'})
        resp.status_code = 200
        return resp