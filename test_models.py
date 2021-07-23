from app import app
import os
from flask import session
from unittest import TestCase
from models import db, connect_db, User, Job

os.environ["DATABASE_URL"] = "postgresql:///jobSearch-test"

db.create_all()

class UserTestCase(TestCase):
    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        user = User.signup(first_name="testfirst",
                            last_name="testlast",
                            username="testuser",
                            email="test@user.com",
                            password="testpass",
                            profile_img=None,                            
                            location="location")
        id = 90
        user.id = id       

        db.session.commit()

        self.user = user
        self.id = id

        self.client = app.test_client()

    def test_authenticate(self):
        user = User.authenticte(self.user.username, "password")    
        self.assertIsNotNone(user)

        self.assertFalse(User.authenticte("badusername", "password"))

        self.assertFalse(User.authenticte(self.user.usernam, "badpassword"))
