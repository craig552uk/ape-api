# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Unit Tests for Visitor Model

import unittest
import datetime as DT
from app import db
from app.models import Visitor

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