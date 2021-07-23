from app import app
import os
from flask import session
from unittest import TestCase
from models import db, connect_db, Jobseeker, Recruiter, Event

os.environ["DATABASE_URL"] = "postgresql:///jobSearch-test"

db.create_all()
