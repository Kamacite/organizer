import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from models.schedule_models import *
from models.user_models import *

basedir = os.path.abspath(os.path.dirname(__file__))
db_name = "organizer123.db"
uri = "sqlite:///" + basedir + "/" + db_name

def create_db(uri):
    engine = sql.create_engine(uri)
    Base.metadata.create_all(engine)

    return True

if __name__ == "__main__":
    create_db(uri)