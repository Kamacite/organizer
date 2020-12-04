import os, sys
import sqlalchemy as sql
from sqlalchemy.orm import sessionmaker
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from models.schedule_models import *
from models.user_models import *
from models.project_models import *
from passlib.apps import custom_app_context as pwd_context

basedir = os.path.abspath(os.path.dirname(__file__))
db_name = "organizer.db"
uri = "sqlite:///" + basedir + "/" + db_name

def connect(uri):
    engine = sql.create_engine(uri)
    Session = sessionmaker(bind=engine)
    session = Session()

    UserBase.metadata.create_all(engine)
    ProjectBase.metadata.create_all(engine)
    ScheduleBase.metadata.create_all(engine)

    return session

if __name__ == "__main__":
    sess = connect(uri)
    admin = User()
    admin.username = "admin"
    admin.roles = "admin"
    admin.password_hash = pwd_context.hash("change_admin_password")
    sess.add(admin)
    sess.commit()