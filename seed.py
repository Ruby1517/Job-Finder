from models import db, Job, User
from app import app

db.drop_all()
db.create_all()
