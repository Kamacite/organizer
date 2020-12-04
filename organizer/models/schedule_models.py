import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

ScheduleBase = declarative_base()

class Item(ScheduleBase):
    __tablename__ = 'items'
    id = sql.Column(sql.Integer, primary_key=True)
    title = sql.Column(sql.String(length=32))
    details = sql.Column(sql.String)
    item_date = sql.Column(sql.String)
    item_time = sql.Column(sql.String)
    last_update = sql.Column(sql.String)
    owner = sql.Column(sql.Integer)
    active = sql.Column(sql.Boolean)
    reoccuring = sql.Column(sql.Boolean)

    def __repr__(self):
        return "<Item=%s" % (self.details)