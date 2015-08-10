# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Unit Tests for Placeholder Model

import unittest
import datetime as DT
from app import db
from app.models import Placeholder, Segment, Component

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

    def test_get_component_for_segments(self):
        segment_1 = Segment()
        segment_2 = Segment()
        segment_3 = Segment()
        segment_4 = Segment()
        component_1 = Component(index=1, segment=segment_1)
        component_2 = Component(index=2, segment=segment_2)
        component_3 = Component(index=3, segment=segment_3)
        placeholder = Placeholder()
        placeholder.components.append(component_3)
        placeholder.components.append(component_2)
        placeholder.components.append(component_1)
        db.session.add(placeholder)
        db.session.commit()

        self.assertEqual(component_1, placeholder.get_component_for_segments([segment_1]))
        self.assertEqual(component_1, placeholder.get_component_for_segments([segment_1, segment_2]))
        self.assertEqual(component_2, placeholder.get_component_for_segments([segment_4, segment_2]))
        self.assertEqual(component_2, placeholder.get_component_for_segments([segment_2]))
        self.assertIsNone(placeholder.get_component_for_segments([segment_4]))
        self.assertIsNone(placeholder.get_component_for_segments([]))

