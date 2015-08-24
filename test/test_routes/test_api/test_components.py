# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Test API components

import unittest
from app import app


class TestAPIComponentRoutes(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_api_components_list(self):
        r = self.app.get('/api/1/placeholders/foobar/components/')
        self.assertEqual(200, r.status_code)

    def test_api_components_add(self):
        r = self.app.post('/api/1/placeholders/foobar/components/')
        self.assertEqual(200, r.status_code)

    def test_api_components_show(self):
        r = self.app.get('/api/1/placeholders/foobar/components/foobaz/')
        self.assertEqual(200, r.status_code)

    def test_api_components_update(self):
        r = self.app.post('/api/1/placeholders/foobar/components/foobaz/')
        self.assertEqual(200, r.status_code)

    def test_api_components_delete(self):
        r = self.app.delete('/api/1/placeholders/foobar/components/foobaz/')
        self.assertEqual(200, r.status_code)