# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Unit Tests for app

import unittest
from app import db
from app.models import User

class TestModelUser(unittest.TestCase):

    def test_crud(self):
        # Create
        user = User(name='Foo')
        db.session.add(user)
        db.session.commit()
        self.assertIn(user, User.query.all())

        # Read
        user = User.query.filter_by(name='Foo').first()
        self.assertEqual(user.name, 'Foo')
        
        # Update
        user.name = 'Bar'
        user = User.query.filter_by(name='Bar').first()
        self.assertIsInstance(user, User)
        self.assertEqual('Bar', user.name)

        # Delete
        db.session.delete(user)
        count = User.query.filter_by(name='Bar').count()
        self.assertEqual(0, count)