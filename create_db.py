import os
import models as db
from datetime import *

basedir = os.path.abspath(os.path.dirname(__file__))
db_name = "schedule.db"
uri = "sqlite:///" + basedir + "/" + db_name

sess = db.connect(uri)

