# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# High-level models

from datetime import datetime as DT
from app import db

class Component(db.Model):
    __tablename__ = "components"

    id             = db.Column(db.Integer, primary_key=True)
    placeholder_id = db.Column(db.Integer, db.ForeignKey('placeholders.id'))
    index          = db.Column(db.Integer)
    name           = db.Column(db.String(80))
    markup         = db.Column(db.String(80))
    created_at     = db.Column(db.DateTime, default=DT.now())
    updated_at     = db.Column(db.DateTime, default=DT.now(), onupdate=DT.now())

    def __repr__(self):
        return 'Component[%r] %r, %r, %r, %r' % \
            (self.id, self.name, self.index, self.created_at, self,updated_at)