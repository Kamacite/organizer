from models import User
from passlib.apps import custom_app_context as pwd_context
from create_db import *

def hash_password(password):
    return pwd_context.encrypt(password)