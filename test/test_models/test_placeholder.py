# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Unit Tests for Placeholder Model

import unittest
from app import db
from app.models import Placeholder

class TestModelPlaceholder(unittest.TestCase):

    def test_placeholder_crud(self):
        # Create
        placeholder = Placeholder(name='Foo')
        db.session.add(placeholder)
        db.session.commit()
        self.assertIn(placeholder, Placeholder.query.all())

        # Read
        placeholder = Placeholder.query.filter_by(name='Foo').first()
        self.assertEqual(placeholder.name, 'Foo')
        
        # Update
        placeholder.name = 'Bar'
        placeholder = Placeholder.query.filter_by(name='Bar').first()
        self.assertIsInstance(placeholder, Placeholder)
        self.assertEqual('Bar', placeholder.name)

        # Delete
        db.session.delete(placeholder)
        count = Placeholder.query.filter_by(name='Bar').count()
        self.assertEqual(0, count)