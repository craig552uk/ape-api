# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Unit Tests for Segment Model

import unittest
import datetime as DT
from app import db
from app.models import Segment, Rule
from app.helpers import factory

class TestModelSegment(unittest.TestCase):

    def setUp(self):
        self.visitor_data = factory.make_visitor_data()

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

    def test_segment_matches_data(self):
        segment      = Segment(name="Foo")
        true_rule_1  = Rule(group_id=1, field='sessions_count', comparator="MATCH", value=self.visitor_data['sessions_count'])
        false_rule_1 = Rule(group_id=1, field='sessions_count', comparator="MATCH", value=100)
        true_rule_2  = Rule(group_id=2, field='sessions_count', comparator="MATCH", value=self.visitor_data['sessions_count'])
        false_rule_2 = Rule(group_id=2, field='sessions_count', comparator="MATCH", value=100)
        
        # True
        segment.rules = [true_rule_1]
        self.assertTrue(segment.matches_data(self.visitor_data))

        # False
        segment.rules = [false_rule_1]
        self.assertFalse(segment.matches_data(self.visitor_data))

        # True OR False = True
        segment.rules = [true_rule_1, false_rule_1]
        self.assertTrue(segment.matches_data(self.visitor_data))

        # False OR True = True
        segment.rules = [false_rule_1, true_rule_1]
        self.assertTrue(segment.matches_data(self.visitor_data))

        # True OR True = True
        segment.rules = [true_rule_1, true_rule_1]
        self.assertTrue(segment.matches_data(self.visitor_data))

        # False OR False = False
        segment.rules = [false_rule_1, false_rule_1]
        self.assertFalse(segment.matches_data(self.visitor_data))

        # True AND True = True
        segment.rules = [true_rule_1, true_rule_2]
        self.assertTrue(segment.matches_data(self.visitor_data))

        # True AND False = False
        segment.rules = [true_rule_1, false_rule_2]
        self.assertFalse(segment.matches_data(self.visitor_data))

        # False AND True = False
        segment.rules = [false_rule_2, true_rule_1]
        self.assertFalse(segment.matches_data(self.visitor_data))

        # False AND False = False
        segment.rules = [false_rule_1, false_rule_2]
        self.assertFalse(segment.matches_data(self.visitor_data))

        # True AND (True OR False) = True
        segment.rules = [true_rule_1, true_rule_2, false_rule_2]
        self.assertTrue(segment.matches_data(self.visitor_data))

        # False AND (True OR False) = False
        segment.rules = [false_rule_1, true_rule_2, false_rule_2]
        self.assertFalse(segment.matches_data(self.visitor_data))

    def test_rules_in_groups(self):
        segment = Segment(name="Bar")
        rule_1  = Rule(group_id=1, field='foo', comparator="MATCH", value='bar')
        rule_2  = Rule(group_id=2, field='foo', comparator="MATCH", value='bar')
        rule_3  = Rule(group_id=2, field='foo', comparator="MATCH", value='bar')
        rule_4  = Rule(group_id=3, field='foo', comparator="MATCH", value='bar')
        rule_5  = Rule(group_id=3, field='foo', comparator="MATCH", value='bar')
        rule_6  = Rule(group_id=3, field='foo', comparator="MATCH", value='bar')
        segment.rules = [rule_1, rule_2, rule_3, rule_4, rule_5, rule_6]
        
        groups = segment.rules_in_groups()
        self.assertEqual(len(groups), 3)
        self.assertEqual(groups[1], [rule_1])
        self.assertEqual(groups[2], [rule_2, rule_3])
        self.assertEqual(groups[3], [rule_4, rule_5, rule_6])