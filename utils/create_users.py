import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from models.user_models import *
from passlib.apps import custom_app_context as pwd_context
from create_db import *

def hash_password(password):
    return pwd_context.hash(password)

if __name__ == '__main__':
    username = input("Enter username:")
    passw = input("Enter password:")

    user = User()
    user.username = username
    user.password_hash = hash_password(passw)

    sess = connect(uri)

    sess.add(user)
    sess.commit()