# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Segment models

from datetime import datetime as DT
from sqlalchemy.orm import relationship
from app import db

class Segment(db.Model):
    __tablename__ = "segments"
    
    id         = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    name       = db.Column(db.String(80))
    created_at = db.Column(db.DateTime, default=DT.now())
    updated_at = db.Column(db.DateTime, default=DT.now(), onupdate=DT.now())

    rules = relationship("Rule", backref="segment")

    def __repr__(self):
        return 'Segment[%r] %r, %r, %r' % (self.id, self.name, self.created_at.isoformat(), self.updated_at.isoformat())