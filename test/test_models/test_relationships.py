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

        # Add components to placeholder
        component_0 = Component(name="Component Foo", index=0)
        component_1 = Component(name="Component Foo", index=1)
        component_2 = Component(name="Component Foo", index=2)
        placeholder.components.append(component_2)
        placeholder.components.append(component_1)
        placeholder.components.append(component_0)
        db.session.commit()
        self.assertIn(component_0, placeholder.components)
        self.assertEqual(component_0.placeholder, placeholder)
        self.assertEqual(component_0, placeholder.components[0])
        self.assertEqual(component_1, placeholder.components[1])
        self.assertEqual(component_2, placeholder.components[2])

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
        component_0.segment = segment
        db.session.commit()
        self.assertEqual(component_0.segment, segment)
        self.assertIn(component_0, segment.components)
