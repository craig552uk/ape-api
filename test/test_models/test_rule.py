# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Unit Tests for Rule Model

import unittest
import datetime as DT
from time import time as epoch
from app import db
from app.models import Rule

class TestModelRule(unittest.TestCase):

    def setUp(self):
        # Test data
        pv = dict()
        pv['page_url']         = "http://example.com"
        pv['referrer_url']     = "http://example.com"
        pv['page_title']       = "Foo Bar"
        pv['timestamp']        = epoch()
        pv['language']         = "en-GB"
        pv['event']            = "pageload"
        pv['placeholders']     = ['a', 'b', 'c`']
        pv['prefix']           = "ape"
        pv['script_version']   = "0.0.0"

        sn = dict()
        sn['session_start']    = epoch()
        sn['session_end']      = epoch()
        sn['session_duration'] = 100
        sn['request_address']  = "http://example.com"
        sn['user_agent']       = "FooBar"
        sn['screen_color']     = 256
        sn['screen_width']     = 1000
        sn['screen_height']    = 1000
        sn['pageviews']        = [pv]
        sn['pageview_count']   = 1

        data = dict()
        data['visitor_id']     = ""
        data['account_id']     = ""
        data['sessions']       = {0:sn}
        data['sessions_count'] = 1

        self.pageview = pv
        self.session  = sn
        self.data     = data


    def test_rule_crud(self):
        # Create
        rule = Rule(group_id=3, field="foo", comparator="MATCH", value="foo bar")
        db.session.add(rule)
        db.session.commit()
        self.assertIn(rule, Rule.query.all())
        self.assertIsInstance(rule.group_id, int)
        self.assertIsInstance(rule.field, unicode)
        self.assertIsInstance(rule.comparator, unicode)
        self.assertIsInstance(rule.value, unicode)
        self.assertIsInstance(rule.created_at, DT.datetime)
        self.assertIsInstance(rule.updated_at, DT.datetime)

        # Read
        rule = Rule.query.filter_by(id=rule.id).first()
        self.assertEqual(rule.group_id, 3)
        self.assertEqual(rule.field, "foo")
        self.assertEqual(rule.comparator, "MATCH")
        self.assertEqual(rule.value, "foo bar")
        
        # Update
        old_created_at  = rule.created_at
        old_updated_at  = rule.updated_at
        rule.group_id   = 5
        rule.field      = "bar"
        rule.comparator = "NOT_MATCH"
        rule.value      = "bar foo"
        rule = Rule.query.filter_by(id=rule.id).first()
        self.assertIsInstance(rule, Rule)
        self.assertEqual(rule.group_id, 5)
        self.assertEqual(rule.field, "bar")
        self.assertEqual(rule.comparator, "NOT_MATCH")
        self.assertEqual(rule.value, "bar foo")
        self.assertEqual(rule.created_at, old_created_at)
        self.assertNotEqual(rule.updated_at, old_updated_at)

        # Delete
        db.session.delete(rule)
        count = Rule.query.filter_by(id=rule.id).count()
        self.assertEqual(0, count)


    def test_apply(self):
        rule_1 = Rule(field='sessions_count', comparator="MATCH", value=self.data['sessions_count'])
        rule_2 = Rule(field='foo',            comparator="MATCH", value=self.data['sessions_count'])
        rule_3 = Rule(field='sessions_count', comparator="MATCH", value="Foo")

        self.assertTrue(rule_1.apply(self.data))
        self.assertFalse(rule_2.apply(self.data))
        self.assertFalse(rule_3.apply(self.data))

        rule_1 = Rule(field='session_start', comparator="MATCH", value=self.session['session_start'])
        rule_2 = Rule(field='foo',           comparator="MATCH", value=self.session['session_start'])
        rule_3 = Rule(field='session_start', comparator="MATCH", value="Foo")

        self.assertTrue(rule_1.apply(self.data))
        self.assertFalse(rule_2.apply(self.data))
        self.assertFalse(rule_3.apply(self.data))

        rule_1 = Rule(field='page_url', comparator="MATCH", value=self.pageview['page_url'])
        rule_2 = Rule(field='foo',      comparator="MATCH", value=self.pageview['page_url'])
        rule_3 = Rule(field='page_url', comparator="MATCH", value="Foo")

        self.assertTrue(rule_1.apply(self.data))
        self.assertFalse(rule_2.apply(self.data))
        self.assertFalse(rule_3.apply(self.data))


    def test_apply_to_data(self):
        rule_1 = Rule(field='visitor_id',     comparator="MATCH", value=self.data['visitor_id'])
        rule_2 = Rule(field='account_id',     comparator="MATCH", value=self.data['account_id'])
        rule_3 = Rule(field='sessions',       comparator="MATCH", value=self.data['sessions'])
        rule_4 = Rule(field='sessions_count', comparator="MATCH", value=self.data['sessions_count'])

        self.assertFalse(rule_1.apply_to_data(self.data))
        self.assertFalse(rule_2.apply_to_data(self.data))
        self.assertFalse(rule_3.apply_to_data(self.data))
        self.assertTrue(rule_4.apply_to_data(self.data))


    def test_apply_to_session(self):
        rule_1 = Rule(field='session_start',    comparator="MATCH", value=self.session['session_start'])
        rule_2 = Rule(field='session_end',      comparator="MATCH", value=self.session['session_end'])
        rule_3 = Rule(field='session_duration', comparator="MATCH", value=self.session['session_duration'])
        rule_4 = Rule(field='request_address',  comparator="MATCH", value=self.session['request_address'])
        rule_5 = Rule(field='user_agent',       comparator="MATCH", value=self.session['user_agent'])
        rule_6 = Rule(field='screen_color',     comparator="MATCH", value=self.session['screen_color'])
        rule_7 = Rule(field='screen_width',     comparator="MATCH", value=self.session['screen_width'])
        rule_8 = Rule(field='screen_height',    comparator="MATCH", value=self.session['screen_height'])
        rule_9 = Rule(field='pageview_count',   comparator="MATCH", value=self.session['pageview_count'])
        rule_0 = Rule(field='pageviews',        comparator="MATCH", value=self.session['pageviews'])

        self.assertTrue(rule_1.apply_to_session(self.session))
        self.assertTrue(rule_2.apply_to_session(self.session))
        self.assertTrue(rule_3.apply_to_session(self.session))
        self.assertTrue(rule_4.apply_to_session(self.session))
        self.assertTrue(rule_5.apply_to_session(self.session))
        self.assertTrue(rule_6.apply_to_session(self.session))
        self.assertTrue(rule_7.apply_to_session(self.session))
        self.assertTrue(rule_8.apply_to_session(self.session))
        self.assertTrue(rule_9.apply_to_session(self.session))
        self.assertFalse(rule_0.apply_to_session(self.session))


    def test_apply_to_pageview(self):
        rule_1 = Rule(field='page_url',       comparator="MATCH", value=self.pageview['page_url'])
        rule_2 = Rule(field='referrer_url',   comparator="MATCH", value=self.pageview['referrer_url'])
        rule_3 = Rule(field='page_title',     comparator="MATCH", value=self.pageview['page_title'])
        rule_4 = Rule(field='timestamp',      comparator="MATCH", value=self.pageview['timestamp'])
        rule_5 = Rule(field='language',       comparator="MATCH", value=self.pageview['language'])
        rule_6 = Rule(field='event',          comparator="MATCH", value=self.pageview['event'])
        rule_7 = Rule(field='placeholders',   comparator="MATCH", value=self.pageview['placeholders'])
        rule_8 = Rule(field='prefix',         comparator="MATCH", value=self.pageview['prefix'])
        rule_9 = Rule(field='script_version', comparator="MATCH", value=self.pageview['script_version'])

        self.assertTrue(rule_1.apply_to_pageview(self.pageview))
        self.assertTrue(rule_2.apply_to_pageview(self.pageview))
        self.assertTrue(rule_3.apply_to_pageview(self.pageview))
        self.assertTrue(rule_4.apply_to_pageview(self.pageview))
        self.assertTrue(rule_5.apply_to_pageview(self.pageview))
        self.assertFalse(rule_6.apply_to_pageview(self.pageview))
        self.assertFalse(rule_7.apply_to_pageview(self.pageview))
        self.assertFalse(rule_8.apply_to_pageview(self.pageview))
        self.assertFalse(rule_9.apply_to_pageview(self.pageview))


    def test_compare(self):
        r_match          = Rule(comparator="MATCH",          value="FooBar")
        r_not_match      = Rule(comparator="NOT_MATCH",      value="FooBaz")
        r_contain        = Rule(comparator="CONTAIN",        value="Bar")
        r_not_contain    = Rule(comparator="NOT_CONTAIN",    value="Spam")
        r_start_with     = Rule(comparator="START_WITH",     value="Foo")
        r_not_start_with = Rule(comparator="NOT_START_WITH", value="Bar")
        r_end_with       = Rule(comparator="END_WITH",       value="Bar")
        r_not_end_with   = Rule(comparator="NOT_END_WITH",   value="Foo")
        r_less_than      = Rule(comparator="LESS_THAN",      value="10")
        r_greater_than   = Rule(comparator="GREATER_THAN",   value="10")

        self.assertTrue(r_match.compare("FooBar"))
        self.assertFalse(r_match.compare("BarFoo"))
        self.assertTrue(r_not_match.compare("FooBar"))
        self.assertFalse(r_not_match.compare("FooBaz"))
        self.assertTrue(r_contain.compare("FooBar"))
        self.assertFalse(r_contain.compare("FooBaz"))
        self.assertTrue(r_not_contain.compare("FooBar"))
        self.assertFalse(r_not_contain.compare("Foo Spam"))
        self.assertTrue(r_start_with.compare("FooBar"))
        self.assertFalse(r_start_with.compare("BarFoo"))
        self.assertTrue(r_not_start_with.compare("FooBar"))
        self.assertFalse(r_not_start_with.compare("BarFoo"))
        self.assertTrue(r_end_with.compare("FooBar"))
        self.assertFalse(r_end_with.compare("BarFoo"))
        self.assertTrue(r_not_end_with.compare("FooBar"))
        self.assertFalse(r_not_end_with.compare("BarFoo"))
        self.assertTrue(r_less_than.compare("20"))
        self.assertFalse(r_less_than.compare("5"))
        self.assertTrue(r_greater_than.compare("5"))
        self.assertTrue(r_greater_than.compare("5.0"))
        self.assertTrue(r_greater_than.compare(5.0))
        self.assertFalse(r_greater_than.compare("20"))
        self.assertFalse(r_greater_than.compare("20.0"))
        self.assertFalse(r_greater_than.compare(20.0))