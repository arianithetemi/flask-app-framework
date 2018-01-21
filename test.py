import unittest, json
from flask_testing import TestCase
from app import create_app, db

class BaseTestCase(TestCase):

    ############################
    #### setup flask app and teardown ####
    ############################

    def create_app(self):
        return create_app()

    # executed prior to each test
    def setUp(self):
        db.create_all()

    # executed after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()


###############
#### tests ####
###############

class FlaskTestCase(BaseTestCase):

    def test_index(self):
        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_main(self):
        response = self.client.get('/', follow_redirects=True)
        self.assertIn(b'Welcome to the Flask App.', response.data)

if __name__ == "__main__":
    unittest.main()
