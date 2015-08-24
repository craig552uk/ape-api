# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Test API root

import unittest
from app import app


class TestAPIRootRoutes(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_api_root(self):
        r = self.app.get('/api/')
        self.assertEqual(401, r.status_code)

    def test_api_root_1(self):
        r = self.app.get('/api/1/')
        self.assertEqual(401, r.status_code)