# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Unit Tests for Rule Model

import unittest
from app import db
from app.models import Rule

class TestModelRule(unittest.TestCase):

    def test_rule_crud(self):
        # Create
        rule = Rule(name='Foo')
        db.session.add(rule)
        db.session.commit()
        self.assertIn(rule, Rule.query.all())

        # Read
        rule = Rule.query.filter_by(name='Foo').first()
        self.assertEqual(rule.name, 'Foo')
        
        # Update
        rule.name = 'Bar'
        rule = Rule.query.filter_by(name='Bar').first()
        self.assertIsInstance(rule, Rule)
        self.assertEqual('Bar', rule.name)

        # Delete
        db.session.delete(rule)
        count = Rule.query.filter_by(name='Bar').count()
        self.assertEqual(0, count)