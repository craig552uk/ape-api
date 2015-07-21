# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Unit Tests for User Model

import unittest
import datetime as DT
from app import db
from app.models import User

class TestModelUser(unittest.TestCase):

    def test_user_crud(self):
        # Create
        user = User(name='Foo', email='a@b.com', password='passw0rd')
        db.session.add(user)
        db.session.commit()
        self.assertIn(user, User.query.all())
        self.assertIsInstance(user.name, unicode)
        self.assertIsInstance(user.email, unicode)
        self.assertIsInstance(user.password, unicode)
        self.assertIsInstance(user.enabled, bool)
        self.assertIsInstance(user.admin, bool)
        self.assertIsInstance(user.created_at, DT.datetime)
        self.assertIsInstance(user.updated_at, DT.datetime)
        self.assertIsInstance(user.last_login, type(None)) # No timestamp before first login

        # Read
        user = User.query.filter_by(name='Foo').first()
        self.assertEqual(user.name, 'Foo')
        self.assertEqual(user.email, 'a@b.com')
        self.assertEqual(user.password, 'passw0rd')
        self.assertTrue(user.enabled)
        self.assertFalse(user.admin)
        
        # Update
        old_created_at  = user.created_at
        old_updated_at  = user.updated_at
        user.name       = 'Bar'
        user.email      = 'c@d.com'
        user.password   = 'qwerty'
        user.enabled    = False
        user.admin      = True
        user.last_login = DT.datetime.now()
        user = User.query.filter_by(name='Bar').first()
        self.assertIsInstance(user, User)
        self.assertEqual('Bar', user.name)
        self.assertEqual(user.email, 'c@d.com')
        self.assertEqual(user.password, 'qwerty')
        self.assertFalse(user.enabled)
        self.assertTrue(user.admin)
        self.assertEqual(user.created_at, old_created_at)
        self.assertNotEqual(user.updated_at, old_updated_at)
        self.assertIsInstance(user.last_login, DT.datetime)

        # Delete
        db.session.delete(user)
        count = User.query.filter_by(name='Bar').count()
        self.assertEqual(0, count)