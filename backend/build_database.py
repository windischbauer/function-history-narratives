import os
from config import db
from sqlalchemy.ext.declarative import declarative_base

# Delete database file if it exists currently
import models
import schemas

if os.path.exists('mhg-sqlite.db'):
    os.remove('mhg-sqlite.db')

# Create the database
db.create_all()


# u = User(username='test', email='email')
# db.session.add(u)

db.session.commit()
