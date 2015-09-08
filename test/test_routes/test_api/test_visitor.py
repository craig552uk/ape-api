# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Test API visitors

import unittest
from app import app
from . import assert_success_response, assert_error_response
from werkzeug.exceptions import NotFound

class TestAPIVisitorRoutes(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_api_visitors_list(self):
        r = self.app.get('/api/1/visitors/')
        self.assertEqual(200, r.status_code)

    def test_api_visitors_add(self):
        r = self.app.post('/api/1/visitors/')
        self.assertEqual(200, r.status_code)

    def test_api_visitors_show(self):
        r = self.app.get('/api/1/visitors/foobar/')
        self.assertEqual(200, r.status_code)

    def test_api_visitors_update(self):
        r = self.app.post('/api/1/visitors/foobar/')
        self.assertEqual(200, r.status_code)

    def test_api_visitors_delete(self):
        r = self.app.delete('/api/1/visitors/foobar/')
        self.assertEqual(200, r.status_code)