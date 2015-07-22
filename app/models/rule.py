# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Rule models

from datetime import datetime as DT
from app import db

class Rule(db.Model):
    __tablename__ = "rules"
    
    id         = db.Column(db.Integer, primary_key=True)
    segment_id = db.Column(db.Integer, db.ForeignKey('segments.id'))
    group_id   = db.Column(db.Integer)
    field      = db.Column(db.String(80))
    comparator = db.Column(db.String(80))
    value      = db.Column(db.String(80))
    created_at = db.Column(db.DateTime, default=DT.now())
    updated_at = db.Column(db.DateTime, default=DT.now(), onupdate=DT.now())

    def __repr__(self):
        return 'Rule[%r] %r, %r, %r, %r, %r, %r, %r' % \
            (self.id, self.segment_id, self.group_id, self.field, self.comparator, self.value, self.created_at.isoformat(), self.updated_at.isoformat())