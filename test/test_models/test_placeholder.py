# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Unit Tests for Placeholder Model

import unittest
import datetime as DT
from app import db
from app.models import Placeholder

class TestModelPlaceholder(unittest.TestCase):

    def test_placeholder_crud(self):
        # Create
        placeholder = Placeholder(name='Foo')
        db.session.add(placeholder)
        db.session.commit()
        self.assertIn(placeholder, Placeholder.query.all())
        self.assertIsInstance(placeholder.uuid, unicode)
        self.assertIsInstance(placeholder.created_at, DT.datetime)
        self.assertIsInstance(placeholder.updated_at, DT.datetime)

        # Read
        placeholder = Placeholder.query.filter_by(name='Foo').first()
        self.assertEqual(placeholder.name, 'Foo')
        
        # Update
        old_created_at = placeholder.created_at
        old_updated_at = placeholder.updated_at
        placeholder.name = 'Bar'
        placeholder = Placeholder.query.filter_by(name='Bar').first()
        self.assertIsInstance(placeholder, Placeholder)
        self.assertEqual('Bar', placeholder.name)
        self.assertEqual(placeholder.created_at, old_created_at)
        self.assertNotEqual(placeholder.updated_at, old_updated_at)

        # Delete
        db.session.delete(placeholder)
        count = Placeholder.query.filter_by(name='Bar').count()
        self.assertEqual(0, count)