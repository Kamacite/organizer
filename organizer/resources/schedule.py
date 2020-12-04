import os, sys
from flask import jsonify, request, abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import *
from ..models.schedule_schemas import item_schema
from ..models.schedule_models import Item as mItem
from organizer import db

class Item(MethodView):
    
    @jwt_required
    def get(self, item_id=0):
        user_id = get_jwt_identity()
        try:
            item = db.session.query(mItem).filter(mItem.id == item_id, mItem.owner == user_id)[0]
        except:
            abort(404)
        if item.active:
            return item_schema.dump(item)
           
        else:
            abort(404)
    @jwt_required
    def put(self, item_id=0):
        user_id = get_jwt_identity()
        if item_id == 0:
            error = item_schema.validate(request.json, session=db.session)
            if error:
                abort(400)
            item = item_schema.load(request.json)
            item.last_update = datetime.now().isoformat()
            item.owner = user_id
            db.session.add(item)
            db.session.commit()
            return item_schema.dump(item)
        else:
            error = item_schema.validate(request.json, session=db.session)
            if error:
                abort(400)
            item = db.session.query(mItem).filter(mItem.id == item_id, mItem.owner == user_id).one()
            changes = item_schema.load(request.json) 
            item.title = changes.title
            item.details = changes.details
            item.item_date = changes.item_date
            item.item_time = changes.item_time
            item.last_update = datetime.now().isoformat()
            db.session.commit()
            return item_schema.dump(item)

    @jwt_required
    def delete(self, item_id):
        user_id = get_jwt_identity()
        try:
            item = db.session.query(mItem).filter(mItem.id == item_id, mItem.owner == user_id).one()
        except:
            abort(404)
        db.session.delete(item)
        db.session.commit()
        return item_schema.dump(item)

class Day(MethodView):

    @jwt_required
    def get(self, get_date):
        user_id = get_jwt_identity()
        cur_date = date.fromisoformat(get_date)
        items = db.session.query(mItem)\
            .filter(mItem.item_date == cur_date.isoformat(), mItem.owner == user_id)\
            .order_by(mItem.item_time.asc())\
            .all()
        result = []
        for item in items:
            result.append(item_schema.dump(item))
        
        return jsonify(result)

class Today(MethodView):

    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        cur_date = date.today()
        items = db.session.query(mItem)\
            .filter(mItem.item_date == cur_date.isoformat(), mItem.owner == user_id)\
            .order_by(mItem.item_time.asc())\
            .all()
        result = []
        for item in items:
            result.append(item_schema.dump(item))
        
        return jsonify(result)

class Week(MethodView):

    @jwt_required
    def get(self, get_date=None):
        user_id = get_jwt_identity()
        if get_date is None:
            cur_date = date.today()
        else:
            cur_date = date.fromisoformat(get_date)
        weektd = timedelta(weeks=1)
        end_week = cur_date + weektd
        items = db.session.query(mItem)\
            .filter(mItem.item_date <= end_week.isoformat(), mItem.item_date >= cur_date.isoformat(), mItem.owner == user_id)\
            .order_by(mItem.item_date.asc(),mItem.item_time.asc())\
            .all()
        result = []
        for item in items:
            result.append(item_schema.dump(item))
        
        return jsonify(result)
