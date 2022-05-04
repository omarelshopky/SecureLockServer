import sys, os
sys.path.append(os.path.abspath(os.path.join('..')))
from main import db

from sqlalchemy.dialects.postgresql import UUID

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(UUID(as_uuid=True), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(11))
    address = db.Column(db.String(200))
# run db.create_all(app=) to affect the sqlite db
