# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Unit Tests for Rule Model

import unittest
import datetime as DT
from app import db
from app.models import Rule

class TestModelRule(unittest.TestCase):

    def test_rule_crud(self):
        # Create
        rule = Rule(group_id=3, field="foo", comparator="EQUAL", value="foo bar")
        db.session.add(rule)
        db.session.commit()
        self.assertIn(rule, Rule.query.all())
        self.assertIsInstance(rule.group_id, int)
        self.assertIsInstance(rule.field, unicode)
        self.assertIsInstance(rule.comparator, unicode)
        self.assertIsInstance(rule.value, unicode)
        self.assertIsInstance(rule.created_at, DT.datetime)
        self.assertIsInstance(rule.updated_at, DT.datetime)

        # Read
        rule = Rule.query.filter_by(id=rule.id).first()
        self.assertEqual(rule.group_id, 3)
        self.assertEqual(rule.field, "foo")
        self.assertEqual(rule.comparator, "EQUAL")
        self.assertEqual(rule.value, "foo bar")
        
        # Update
        old_created_at  = rule.created_at
        old_updated_at  = rule.updated_at
        rule.group_id   = 5
        rule.field      = "bar"
        rule.comparator = "NOT_EQUAL"
        rule.value      = "bar foo"
        rule = Rule.query.filter_by(id=rule.id).first()
        self.assertIsInstance(rule, Rule)
        self.assertEqual(rule.group_id, 5)
        self.assertEqual(rule.field, "bar")
        self.assertEqual(rule.comparator, "NOT_EQUAL")
        self.assertEqual(rule.value, "bar foo")
        self.assertEqual(rule.created_at, old_created_at)
        self.assertNotEqual(rule.updated_at, old_updated_at)

        # Delete
        db.session.delete(rule)
        count = Rule.query.filter_by(id=rule.id).count()
        self.assertEqual(0, count)