#!flask/bin/python
import os
import unittest

from config import basedir
from app import app, db

class TestCase(unittest.TestCase):
	def setUp(self):
		app.config['TESTING'] = True
		app.config['CSRF_ENABLED'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

    # every def will be a test

if __name__ == '__main__':
	unittest.main()