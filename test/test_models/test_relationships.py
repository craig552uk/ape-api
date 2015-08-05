# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Unit Tests for Account Model

import unittest
import datetime as DT
from app import db
from app.models import Account, User, Visitor, Placeholder, Component, Segment, Rule

class TestModelRelationships(unittest.TestCase):

    def test_relationships(self):

        # Create account with no relationships
        account = Account(name="Account Foo")
        db.session.add(account)
        db.session.commit()
        self.assertEqual(account.users, [])

        # Add user to account
        user = User(name="User 1", email="a@b.com", password="passw0rd")
        account.users.append(user)
        db.session.add(user)
        db.session.commit()
        self.assertIn(user, account.users)
        self.assertEqual(user.account, account)

        # Add visitor to account
        visitor = Visitor()
        account.visitors.append(visitor)
        db.session.add(visitor)
        db.session.commit()
        self.assertIn(visitor, account.visitors)
        self.assertEqual(visitor.account, account)

        # Add placeholder to account
        placeholder = Placeholder(name="Placeholder Foo")
        account.placeholders.append(placeholder)
        db.session.add(placeholder)
        db.session.commit()
        self.assertIn(placeholder, account.placeholders)
        self.assertEqual(placeholder.account, account)

        # Add component to placeholder
        component = Component(name="Component Foo")
        placeholder.components.append(component)
        db.session.add(component)
        db.session.commit()
        self.assertIn(component, placeholder.components)
        self.assertEqual(component.placeholder, placeholder)

        # Add segment to account
        segment = Segment(name="Segment Foo")
        account.segments.append(segment)
        db.session.add(segment)
        db.session.commit()
        self.assertIn(segment, account.segments)
        self.assertEqual(segment.account, account)
        self.assertEqual(segment.rules, [])

        # Add rule to segment
        rule = Rule()
        segment.rules.append(rule)
        db.session.add(rule)
        db.session.commit()
        self.assertIn(rule, segment.rules)
        self.assertEqual(rule.segment, segment)

        # Add segment to component
        component.segment = segment
        db.session.commit()
        self.assertEqual(component.segment, segment)
        self.assertIn(component, segment.components)
