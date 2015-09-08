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
        account = Account.query.filter_by(id=account.id).first()
        self.assertEqual(account.name, 'Foo')
        self.assertEqual(account.sites, ['foo', 'bar'])
        self.assertTrue(account.enabled)
        
        # Update
        old_created_at = account.created_at
        old_updated_at = account.updated_at
        account.name = 'Bar'
        account.sites = ['spam', 'eggs']
        account.enabled = False
        account = Account.query.filter_by(id=account.id).first()
        self.assertIsInstance(account, Account)
        self.assertEqual(account.name, 'Bar')
        self.assertEqual(account.sites, ['spam', 'eggs'])
        self.assertFalse(account.enabled)
        self.assertEqual(account.created_at, old_created_at)
        self.assertNotEqual(account.updated_at, old_updated_at)

        # Delete
        db.session.delete(account)
        count = Account.query.filter_by(id=account.id).count()
        self.assertEqual(0, count)

    def test_account_url_in_sites(self):
        account = Account(name='Foo', sites=['example.com', 'foo-bar.org'])
        self.assertTrue(account.url_in_sites("http://example.com"))
        self.assertTrue(account.url_in_sites("https://example.com"))
        self.assertTrue(account.url_in_sites("http://example.com/foo/bar"))
        self.assertTrue(account.url_in_sites("https://example.com/foo/bar"))
        self.assertFalse(account.url_in_sites("http://dummy.com"))
        self.assertFalse(account.url_in_sites("https://dummy.com"))
        self.assertFalse(account.url_in_sites("http://dummy.com/foo/bar"))
        self.assertFalse(account.url_in_sites("https://dummy.com/foo/bar"))

    def test_account_to_dict(self): # TODO
        account = Account(name='Foo', sites=['example.com', 'foo-bar.org'])
        db.session.add(account)
        db.session.commit()
        d = account.to_dict()
        self.assertEqual(d.get('type'), "account")
        self.assertEqual(d.get('id'), account.id)
        self.assertEqual(d.get('name'), account.name)
        self.assertEqual(d.get('uuid'), account.uuid)
        self.assertEqual(d.get('sites'), account.sites)
        self.assertEqual(d.get('enabled'), account.enabled)
        self.assertEqual(d.get('created_at'), account.created_at)
        self.assertEqual(d.get('updated_at'), account.updated_at)