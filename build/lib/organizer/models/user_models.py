import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from passlib.apps import custom_app_context as pwd_context

UserBase = declarative_base()

class User(UserBase):
    __tablename__ = 'users'
    id = sql.Column(sql.Integer, primary_key=True)
    username = sql.Column(sql.String, unique=True)
    password_hash = sql.Column(sql.String)
    roles = sql.Column(sql.String)
    email = sql.Column(sql.String)
    data = sql.Column(sql.String)