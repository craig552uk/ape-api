# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Unit Tests for Demographic Model

import unittest
from app import db
from app.models import Demographic

class TestModelDemographic(unittest.TestCase):

    def test_crud(self):
        # Create
        demographic = Demographic(name='Foo')
        db.session.add(demographic)
        db.session.commit()
        self.assertIn(demographic, Demographic.query.all())

        # Read
        demographic = Demographic.query.filter_by(name='Foo').first()
        self.assertEqual(demographic.name, 'Foo')
        
        # Update
        demographic.name = 'Bar'
        demographic = Demographic.query.filter_by(name='Bar').first()
        self.assertIsInstance(demographic, Demographic)
        self.assertEqual('Bar', demographic.name)

        # Delete
        db.session.delete(demographic)
        count = Demographic.query.filter_by(name='Bar').count()
        self.assertEqual(0, count)