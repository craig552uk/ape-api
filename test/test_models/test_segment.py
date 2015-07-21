# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Unit Tests for Segment Model

import unittest
from app import db
from app.models import Segment

class TestModelSegment(unittest.TestCase):

    def test_segment_crud(self):
        # Create
        segment = Segment(name='Foo')
        db.session.add(segment)
        db.session.commit()
        self.assertIn(segment, Segment.query.all())

        # Read
        segment = Segment.query.filter_by(name='Foo').first()
        self.assertEqual(segment.name, 'Foo')
        
        # Update
        segment.name = 'Bar'
        segment = Segment.query.filter_by(name='Bar').first()
        self.assertIsInstance(segment, Segment)
        self.assertEqual('Bar', segment.name)

        # Delete
        db.session.delete(segment)
        count = Segment.query.filter_by(name='Bar').count()
        self.assertEqual(0, count)