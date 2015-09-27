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
from passlib.hash import pbkdf2_sha256 as hasher
from app import db


class Password(db.TypeDecorator):
    """Custom field type for storing passwords"""
    impl = db.String(40)

    def process_bind_param(self, value, dialect):
        return hasher.encrypt(value)


class User(db.Model):
    __tablename__ = "users"
    
    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(80))
    email      = db.Column(db.String(80))
    password   = db.Column(Password())
    enabled    = db.Column(db.Boolean(), default=True)
    admin      = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime, default=DT.now())
    updated_at = db.Column(db.DateTime, default=DT.now(), onupdate=DT.now())
    last_login = db.Column(db.DateTime)

    @classmethod
    def authenticate(cls, email, password):
        user = cls.query.filter_by(email=email).first()
        if user and hasher.verify(password, user.password):
            return user

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
        is_admin   = "ADMIN"   if (self.admin)   else "NOT ADMIN"
        is_enabled = "ENABLED" if (self.enabled) else "DISABLED"
        last_login = self.last_login.isoformat() if self.last_login else "NO LOGIN"
        return 'User[%r] %r, %r, %r, %r, %r, %r, %r' % \
            (self.id, self.name, self.email, is_enabled, is_admin, self.created_at.isoformat(), self.updated_at.isoformat(), last_login)