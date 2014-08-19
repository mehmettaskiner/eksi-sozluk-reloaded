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

	def tearDown(self):
		db.session.remove()
		db.drop_all()

if __name__ == '__main__':
	unittest.main()