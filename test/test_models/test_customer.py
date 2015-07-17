# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Unit Tests for Customer Model

import unittest
import datetime as DT
from app import db
from app.models import Customer

class TestModelCustomer(unittest.TestCase):

    def test_crud(self):
        # Create
        customer = Customer(name='Foo', sites=['foo', 'bar'])
        db.session.add(customer)
        db.session.commit()
        self.assertIn(customer, Customer.query.all())
        self.assertIsInstance(customer.uuid, unicode)
        self.assertIsInstance(customer.sites, list)
        self.assertIsInstance(customer.enabled, bool)
        self.assertIsInstance(customer.created_at, DT.datetime)
        self.assertIsInstance(customer.updated_at, DT.datetime)

        # Read
        customer = Customer.query.filter_by(name='Foo').first()
        self.assertEqual(customer.name, 'Foo')
        self.assertEqual(customer.sites, ['foo', 'bar'])
        self.assertTrue(customer.enabled)
        
        # Update
        old_created_at = customer.created_at
        old_updated_at = customer.updated_at
        customer.name = 'Bar'
        customer.sites = ['spam', 'eggs']
        customer.enabled = False
        customer = Customer.query.filter_by(name='Bar').first()
        self.assertIsInstance(customer, Customer)
        self.assertEqual(customer.name, 'Bar')
        self.assertEqual(customer.sites, ['spam', 'eggs'])
        self.assertFalse(customer.enabled)
        self.assertEqual(customer.created_at, old_created_at)
        self.assertNotEqual(customer.updated_at, old_updated_at)

        # Delete
        db.session.delete(customer)
        count = Customer.query.filter_by(name='Bar').count()
        self.assertEqual(0, count)