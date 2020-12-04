from flask import jsonify, request, abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.user_models import *
from ..models.project_models import *
from ..models.schedule_models import *
from passlib.apps import custom_app_context as pwd_context
from organizer_api import db


class Users(MethodView):
    
    #check if user has admin role
    def _check_admin_role(self, user_id):
        is_admin = False
        try:
            admin = db.session.query(User).filter(User.id == user_id).one()
        except:
            abort(404)
        roles = admin.roles.split(",")
        for role in roles:
            if role == "admin":
                is_admin = True
        return is_admin

    #list of all users plus their id and roles
    @jwt_required
    def get(self):
        admin_id = get_jwt_identity()
        #check if user has admin role
        is_admin = self._check_admin_role(admin_id)
        #if admin, get all users and return
        if(is_admin):
            result = []
            try:
                users = db.session.query(User).all()
            except:
                abort(404)
            for user in users:
                result.append({"username":user.username, "id": user.id, "roles": user.roles})
            resp = jsonify(result)
            resp.status_code = 200
            return resp
        else:
            abort(403)

    #update user (new username, new password, and/or new role)
    @jwt_required
    def patch(self, user_id):
        #check_admin
        admin_id = get_jwt_identity()
        #check if user has admin role
        is_admin = self._check_admin_role(admin_id)
        #if admin, get all users and return
        if(is_admin):
            patch_data = request.json
        #check target user exists
        try:
            user = db.session.query(User).filter(User.id == user_id).one()
        except:
            abort(404)
        #patch user
        user_updates = request.json
        if ("username" in user_updates):
            user.username = user_updates["username"]
        if ("password" in user_updates):
            user.password_hash = pwd_context.hash(user_updates["password"])
        if ("roles" in user_updates):
            if (admin_id == user_id):
                check_roles = user_updates["roles"].split(",")
                if "admin" not in check_roles:
                    resp = jsonify({"message": "Cannot remove admin role from own account."})
                    resp.status_code = 403
                    return resp
            user.roles = user_updates["roles"]
        db.session.commit()
        resp = jsonify({"message": "User successfully updated"})
        resp.status_code = 200
        return resp

    #delete users and anything related to user
    @jwt_required
    def delete(self, user_id):
        #check admin
        admin_id = get_jwt_identity()
        if (admin_id == user_id):
            resp = jsonify({"message":"Cannot delete own account."})
            resp.status_code = 403
            return resp
        #check if user has admin role
        is_admin = self._check_admin_role(admin_id)
        #if admin, get all users and return
        if(is_admin):
            #check target user exists
            try:
                user = db.session.query(User).filter(User.id == user_id).one()
            except:
                abort(404)
            #delete project items
            try:
                projects = db.session.query(Project).filter(Project.owner_id == user_id).all()
                for project in projects:
                    db.session.delete(project)
                db.session.commit()
            except:
                pass
            #delete schedule items
            try:
                sched_items = db.session.query(Item).filter(Item.owner == user_id).all()
                for item in sched_items:
                    db.session.delete(item)
                db.session.commit()
            except:
                pass
            #delete user
            db.session.delete(user)
            db.session.commit()
            resp = jsonify({"message": "User successfully deleted."})
            resp.status_code = 200
            return resp
        else:
            abort(403)