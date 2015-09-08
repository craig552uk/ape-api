# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Unit Tests for app

import unittest
import simplejson as json
from app import app, db
from app.models import Account, Segment, Rule, Placeholder, Component
from urllib import urlencode

# Mapping of friendly and short param names
params = {
    'visitor_id':     'cc', # The APE cookie visitor_id
    'debug':          'db', # Debug switch
    'page_url':       'dl', # Page URL
    'referrer_url':   'dr', # Referrer URL if set
    'page_title':     'dt', # Page title
    'event':          'ev', # Event
    'account_id':     'id', # The customer account ID
    'timestamp':      'ld', # Event timestamp
    'language':       'lg', # Browser language
    'placeholders':   'pc', # The set of Placeholder ids on this page
    'prefix':         'px', # Placeholder class prefix
    'screen_color':   'sc', # Screen colour depth
    'screen_height':  'sh', # Screen height
    'screen_width':   'sw', # Screen width
    'script_version': 'vr', # Version number of this script
}

class TestBeaconIntegration(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def parse_jsonp(self, jsonp):
        """Unpack jsonp response"""
        data = jsonp.lstrip('_ape.callback(').rstrip(')')
        data = json.loads(data)
        self.assertIsInstance(data, dict)
        return data

    def get_beacon(self, **kwargs):
        """ helpful wrapper for querying beacon"""
        # Map frindly params to short names
        args = {params[key]: val for key,val in kwargs.items()}
        r = self.app.get('/beacon.js?' + urlencode(args))
        return self.parse_jsonp(r.data)

    def test_beacon_bad_request_response(self):

        def assert_bad_request_error(r):
            self.assertIn('status', r.keys())
            self.assertIn('error', r.keys())
            self.assertIn('title', r['error'].keys())
            self.assertIn('status', r['error'].keys())
            self.assertIn('detail', r['error'].keys())
            self.assertEqual("Bad Request", r['error']['title'])
            self.assertEqual("400", r['error']['status'])
            self.assertEqual(400, r['status'])

        # Empty request
        assert_bad_request_error(self.get_beacon())

        # Bad Account id
        assert_bad_request_error(self.get_beacon(account_id="foobar"))

        # Bad page url
        assert_bad_request_error(self.get_beacon(page_url="foobar"))

    def test_beacon_valid_request_response(self):
        # Invalid account id returns empty response
        r = self.get_beacon(account_id="foo", page_url="http://foo.com/bar")
        self.assertIsInstance(r, dict)
        self.assertEqual(r.keys(), ['status'])

        # Create inactive account
        account = Account(name="Foo Bar", sites=["foo.com"], enabled=False)
        db.session.add(account)
        db.session.commit()

        # Inactive account returns empty response
        r = self.get_beacon(account_id=account.uuid, page_url="http://foo.com/bar")
        self.assertIsInstance(r, dict)
        self.assertEqual(r.keys(), ['status'])

        # Activate account
        account.enabled = True
        db.session.add(account)
        db.session.commit()

        # Active account with bad url returns empty response
        r = self.get_beacon(account_id=account.uuid, page_url="http://bad.com/bar")
        self.assertIsInstance(r, dict)
        self.assertEqual(r.keys(), ['status'])

        # Active account with good url returns new visitor id
        r = self.get_beacon(account_id=account.uuid, page_url="http://foo.com/bar")
        self.assertIn('visitor_id', r)
        visitor_id = r['visitor_id']

        # Return submitted visitor id if provided
        r = self.get_beacon(account_id=account.uuid, page_url="http://foo.com/bar", visitor_id=visitor_id)
        self.assertEqual(visitor_id, r['visitor_id'])

        # Configure placeholders, components and segments for account
        rule = Rule(field="page_url", comparator="START_WITH", value="http://foo.com/yes")
        db.session.add(rule)

        segment = Segment(name="My Segment", rules=[rule])
        db.session.add(segment)

        component = Component(name="My Component", segment=segment, markup="<h1>My Component</h1>")
        db.session.add(component)

        placeholder = Placeholder(name="My Placeholder", components=[component])
        db.session.add(placeholder)
        
        db.session.add(account)
        account.placeholders = [placeholder]
        account.segments = [segment]
        db.session.commit()

        # Refresh objects in db session after commit
        db.session.refresh(account)
        db.session.refresh(rule)
        db.session.refresh(segment)
        db.session.refresh(component)
        db.session.refresh(placeholder)

        # Unknown placeholder ids returns empty set of components 
        r = self.get_beacon(account_id=account.uuid, page_url="http://foo.com", 
                            visitor_id=visitor_id, placeholders="ape-foo")
        self.assertIn('components', r)
        self.assertEqual(dict(), r['components'])

        # Known placeholder ids with no matching components returns empty set of components
        placeholder_str = "ape-" + placeholder.uuid
        r = self.get_beacon(account_id=account.uuid, page_url="http://foo.com/nope", 
                            visitor_id=visitor_id, placeholders=placeholder_str)
        self.assertIn('components', r)
        self.assertEqual(dict(), r['components'])

        # Known placeholder ids with matching components returns set of components
        placeholder_str = "ape-" + placeholder.uuid
        r = self.get_beacon(account_id=account.uuid, page_url="http://foo.com/yes", 
                            visitor_id=visitor_id, placeholders=placeholder_str)
        self.assertIn('components', r)
        self.assertIn(placeholder_str, r['components'])
        self.assertIn('content', r['components'][placeholder_str])
        self.assertEqual(component.markup, r['components'][placeholder_str]['content'])