import os, sys
from marshmallow import post_load, fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from models.schedule_models import Item

class ItemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Item
        include_fk = True

    title = fields.Str(validate=validate.Length(min=1))
    details = fields.Str()
    item_date = fields.Str(validate=validate.Length(min=1))
    item_time = fields.Str(validate=validate.Length(min=1))
    last_update = auto_field()
    owner = auto_field()
    active = auto_field()
    reoccuring = auto_field()


    @post_load
    def make_item(self, data, **kwargs):
        return Item(**data)

item_schema = ItemSchema()