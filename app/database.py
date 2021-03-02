import os
from app import app
from flask_sqlalchemy import SQLAlchemy


db_path = os.path.join(os.path.dirname(__file__), '..', 'database.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
