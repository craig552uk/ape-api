# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Unit Tests for Account Model

import unittest
import datetime as DT
from app import db
from app.models import Account

class TestModelAccount(unittest.TestCase):

    def test_account_crud(self):
        # Create
        account = Account(name='Foo', sites=['foo', 'bar'])
        db.session.add(account)
        db.session.commit()
        self.assertIn(account, Account.query.all())
        self.assertIsInstance(account.uuid, unicode)
        self.assertIsInstance(account.sites, list)
        self.assertIsInstance(account.enabled, bool)
        self.assertIsInstance(account.created_at, DT.datetime)
        self.assertIsInstance(account.updated_at, DT.datetime)

        # Read
        account = Account.query.filter_by(name='Foo').first()
        self.assertEqual(account.name, 'Foo')
        self.assertEqual(account.sites, ['foo', 'bar'])
        self.assertTrue(account.enabled)
        
        # Update
        old_created_at = account.created_at
        old_updated_at = account.updated_at
        account.name = 'Bar'
        account.sites = ['spam', 'eggs']
        account.enabled = False
        account = Account.query.filter_by(name='Bar').first()
        self.assertIsInstance(account, Account)
        self.assertEqual(account.name, 'Bar')
        self.assertEqual(account.sites, ['spam', 'eggs'])
        self.assertFalse(account.enabled)
        self.assertEqual(account.created_at, old_created_at)
        self.assertNotEqual(account.updated_at, old_updated_at)

        # Delete
        db.session.delete(account)
        count = Account.query.filter_by(name='Bar').count()
        self.assertEqual(0, count)