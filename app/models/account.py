# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Account Model

import uuid
from app import db
from datetime import datetime as DT

class Account(db.Model):
    __tablename__ = "accounts"

    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(80))
    uuid       = db.Column(db.String(80), default=lambda: str(uuid.uuid4()))
    sites      = db.Column(db.PickleType(), default=[])
    enabled    = db.Column(db.Boolean(), default=True)
    created_at = db.Column(db.DateTime, default=DT.now())
    updated_at = db.Column(db.DateTime, default=DT.now(), onupdate=DT.now())

    # TODO Account <has> Users
    # TODO Account <has> Placeholders
    # TODO Account <has> Components
    # TODO Account <has> Visitors
    # TODO Account <has> Segments

    def __repr__(self):
        return 'Account[%r] %r, %r, %r, %r, %r, %r' % \
            (self.id, self.name, self.uuid, self.sites, self.enabled, self.created_at, self.updated_at)