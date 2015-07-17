# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Customer Model

import uuid
from app import db
from datetime import datetime as DT

class Customer(db.Model):
    __tablename__ = "customers"

    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(80))
    uuid       = db.Column(db.String(80), default=lambda: str(uuid.uuid4()))
    sites      = db.Column(db.PickleType(), default=[])
    enabled    = db.Column(db.Boolean(), default=True)
    created_at = db.Column(db.DateTime, default=DT.now())
    updated_at = db.Column(db.DateTime, default=DT.now(), onupdate=DT.now())

    # TODO Customer <has> Users
    # TODO Customer <has> Placeholders
    # TODO Customer <has> Components
    # TODO Customer <has> Visitors
    # TODO Customer <has> Demographics

    def __repr__(self):
        return 'Customer[%r] %r, %r, %r, %r, %r, %r' % \
            (self.id, self.name, self.uuid, self.sites, self.enabled, self.created_at, self.updated_at)