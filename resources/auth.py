from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,jwt_refresh_token_required, 
    create_refresh_token,set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)
from passlib.apps import custom_app_context as pwd_context
from models.user_models import User


class Login(Resource):
    def __init__(self, **kwargs):
        self.db = kwargs['db']

    def post(self):
        content = request.json
        username = content['username']
        password = content['password']
        try:
            user = self.db.session.query(User).filter(User.username == username).one()
        except:
            resp = jsonify({'login': False})
            resp.status_code = 401
            return resp
        if user and pwd_context.verify(password, user.password_hash):
            
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            
            resp = jsonify({'login': True})
           
            set_access_cookies(resp, access_token)
            set_refresh_cookies(resp, refresh_token)
            
            return resp

        else:
            resp = jsonify({'login': False})
            resp.status_code = 401
            return resp

class Logout(Resource):
    def post(self):
        resp = jsonify({'logout': True})
        unset_jwt_cookies(resp)
        resp.status_code = 200
        return resp