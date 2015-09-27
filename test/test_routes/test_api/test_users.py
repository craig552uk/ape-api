# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Test API users

import unittest
import simplejson as json
from app import app
from app.models import User
from . import assert_success_response, assert_error_response
from werkzeug.exceptions import NotFound, BadRequest

class TestAPIUserRoutes(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.headers = [('Content-Type', 'application/json')]

    def test_api_users_list(self):
        r = self.app.get('/api/1/users/')
        d = assert_success_response(self, r)

        all_users = User.query.all()
        self.assertIsInstance(d['data'], list)
        self.assertEqual(len(all_users), len(d['data']))

    def test_api_users_add(self):
        # Bad requests
        r = self.app.post('/api/1/users/', headers=self.headers)
        assert_error_response(self, r, BadRequest())

        r = self.app.post('/api/1/users/', headers=self.headers, data='{}')
        assert_error_response(self, r, BadRequest())

        r = self.app.post('/api/1/users/', headers=self.headers, data='{"name":"Jim Jones"}')
        assert_error_response(self, r, BadRequest())

        r = self.app.post('/api/1/users/', headers=self.headers, data='{"email":"jim@jones.com"}')
        assert_error_response(self, r, BadRequest())

        r = self.app.post('/api/1/users/', headers=self.headers, data='{"password":"passw0rd"}')
        assert_error_response(self, r, BadRequest())

        # Good request
        data = dict(name="Jim Jones", email="jim@example.com", password="passw0rd")
        r = self.app.post('/api/1/users/', headers=self.headers, data=json.dumps(data))
        b = assert_success_response(self, r).get('data')
        self.assertEqual(b['type'], "user")
        self.assertEqual(b['name'], data['name'])
        self.assertEqual(b['email'], data['email'])
        self.assertIsNotNone(b['password'])
        self.assertTrue(b['enabled'])
        self.assertFalse(b['admin'])
        self.assertIsNotNone(b['id'])
        self.assertIsNotNone(b['created_at'])
        self.assertIsNotNone(b['updated_at'])
        self.assertIsNone(b['last_login'])

        c = User.authenticate(data['email'], data['password'])
        self.assertEqual(c.name, data['name'])
        self.assertEqual(c.email, data['email'])

    def test_api_users_show(self):
        data = dict(name="Jim Jones", email="jim@example.com", password="passw0rd")
        r = self.app.post('/api/1/users/', headers=self.headers, data=json.dumps(data))
        u = assert_success_response(self, r).get('data')

        # Bad request
        r = self.app.get('/api/1/users/foobar/')
        assert_error_response(self, r, NotFound())

        # Good request        
        r = self.app.get('/api/1/users/%s/' % u['id'])
        d = assert_success_response(self, r)

        self.assertEqual(d['data']['type'], "user")
        self.assertEqual(d['data']['id'], u['id'])


    def test_api_users_update(self):
        data = dict(name="Jim Jones", email="jim@example.com", password="passw0rd")
        r = self.app.post('/api/1/users/', headers=self.headers, data=json.dumps(data))
        u = assert_success_response(self, r).get('data')

        # Bad requests
        r = self.app.post('/api/1/users/foobar/')
        assert_error_response(self, r, NotFound())

        r = self.app.post('/api/1/users/%s/' % u['id'], headers=self.headers)
        assert_error_response(self, r, BadRequest())

        # Good request
        data = dict(name="Jane", email="jane@foo.com", password="qw3rty", enabled=False, admin=True)
        r = self.app.post('/api/1/users/%s/' % u['id'], headers=self.headers, data=json.dumps(data))

        b = assert_success_response(self, r).get('data')
        self.assertEqual(b['type'], "user")
        self.assertEqual(b['name'], data['name'])
        self.assertEqual(b['email'], data['email'])
        self.assertEqual(b['enabled'], data['enabled'])
        self.assertEqual(b['admin'], data['admin'])

        c = User.query.filter_by(id=u['id']).first()
        self.assertEqual(c.name, data['name'])
        self.assertEqual(c.email, data['email'])
        self.assertEqual(c.enabled, data['enabled'])
        self.assertEqual(c.admin, data['admin'])


    def test_api_users_delete(self):
        data = dict(name="Jim Jones", email="jim@example.com", password="passw0rd")
        r = self.app.post('/api/1/users/', headers=self.headers, data=json.dumps(data))
        u = assert_success_response(self, r).get('data')

        # Bad request
        r = self.app.delete('/api/1/users/foobar/')
        assert_error_response(self, r, NotFound())

        # Good request
        r = self.app.delete('/api/1/users/%s/' % u['id'])
        d = assert_success_response(self, r)

        self.assertIn("deleted", d['data'])
        self.assertIsNone(User.query.filter_by(id=u['id']).first())

