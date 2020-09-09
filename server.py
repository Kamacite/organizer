import os
from datetime import *
import json
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import post_load, fields, validate
import models


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'schedule.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)

ritem = models.Item

class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ritem
        include_fk = True

    title = fields.Str(validate=validate.Length(min=1))
    details = fields.Str()
    item_date = fields.Str(validate=validate.Length(min=1))
    item_time = fields.Str(validate=validate.Length(min=1))
    last_update = ma.auto_field()
    owner = ma.auto_field()
    active = ma.auto_field()
    reoccuring = ma.auto_field()


    @post_load
    def make_item(self, data, **kwargs):
        return ritem(**data)

item_schema = ItemSchema()

class Item(Resource):
    
    def get(self, item_id=0):
        try:
            item = db.session.query(ritem).filter(ritem.id == item_id)[0]
        except:
            abort(404, message="Item does not exist")
        if item.active:
            return item_schema.dump(item)
           
        else:
            abort(404, message="Item does not exist")

    def put(self, item_id=0):
        if item_id == 0:
            error = item_schema.validate(request.json)
            if error:
                abort(400, message=str(error))
            item = item_schema.load(request.json)
            item.last_update = datetime.now().isoformat()
            db.session.add(item)
            db.session.commit()
            return item_schema.dump(item)
        else:
            error = item_schema.validate(request.json)
            if error:
                abort(400, message=str(error))
            item = db.session.query(ritem).filter(ritem.id == item_id).one()
            changes = item_schema.load(request.json) 
            item.title = changes.title
            item.details = changes.details
            item.item_date = changes.item_date
            item.item_time = changes.item_time
            item.last_update = datetime.now().isoformat()
            db.session.commit()
            return item_schema.dump(item)

class Day(Resource):
    def get(self, get_date):
        cur_date = date.fromisoformat(get_date)
        items = db.session.query(ritem)\
            .filter(ritem.item_date == cur_date.isoformat())\
            .order_by(ritem.item_time.asc())\
            .all()
        result = []
        for item in items:
            result.append(item_schema.dump(item))
        
        return jsonify(result)

class Today(Resource):
    def get(self):
        cur_date = date.today()
        items = db.session.query(ritem)\
            .filter(ritem.item_date == cur_date.isoformat())\
            .order_by(ritem.item_time.asc())\
            .all()
        result = []
        for item in items:
            result.append(item_schema.dump(item))
        
        return jsonify(result)

class Week(Resource):
    def get(self, get_date=None):
        if get_date is None:
            cur_date = date.today()
        else:
            cur_date = date.fromisoformat(get_date)
        weektd = timedelta(weeks=1)
        end_week = cur_date + weektd
        items = db.session.query(ritem)\
            .filter(ritem.item_date <= end_week.isoformat(), ritem.item_date >= cur_date.isoformat())\
            .order_by(ritem.item_date.asc(),ritem.item_time.asc())\
            .all()
        result = []
        for item in items:
            result.append(item_schema.dump(item))
        
        return jsonify(result)
        

api.add_resource(Item, '/item/<int:item_id>', '/item')
api.add_resource(Day, '/day/<string:get_date>')
api.add_resource(Today, '/today')
api.add_resource(Week, '/week', '/week/<string:get_date>')

if __name__ == '__main__':
    app.run(debug=True)