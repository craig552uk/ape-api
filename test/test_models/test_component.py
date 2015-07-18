# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Unit Tests for Component Model

import unittest
from app import db
from app.models import Component

class TestModelComponent(unittest.TestCase):

    def test_component_crud(self):
        # Create
        component = Component(name='Foo')
        db.session.add(component)
        db.session.commit()
        self.assertIn(component, Component.query.all())

        # Read
        component = Component.query.filter_by(name='Foo').first()
        self.assertEqual(component.name, 'Foo')
        
        # Update
        component.name = 'Bar'
        component = Component.query.filter_by(name='Bar').first()
        self.assertIsInstance(component, Component)
        self.assertEqual('Bar', component.name)

        # Delete
        db.session.delete(component)
        count = Component.query.filter_by(name='Bar').count()
        self.assertEqual(0, count)