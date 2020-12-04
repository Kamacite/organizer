from ..models.user_models import *
from ..models.project_models import *
from ..models.schedule_models import *
from passlib.apps import custom_app_context as pwd_context


def get_user_ids():
    #list all users and their id
    pass

def delete_user(user_id):
    #delete all schedule items and projects belonging to user
    #delete user
    pass

def change_password(user_id, password):
    #get user id
    #update password hash
    pass