# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Test API placeholders

import unittest
from app import app


class TestAPIVisitorRoutes(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_api_placeholders_list(self):
        r = self.app.get('/api/1/placeholders/')
        self.assertEqual(200, r.status_code)

    def test_api_placeholders_add(self):
        r = self.app.post('/api/1/placeholders/')
        self.assertEqual(200, r.status_code)

    def test_api_placeholders_show(self):
        r = self.app.get('/api/1/placeholders/foobar/')
        self.assertEqual(200, r.status_code)

    def test_api_placeholders_update(self):
        r = self.app.post('/api/1/placeholders/foobar/')
        self.assertEqual(200, r.status_code)

    def test_api_placeholders_delete(self):
        r = self.app.delete('/api/1/placeholders/foobar/')
        self.assertEqual(200, r.status_code)