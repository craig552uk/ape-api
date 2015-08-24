# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Test API root

import unittest
from app import app


class TestAPIAccountRoutes(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_api_accounts_(self):
        r = self.app.get('/api/1/accounts/')
        self.assertEqual(200, r.status_code)

    def test_api_accounts_(self):
        r = self.app.post('/api/1/accounts/')
        self.assertEqual(200, r.status_code)

    def test_api_accounts_(self):
        r = self.app.get('/api/1/accounts/foobar/')
        self.assertEqual(200, r.status_code)

    def test_api_accounts_(self):
        r = self.app.post('/api/1/accounts/foobar/')
        self.assertEqual(200, r.status_code)

    def test_api_accounts_(self):
        r = self.app.delete('/api/1/accounts/foobar/')
        self.assertEqual(200, r.status_code)