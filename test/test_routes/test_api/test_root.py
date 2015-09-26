# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Test API root

import unittest
from app import app
from . import assert_success_response, assert_error_response
from werkzeug.exceptions import NotFound

class TestAPIRootRoutes(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_api_root(self):
        r = self.app.get('/api/')
        self.assertEqual(401, r.status_code)

    def test_api_root_1(self):
        r = self.app.get('/api/1/')
        self.assertEqual(401, r.status_code)

    def test_jsonp(self):
        r = self.app.get("/api/?callback=foo")
        self.assertTrue(r.data.startswith("foo("))
        self.assertTrue(r.data.endswith(");"))
        self.assertEqual(200, r.status_code)
        self.assertEqual(r.mimetype, "application/javascript")