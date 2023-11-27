"""Sample test suite for testing demo."""

from unittest import TestCase
from app import app, get_recipe
from models import db, User
from flask import session

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///spoontaneous_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True
# app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class Tests(TestCase):

    def setUp(self):

        db.drop_all()
        db.create_all()

        self.testuser = User.register(username='testuser', password='testuser')
        db.session.add(self.testuser)
        db.session.commit()
        
    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp

    def test_home_page(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('SPOONTANEOUS</h1>', html)

    def test_register(self):
        with app.test_client() as client:
            resp = client.get('/register')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Signup', html)

    def test_login(self):
        with app.test_client() as client:
            resp = client.get('/login')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Login', html)

    def test_recipe_page(self):
        with app.test_client() as client:
            resp = client.get('/recipe/52814')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)

    def test_get_recipe(self):
        resp = get_recipe('52814')

        self.assertIn('Thai Green Curry',str(resp))
        self.assertIn('4 tsp',str(resp))
        self.assertIn('Put the potatoes in a pan of boiling water',str(resp))
            
