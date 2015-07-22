# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Unit Tests for Component Model

import unittest
import datetime as DT
from app import db
from app.models import Component

class TestModelComponent(unittest.TestCase):

    def test_component_crud(self):
        # Create
        component = Component(name='Foo', index=5, markup="<h1>Hello</h1>")
        db.session.add(component)
        db.session.commit()
        self.assertIn(component, Component.query.all())
        self.assertIsInstance(component.index, int)
        self.assertIsInstance(component.markup, unicode)
        self.assertIsInstance(component.created_at, DT.datetime)
        self.assertIsInstance(component.updated_at, DT.datetime)

        # Read
        component = Component.query.filter_by(name='Foo').first()
        self.assertEqual(component.name, 'Foo')
        self.assertEqual(component.index, 5)
        self.assertEqual(component.markup, "<h1>Hello</h1>")
        
        # Update
        old_created_at = component.created_at
        old_updated_at = component.updated_at
        component.name   = 'Bar'
        component.index  = 7
        component.markup = "<h2>Bye</h2>"
        component = Component.query.filter_by(name='Bar').first()
        self.assertIsInstance(component, Component)
        self.assertEqual(component.name, "Bar")
        self.assertEqual(component.index, 7)
        self.assertEqual(component.markup, "<h2>Bye</h2>")
        self.assertEqual(component.created_at, old_created_at)
        self.assertNotEqual(component.updated_at, old_updated_at)

        # Delete
        db.session.delete(component)
        count = Component.query.filter_by(name='Bar').count()
        self.assertEqual(0, count)