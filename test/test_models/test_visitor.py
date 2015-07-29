# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Unit Tests for Visitor Model

import unittest
import datetime as DT
from time import time as epoch
from app import db
from app.models import Visitor, Account

class TestModelVisitor(unittest.TestCase):

    def test_visitor_crud(self):
        # Create
        visitor = Visitor()
        db.session.add(visitor)
        db.session.commit()
        self.assertIn(visitor, Visitor.query.all())
        self.assertIsInstance(visitor.uuid, unicode)
        self.assertIsInstance(visitor.created_at, DT.datetime)

        # Read
        uuid = visitor.uuid
        visitor = Visitor.query.filter_by(uuid=uuid).first()
        self.assertEqual(uuid, visitor.uuid)
        
        # Update
        visitor.uuid = 'FooBar'
        visitor = Visitor.query.filter_by(uuid='FooBar').first()
        self.assertIsInstance(visitor, Visitor)
        self.assertEqual('FooBar', visitor.uuid)

        # Delete
        db.session.delete(visitor)
        count = Visitor.query.filter_by(uuid='FooBar').count()
        self.assertEqual(0, count)

    def test_visitor_get_or_create(self):
        account_1 = Account(name="Foo 1")
        account_2 = Account(name="Foo 2")
        visitor = Visitor()
        account_2.visitors.append(visitor)
        db.session.add(account_1)
        db.session.add(account_2)
        db.session.commit()

        # Return new Visitor if visitor uuid empty
        visitor_a = Visitor.get_or_create(account_1, "")
        self.assertIsInstance(visitor_a, Visitor)
        self.assertEqual(visitor_a.account, account_1)
        self.assertIn(visitor_a, account_1.visitors)

        # Return new Visitor with specified uuid if unknown
        visitor_b = Visitor.get_or_create(account_1, "new-visitor-uuid")
        self.assertIsInstance(visitor_b, Visitor)
        self.assertEqual(visitor_b.account, account_1)
        self.assertEqual(visitor_b.uuid, "new-visitor-uuid")
        self.assertIn(visitor_b, account_1.visitors)
        
        # Return new Visitor if known but unknown to Account
        visitor_c = Visitor.get_or_create(account_1, visitor.uuid)
        self.assertIsInstance(visitor_c, Visitor)
        self.assertEqual(visitor_c.account, account_1)
        self.assertEqual(visitor_c.uuid, visitor.uuid)
        self.assertIn(visitor_c, account_1.visitors)

        # Return Visitor if known to Account
        visitor_d = Visitor.get_or_create(account_2, visitor.uuid)
        self.assertIsInstance(visitor_d, Visitor)
        self.assertEqual(visitor_d.account, account_2)
        self.assertEqual(visitor_d, visitor)
        self.assertIn(visitor_d, account_2.visitors)

    def test_visitor_guid(self):
        account = Account(name="Foo 3")
        visitor = Visitor()
        account.visitors.append(visitor)
        db.session.add(account)
        db.session.commit()

        required_guid = "%s-%s" % (account.uuid, visitor.uuid)
        self.assertEqual(visitor.guid(), required_guid)

    def test_store_payload(self):
        account = Account(name="Foo 4")
        visitor = Visitor()
        account.visitors.append(visitor)
        db.session.add(account)
        db.session.commit()

        args = dict()
        args['user_agent']      = "Foo Bar"                    # Full UserAgent string
        args['platform_name']   = "linux"                      # Platform name from UA
        args['browser_name']    = "chrome"                     # Browser name from UA
        args['browser_version'] = "1.2.3"                      # Browser version from UA
        args['request_address'] = "0.0.0.0"                    # Request IP address
        args['visitor_id']      = "12345"                      # The APE cookie visitor_id
        args['debug']           = False                        # Debug switch
        args['page_url']        = "http://example.com/foo/bar" # Page URL
        args['referrer_url']    = "http://example.com/foo/baz" # Referrer URL if set
        args['page_title']      = "Foo Bar Baz"                # Page title
        args['event']           = ""                           # Event
        args['account_id']      = "67890"                      # The customer account ID
        args['timestamp']       = epoch()                      # Epoch timestamp
        args['language']        = "en-GB"                      # Browser language
        args['placeholders']    = []                           # The set of Placeholder ids on this page
        args['prefix']          = "ape"                        # Placeholder class prefix
        args['screen_colour']   = 256                          # Screen colour depth
        args['screen_height']   = 1000                         # Screen height
        args['screen_width']    = 1000                         # Screen width
        args['script_version']  = "0.0.0"                      # Version number of this script

        visitor_data = visitor.store_payload(args)
        self.assertIsInstance(visitor_data, dict)