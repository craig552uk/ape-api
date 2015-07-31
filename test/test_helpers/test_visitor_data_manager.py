# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Unit Tests for Visitor Model

import unittest
from time import time as epoch
from app.helpers import visitor_data_manager as VDM

class TestVisitorDataManager(unittest.TestCase):

    def setUp(self):
        self.payload = dict()
        self.payload['user_agent']      = "Foo Bar"                    # Full UserAgent string
        self.payload['platform_name']   = "linux"                      # Platform name from UA
        self.payload['browser_name']    = "chrome"                     # Browser name from UA
        self.payload['browser_version'] = "1.2.3"                      # Browser version from UA
        self.payload['request_address'] = "0.0.0.0"                    # Request IP address
        self.payload['visitor_id']      = "12345"                      # The APE cookie visitor_id
        self.payload['debug']           = False                        # Debug switch
        self.payload['page_url']        = "http://example.com/foo/bar" # Page URL
        self.payload['referrer_url']    = "http://example.com/foo/baz" # Referrer URL if set
        self.payload['page_title']      = "Foo Bar Baz"                # Page title
        self.payload['event']           = ""                           # Event
        self.payload['account_id']      = "67890"                      # The customer account ID
        self.payload['timestamp']       = epoch()                      # Epoch timestamp
        self.payload['language']        = "en-GB"                      # Browser language
        self.payload['placeholders']    = []                           # The set of Placeholder ids on this page
        self.payload['prefix']          = "ape"                        # Placeholder class prefix
        self.payload['screen_color' ]   = 256                          # Screen colour depth
        self.payload['screen_height']   = 1000                         # Screen height
        self.payload['screen_width']    = 1000                         # Screen width
        self.payload['script_version']  = "0.0.0"                      # Version number of this script

    def test_append_payload(self):
        payload_1 = self.payload.copy()
        payload_2 = self.payload.copy()
        payload_3 = self.payload.copy()
        timestamp = epoch()
        payload_1.update(request_address="Foo", user_agent="Foo", timestamp=timestamp)
        payload_2.update(request_address="Foo", user_agent="Foo", timestamp=timestamp+1)
        payload_3.update(request_address="Foo", user_agent="Foo", timestamp=timestamp+31*60)

        # Data with first session and first pageview
        data_1 = VDM.append_payload(payload_1, dict())
        self.assertIsInstance(data_1['visitor_id'], str)
        self.assertIsInstance(data_1['account_id'], str)
        self.assertIsInstance(data_1['sessions'], list)
        self.assertEqual(data_1['session_count'], 1)
        self.assertEqual(len(data_1['sessions']), 1)
        self.assertEqual(len(data_1['sessions'][0]['pageviews']), 1)

        # Add new pageview to existing session
        data_2 = VDM.append_payload(payload_2, data_1).copy()
        self.assertEqual(data_2['visitor_id'], data_1['visitor_id'])
        self.assertEqual(data_2['account_id'], data_1['account_id'])
        self.assertEqual(len(data_2['sessions']), 1)
        self.assertEqual(data_2['session_count'], 1)
        self.assertEqual(len(data_2['sessions'][0]['pageviews']), 2)

        # Add new session with new pageview
        data_3 = VDM.append_payload(payload_3, data_2).copy()
        self.assertEqual(data_3['visitor_id'], data_1['visitor_id'])
        self.assertEqual(data_3['account_id'], data_1['account_id'])
        self.assertEqual(len(data_3['sessions']), 2)
        self.assertEqual(data_3['session_count'], 2)
        self.assertEqual(len(data_3['sessions'][0]['pageviews']), 2)
        self.assertEqual(len(data_3['sessions'][1]['pageviews']), 1)


    def test_new_session(self):
        payload = self.payload.copy()
        session = VDM.new_session(payload)
        self.assertEqual(session['session_start'], payload['timestamp'])
        self.assertEqual(session['session_end'], payload['timestamp'])
        self.assertEqual(session['session_duration'], 0)
        self.assertEqual(session['request_address'], payload['request_address'])
        self.assertEqual(session['user_agent'], payload['user_agent'])
        self.assertEqual(session['screen_color'], payload['screen_color'])
        self.assertEqual(session['screen_width'], payload['screen_width'])
        self.assertEqual(session['screen_height'], payload['screen_height'])
        self.assertIsInstance(session['pageviews'], list)
        self.assertEqual(session['pageview_count'], 1)

    def test_update_session(self):
        payload_1 = self.payload
        payload_2 = payload_1.copy()
        payload_2.update(timestamp=epoch())
        session_1 = VDM.new_session(payload_1)
        session_2 = VDM.update_session(payload_2, session_1)
        
        # Values not updated
        self.assertEqual(session_1['session_start'], session_2['session_start'])
        self.assertEqual(session_1['request_address'], session_2['request_address'])
        self.assertEqual(session_1['user_agent'], session_2['user_agent'])
        self.assertEqual(session_1['screen_color'], session_2['screen_color'])
        self.assertEqual(session_1['screen_width'], session_2['screen_width'])
        self.assertEqual(session_1['screen_height'], session_2['screen_height'])

        # Values updated
        self.assertEqual(session_2['session_end'], payload_2['timestamp'])
        self.assertEqual(session_2['session_duration'], session_2['session_end'] - session_2['session_start'])
        self.assertEqual(len(session_2['pageviews']), len(session_1['pageviews'])+1)
        self.assertEqual(session_2['pageview_count'], len(session_2['pageviews']))

    def test_new_pageview(self):
        payload  = self.payload.copy()
        pageview = VDM.new_pageview(payload)
        self.assertEqual(pageview['page_url'], payload['page_url'])
        self.assertEqual(pageview['referrer_url'], payload['referrer_url'])
        self.assertEqual(pageview['page_title'], payload['page_title'])
        self.assertEqual(pageview['event'], payload['event'])
        self.assertEqual(pageview['timestamp'], payload['timestamp'])
        self.assertEqual(pageview['language'], payload['language'])
        self.assertEqual(pageview['placeholders'], payload['placeholders'])
        self.assertEqual(pageview['prefix'], payload['prefix'])
        self.assertEqual(pageview['script_version'], payload['script_version'])

    def test_payload_is_part_of_session(self):
        payload_1 = self.payload.copy()
        payload_2 = self.payload.copy()
        payload_3 = self.payload.copy()
        payload_4 = self.payload.copy()
        timestamp = epoch()
        payload_1.update(request_address="Foo", user_agent="Foo", timestamp=timestamp)
        payload_2.update(request_address="Foo", user_agent="Bar", timestamp=timestamp)
        payload_3.update(request_address="Bar", user_agent="Foo", timestamp=timestamp)
        payload_4.update(request_address="Foo", user_agent="Foo", timestamp=timestamp+31*60)

        session = VDM.new_session(payload_1)
        self.assertTrue(VDM.payload_is_part_of_session(payload_1, session))
        self.assertFalse(VDM.payload_is_part_of_session(payload_2, session))
        self.assertFalse(VDM.payload_is_part_of_session(payload_3, session))
        self.assertFalse(VDM.payload_is_part_of_session(payload_4, session))