# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# High-level models

from datetime import datetime as DT
from app import db

class User(db.Model):
    __tablename__ = "users"
    
    id         = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    name       = db.Column(db.String(80))
    email      = db.Column(db.String(80))
    password   = db.Column(db.String(218))
    enabled    = db.Column(db.Boolean(), default=True)
    admin      = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime, default=DT.now())
    updated_at = db.Column(db.DateTime, default=DT.now(), onupdate=DT.now())
    last_login = db.Column(db.DateTime)

    def __repr__(self):
        return 'User[%r] %r, %r, %r, %r, %r, %r, %r' % \
            (self.id, self.name, self.email, self.enabled, self.is_admin, self.created_at, self.updated_at, self.last_login)