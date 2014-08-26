#!flask/bin/python
#-*- coding: utf-8 -*-
import os
import unittest

from config import basedir
from app import app, db
from app.models import User, Entry, Title
from datetime import datetime, timedelta
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

    def test_follow(self):
        u1 = User(nickname = 'tayyip')
        u2 = User(nickname = 'kkilicdaroglu')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        assert u1.unfollow(u2) == None
        u = u1.follow(u2)
        db.session.add(u)
        db.session.commit()
        assert u1.follow(u2) == None
        assert u1.is_following(u2)
        assert u1.followed.count() == 1
        assert u1.followed.first().nickname == 'kkilicdaroglu'
        assert u2.followers.count() == 1
        assert u2.followers.first().nickname == 'tayyip'
        u = u1.unfollow(u2)
        assert u != None
        db.session.add(u)
        db.session.commit()
        assert u1.is_following(u2) == False
        assert u1.followed.count() == 0
        assert u2.followers.count() == 0

if __name__ == '__main__':
	unittest.main()




