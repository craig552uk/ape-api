# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Unit Tests for Account Model

import unittest
import datetime as DT
from app import db
from app.models import Account, User

class TestModelRelationships(unittest.TestCase):

    def test_relationships(self):

        # Create account with no relationships
        account = Account(name="Account Foo")
        db.session.add(account)
        db.session.commit()
        self.assertEqual(account.users, [])

        # Add user to account
        user = User(name="User 1", email="a@b.com", password="passw0rd")
        account.users.append(user)
        db.session.add(user)
        db.session.commit()
        self.assertIn(user, account.users)
        self.assertEqual(user.account, account)