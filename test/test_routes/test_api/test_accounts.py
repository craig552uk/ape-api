# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Test API accounts

import unittest
from app import app, db
from app.models import Account
from . import assert_success_response, assert_error_response
from werkzeug.exceptions import NotFound


class TestAPIAccountRoutes(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        account = Account(name='Foo', sites=['example.com', 'foo-bar.org'])
        db.session.add(account)
        db.session.commit()
        db.session.refresh(account)
        self.account = account

    def test_api_accounts_list(self):
        r = self.app.get('/api/1/accounts/')
        d = assert_success_response(self, r)

        all_accounts = Account.query.all()
        self.assertIsInstance(d['data'], list)
        self.assertEqual(len(d['data']), len(all_accounts))

    def test_api_accounts_add(self):
        r = self.app.post('/api/1/accounts/')
        d = assert_success_response(self, r)
        # TODO

    def test_api_accounts_show(self):
        # Bad Request
        r = self.app.get('/api/1/accounts/foobar/')
        assert_error_response(self, r, NotFound())
        
        # Good request
        r = self.app.get('/api/1/accounts/%s/' % self.account.id)
        d = assert_success_response(self, r)
        
        self.assertIsInstance(d['data'], dict)
        self.assertEqual(d['data']['type'], "account")
        self.assertEqual(d['data']['uuid'], self.account.uuid)

    def test_api_accounts_update(self):
        # Bad Request
        r = self.app.post('/api/1/accounts/foobar/')
        assert_error_response(self, r, NotFound())
        
        # Good request
        r = self.app.post('/api/1/accounts/%s/' % self.account.id)
        d = assert_success_response(self, r)
        # TODO

    def test_api_accounts_delete(self):
        # Bad Request
        r = self.app.delete('/api/1/accounts/foobar/')
        assert_error_response(self, r, NotFound())
        
        # Good request
        r = self.app.delete('/api/1/accounts/%s/' % self.account.id)
        d = assert_success_response(self, r)
        # TODO