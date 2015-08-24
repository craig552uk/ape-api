# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Test API users

import unittest
from app import app


class TestAPIUserRoutes(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_api_users_list(self):
        r = self.app.get('/api/1/users/')
        self.assertEqual(200, r.status_code)

    def test_api_users_add(self):
        r = self.app.post('/api/1/users/')
        self.assertEqual(200, r.status_code)

    def test_api_users_show(self):
        r = self.app.get('/api/1/users/foobar/')
        self.assertEqual(200, r.status_code)

    def test_api_users_update(self):
        r = self.app.post('/api/1/users/foobar/')
        self.assertEqual(200, r.status_code)

    def test_api_users_delete(self):
        r = self.app.delete('/api/1/users/foobar/')
        self.assertEqual(200, r.status_code)