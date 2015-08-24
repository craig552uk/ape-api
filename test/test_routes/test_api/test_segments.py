# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Test API segments

import unittest
from app import app
from . import test_json_response_format


class TestAPISegmentRoutes(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_api_segments_list(self):
        r = self.app.get('/api/1/segments/')
        test_json_response_format(self, r)
        self.assertEqual(200, r.status_code)

    def test_api_segments_add(self):
        r = self.app.post('/api/1/segments/')
        test_json_response_format(self, r)
        self.assertEqual(200, r.status_code)

    def test_api_segments_show(self):
        r = self.app.get('/api/1/segments/foobar/')
        test_json_response_format(self, r)
        self.assertEqual(200, r.status_code)

    def test_api_segments_update(self):
        r = self.app.post('/api/1/segments/foobar/')
        test_json_response_format(self, r)
        self.assertEqual(200, r.status_code)

    def test_api_segments_delete(self):
        r = self.app.delete('/api/1/segments/foobar/')
        test_json_response_format(self, r)
        self.assertEqual(200, r.status_code)