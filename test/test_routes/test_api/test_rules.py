# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Test API rules

import unittest
from app import app


class TestAPIRulesRoutes(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_api_rules_list(self):
        r = self.app.get('/api/1/segments/foobar/rules/')
        self.assertEqual(200, r.status_code)

    def test_api_rules_add(self):
        r = self.app.post('/api/1/segments/foobar/rules/')
        self.assertEqual(200, r.status_code)

    def test_api_rules_show(self):
        r = self.app.get('/api/1/segments/foobar/rules/foobaz/')
        self.assertEqual(200, r.status_code)

    def test_api_rules_update(self):
        r = self.app.post('/api/1/segments/foobar/rules/foobaz/')
        self.assertEqual(200, r.status_code)

    def test_api_rules_delete(self):
        r = self.app.delete('/api/1/segments/foobar/rules/foobaz/')
        self.assertEqual(200, r.status_code)