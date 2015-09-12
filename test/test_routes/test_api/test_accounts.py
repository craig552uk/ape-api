# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Test API accounts

import unittest
import simplejson as json
from app import app, db
from app.models import Account
from . import assert_success_response, assert_error_response
from werkzeug.exceptions import NotFound, BadRequest


class TestAPIAccountRoutes(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.headers = [('Content-Type', 'application/json')]

    def test_api_accounts_list(self):
        r = self.app.get('/api/1/accounts/')
        d = assert_success_response(self, r)

        all_accounts = Account.query.all()
        self.assertIsInstance(d['data'], list)
        self.assertEqual(len(d['data']), len(all_accounts))

    def test_api_accounts_add(self):

        # Bad Requests
        r = self.app.post('/api/1/accounts/', headers=self.headers)
        assert_error_response(self, r, BadRequest())
        
        r = self.app.post('/api/1/accounts/', headers=self.headers, data='{}')
        assert_error_response(self, r, BadRequest())

        r = self.app.post('/api/1/accounts/', headers=self.headers, data='{"name":""}')
        assert_error_response(self, r, BadRequest())

        # Good request
        data = dict(name="FooBar", sites=['a', 'b'], enabled=True)
        r = self.app.post('/api/1/accounts/', headers=self.headers, data=json.dumps(data))

        b = assert_success_response(self, r).get('data')
        self.assertEqual(b['type'], "account")
        self.assertEqual(b['name'], data['name'])
        self.assertEqual(b['sites'], data['sites'])
        self.assertEqual(b['enabled'], data['enabled'])
        self.assertIsNotNone(b['id'])
        self.assertIsNotNone(b['uuid'])
        self.assertIsNotNone(b['created_at'])
        self.assertIsNotNone(b['updated_at'])

        c = Account.query.filter_by(id=b['id']).first()
        self.assertEqual(c.name, data['name'])
        self.assertEqual(c.sites, data['sites'])
        self.assertEqual(c.enabled, data['enabled'])

    def test_api_accounts_show(self):
        # Create account
        r = self.app.post('/api/1/accounts/', headers=self.headers, data=json.dumps(dict(name="Foo")))
        a = assert_success_response(self, r).get('data')

        # Bad Request
        r = self.app.get('/api/1/accounts/foobar/')
        assert_error_response(self, r, NotFound())
        
        # Good request
        r = self.app.get('/api/1/accounts/%s/' % a['id'])
        d = assert_success_response(self, r)
        
        self.assertEqual(d['data']['type'], "account")
        self.assertEqual(d['data']['uuid'], a['uuid'])

    def test_api_accounts_update(self):
        # Create account
        r = self.app.post('/api/1/accounts/', headers=self.headers, data=json.dumps(dict(name="Foo")))
        a = assert_success_response(self, r).get('data')

        # Bad Request
        r = self.app.post('/api/1/accounts/foobar/')
        assert_error_response(self, r, NotFound())

        r = self.app.post('/api/1/accounts/%s/' % a['id'], headers=self.headers)
        assert_error_response(self, r, BadRequest())

        # Good request
        data = dict(name="Bar", sites=['a'], enabled=False)
        r = self.app.post('/api/1/accounts/%s/' % a['id'], headers=self.headers, data=json.dumps(data))

        b = Account.query.filter_by(id=a['id']).first()
        self.assertEqual(b.name, data['name'])
        self.assertEqual(b.sites, data['sites'])
        self.assertEqual(b.enabled, data['enabled'])

        c = assert_success_response(self, r).get('data')
        self.assertEqual(c['type'], "account")
        self.assertEqual(c['name'], data['name'])
        self.assertEqual(c['sites'], data['sites'])
        self.assertEqual(c['enabled'], data['enabled'])

    def test_api_accounts_delete(self):
        # Create account
        r = self.app.post('/api/1/accounts/', headers=self.headers, data=json.dumps(dict(name="Foo")))
        a = assert_success_response(self, r).get('data')

        # Bad Request
        r = self.app.delete('/api/1/accounts/foobar/')
        assert_error_response(self, r, NotFound())
        
        # Good request
        r = self.app.delete('/api/1/accounts/%s/' % a['id'])
        d = assert_success_response(self, r)
        
        self.assertIn("deleted", d['data'])
        self.assertIsNone(Account.query.filter_by(id=a['id']).first())