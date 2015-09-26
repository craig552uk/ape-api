# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# High-level models
# 
# When logging in to the portal a user can see all accounts to which they are associated
# An admin user can see all accounts and can impersonate any other user
# Only an admin can create users and accounts
# An agency user will have visibility of all client accounts
# A client user will have visibility of their own account only

from datetime import datetime as DT
from app import db

class User(db.Model):
    __tablename__ = "users"
    
    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(80))
    email      = db.Column(db.String(80))
    password   = db.Column(db.String(218))
    enabled    = db.Column(db.Boolean(), default=True)
    admin      = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime, default=DT.now())
    updated_at = db.Column(db.DateTime, default=DT.now(), onupdate=DT.now())
    last_login = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'type':        "user",
            'id':          self.id,
            'name':        self.name,
            'email':       self.email,
            'password':    self.password,
            'enabled':     self.enabled,
            'admin':       self.admin,
            'created_at':  self.created_at,
            'updated_at':  self.updated_at,
            'last_login':  self.last_login,
        }

    def __repr__(self):
        if self.last_login:
            return 'User[%r] %r, %r, %r, %r, %r, %r, %r' % \
                (self.id, self.name, self.email, self.enabled, self.admin, self.created_at.isoformat(), self.updated_at.isoformat(), self.last_login.isoformat())
        else:
            return 'User[%r] %r, %r, %r, %r, %r, %r, %r' % \
                (self.id, self.name, self.email, self.enabled, self.admin, self.created_at.isoformat(), self.updated_at.isoformat(), "Never Logged In")
