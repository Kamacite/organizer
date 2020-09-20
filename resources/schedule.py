import os, sys
from flask import jsonify, request
from flask_restful import Resource, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import *
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from models.schedule_schemas import item_schema
from models.schedule_models import Item as mItem

class Item(Resource):

    def __init__(self, **kwargs):
        self.db = kwargs['db']
        
    @jwt_required
    def get(self, item_id=0):
        user_id = get_jwt_identity()
        try:
            item = self.db.session.query(mItem).filter(mItem.id == item_id, mItem.owner == user_id)[0]
        except:
            abort(404, message="Item does not exist")
        if item.active:
            return item_schema.dump(item)
           
        else:
            abort(404, message="Item does not exist")
    @jwt_required
    def put(self, item_id=0):
        user_id = get_jwt_identity()
        if item_id == 0:
            error = item_schema.validate(request.json, session=self.db.session)
            if error:
                abort(400, message=str(error))
            item = item_schema.load(request.json)
            item.last_update = datetime.now().isoformat()
            item.owner = user_id
            self.db.session.add(item)
            self.db.session.commit()
            return item_schema.dump(item)
        else:
            error = item_schema.validate(request.json, session=self.db.session)
            if error:
                abort(400, message=str(error))
            item = self.db.session.query(mItem).filter(mItem.id == item_id, mItem.owner == user_id).one()
            changes = item_schema.load(request.json) 
            item.title = changes.title
            item.details = changes.details
            item.item_date = changes.item_date
            item.item_time = changes.item_time
            item.last_update = datetime.now().isoformat()
            self.db.session.commit()
            return item_schema.dump(item)

class Day(Resource):

    def __init__(self, **kwargs):
        self.db = kwargs['db']

    @jwt_required
    def get(self, get_date):
        user_id = get_jwt_identity()
        cur_date = date.fromisoformat(get_date)
        items = self.db.session.query(mItem)\
            .filter(mItem.item_date == cur_date.isoformat(), mItem.owner == user_id)\
            .order_by(mItem.item_time.asc())\
            .all()
        result = []
        for item in items:
            result.append(item_schema.dump(item))
        
        return jsonify(result)

class Today(Resource):

    def __init__(self, **kwargs):
        self.db = kwargs['db']

    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        cur_date = date.today()
        items = self.db.session.query(mItem)\
            .filter(mItem.item_date == cur_date.isoformat(), mItem.owner == user_id)\
            .order_by(mItem.item_time.asc())\
            .all()
        result = []
        for item in items:
            result.append(item_schema.dump(item))
        
        return jsonify(result)

class Week(Resource):

    def __init__(self, **kwargs):
        self.db = kwargs['db']

    @jwt_required
    def get(self, get_date=None):
        user_id = get_jwt_identity()
        if get_date is None:
            cur_date = date.today()
        else:
            cur_date = date.fromisoformat(get_date)
        weektd = timedelta(weeks=1)
        end_week = cur_date + weektd
        items = self.db.session.query(mItem)\
            .filter(mItem.item_date <= end_week.isoformat(), mItem.item_date >= cur_date.isoformat(), mItem.owner == user_id)\
            .order_by(mItem.item_date.asc(),mItem.item_time.asc())\
            .all()
        result = []
        for item in items:
            result.append(item_schema.dump(item))
        
        return jsonify(result)
