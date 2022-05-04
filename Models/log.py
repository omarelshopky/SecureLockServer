import sys, os
sys.path.append(os.path.abspath(os.path.join('..')))
from main import db


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    unlocking_method = db.Column(db.String(80), nullable=False)
    date_time = db.Column(db.DateTime(timezone=True), default=db.func.now())

    