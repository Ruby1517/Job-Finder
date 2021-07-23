from app import app, CURR_USER_KEY
import os
from flask import session, Flask
from unittest import TestCase
from models import db, connect_db, User, Job

os.environ["DATABASE_URI"] = "postgresql:///jobSearch-app"
db.drop_all()
db.create_all()

class JobSearchTestCase(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app


    def setUp(self):

        Job.query.delete()
        User.query.delete()  

        self.client = app.test_client()         
              
        self.testuser = User.signup(first_name="test",
                                    last_name="tester",
                                    username="usertest",
                                    email="test@user.com",
                                    password="password",
                                    profile_img=None,
                                    location="location")
        self.testuser_id = 4680
        self.testuser.id = self.testuser_id       
        db.session.commit() 

    def test_starter_page(self):
        """ Ensuring homepage works"""

        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1 class="display-1">Job search App</h1>', html)


    def test_logout(self):
        with app.test_client() as client:
            resp = client.get('/logout')
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "http://localhost/login")    



    def test_login(self):
        with app.test_client() as client:
            resp = client.post('/login', data={
                'username': 'usertest',
                'password':'password'}, follow_redirects=True)             

            self.assertEqual(resp.status_code, 200)             
            self.assertIn('Welcome', resp.get_data(as_text=True))
    
    def test_favorites(self):
        """Make sure user can access Favorites Page."""

        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = client.get(f"/users/{self.testuser.id}/favorites")
            html = resp.get_data(as_text=True)
            self.assertIn('Favorite Jobs List', html)


    def test_searchpage(self):
        """ Show search page after user login"""
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id 
                resp = client.get("/users/search")
                html = resp.get_data(as_text=True)
                self.assertIn('Search desierd job', html)

    def test_searchpage(self):
        """ post job title and location for search job after user login"""

        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id 
                
                resp = client.post("/users/search", data={
                                'title': 'software engineer',
                                'location':'fresno'})                               

                html = resp.get_data(as_text=True)
                self.assertEqual(resp.status_code, 200)
                
                
