# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Customer Model

from app import db

class Customer(db.Model):
    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __repr__(self):
        return 'Customer[%r] %r' % (self.id, self.name)