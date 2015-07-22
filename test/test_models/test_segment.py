# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Unit Tests for Segment Model

import unittest
import datetime as DT
from app import db
from app.models import Segment

class TestModelSegment(unittest.TestCase):

    def test_segment_crud(self):
        # Create
        segment = Segment(name='Foo')
        db.session.add(segment)
        db.session.commit()
        self.assertIn(segment, Segment.query.all())
        self.assertIsInstance(segment.created_at, DT.datetime)
        self.assertIsInstance(segment.updated_at, DT.datetime)

        # Read
        segment = Segment.query.filter_by(name='Foo').first()
        self.assertEqual(segment.name, 'Foo')
        
        # Update
        old_created_at = segment.created_at
        old_updated_at = segment.updated_at
        segment.name = 'Bar'
        segment = Segment.query.filter_by(name='Bar').first()
        self.assertIsInstance(segment, Segment)
        self.assertEqual('Bar', segment.name)
        self.assertEqual(segment.created_at, old_created_at)
        self.assertNotEqual(segment.updated_at, old_updated_at)

        # Delete
        db.session.delete(segment)
        count = Segment.query.filter_by(name='Bar').count()
        self.assertEqual(0, count)