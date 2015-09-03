# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Test API root

import unittest
from app import app
from . import test_json_response_format


class TestAPIRootRoutes(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_api_root(self):
        r = self.app.get('/api/')
        test_json_response_format(self, r)
        self.assertEqual(401, r.status_code)

    def test_api_root_1(self):
        r = self.app.get('/api/1/')
        test_json_response_format(self, r)
        self.assertEqual(401, r.status_code)