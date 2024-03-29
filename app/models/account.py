# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Account Model

import uuid
from datetime import datetime as DT
from sqlalchemy.orm import relationship
from app import db


# Table for many-to-many relationship between accounts and users
accounts_users = db.Table('accounts_users', db.Model.metadata,
    db.Column('account_id', db.Integer, db.ForeignKey('accounts.id')),
    db.Column('user_id',    db.Integer, db.ForeignKey('users.id'))
)


class Account(db.Model):
    __tablename__ = "accounts"

    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(80))
    uuid       = db.Column(db.String(80), default=lambda: str(uuid.uuid4()))
    sites      = db.Column(db.PickleType(), default=[])
    enabled    = db.Column(db.Boolean(), default=True)
    created_at = db.Column(db.DateTime, default=DT.now())
    updated_at = db.Column(db.DateTime, default=DT.now(), onupdate=DT.now())

    users        = relationship("User", backref="accounts", secondary=accounts_users)
    visitors     = relationship("Visitor", backref="account")
    placeholders = relationship("Placeholder", backref="account")
    segments     = relationship("Segment", backref="account")

    def url_in_sites(self, url):
        """Returns true if the requested url belongs to one of the sites owned by this account"""
        url = url.lstrip("http://")
        url = url.lstrip("https://")

        for site in self.sites:
            if url.startswith(site): return True
        return False

    def to_dict(self):
        """Dictionary representation"""
        return {
            'type'       : "account",
            'id'         : self.id,
            'name'       : self.name,
            'uuid'       : self.uuid,
            'sites'      : self.sites,
            'enabled'    : self.enabled,
            'created_at' : self.created_at,
            'updated_at' : self.updated_at,
            'user_ids'   : [u.id for u in self.users]
        }

    def __repr__(self):
        return 'Account[%r] %r, %r, %r, %r, %r, %r' % \
            (self.id, self.name, self.uuid, self.sites, self.enabled, self.created_at.isoformat(), self.updated_at.isoformat())