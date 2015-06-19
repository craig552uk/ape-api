# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Unit Tests for app

import unittest
from app import app


class TestRoutes(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_home(self):
        r = self.app.get('/')
        self.assertEqual(200, r.status_code)
        self.assertIn("Hello World!", r.data)

    def test_static(self):
        r = self.app.get('/favicon.ico')
        self.assertEqual(200, r.status_code)