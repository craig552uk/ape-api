# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Unit Tests for Customer Model

import unittest
from app import db
from app.models import Customer

class TestModelCustomer(unittest.TestCase):

    def test_crud(self):
        # Create
        customer = Customer(name='Foo')
        db.session.add(customer)
        db.session.commit()
        self.assertIn(customer, Customer.query.all())

        # Read
        customer = Customer.query.filter_by(name='Foo').first()
        self.assertEqual(customer.name, 'Foo')
        
        # Update
        customer.name = 'Bar'
        customer = Customer.query.filter_by(name='Bar').first()
        self.assertIsInstance(customer, Customer)
        self.assertEqual('Bar', customer.name)

        # Delete
        db.session.delete(customer)
        count = Customer.query.filter_by(name='Bar').count()
        self.assertEqual(0, count)