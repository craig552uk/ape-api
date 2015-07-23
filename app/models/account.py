# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Account Model

import uuid
from datetime import datetime as DT
from sqlalchemy.orm import relationship
from app import db

class Account(db.Model):
    __tablename__ = "accounts"

    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(80))
    uuid       = db.Column(db.String(80), default=lambda: str(uuid.uuid4()))
    sites      = db.Column(db.PickleType(), default=[])
    enabled    = db.Column(db.Boolean(), default=True)
    created_at = db.Column(db.DateTime, default=DT.now())
    updated_at = db.Column(db.DateTime, default=DT.now(), onupdate=DT.now())

    users        = relationship("User", backref="account")
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

    @classmethod
    def can_track(cls, account_uuid, url): # TODO
        """Returns true if account exists, is enabled and owns this site"""
        account = Account.query.filter_by(uuid=account_uuid).first()
        if account:
            return account and account.enabled and account.url_in_sites(url)
        return False

    def __repr__(self):
        return 'Account[%r] %r, %r, %r, %r, %r, %r' % \
            (self.id, self.name, self.uuid, self.sites, self.enabled, self.created_at.isoformat(), self.updated_at.isoformat())