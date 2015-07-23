# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Placeholder Model

import uuid
from datetime import datetime as DT
from sqlalchemy.orm import relationship
from app import db

class Placeholder(db.Model):
    __tablename__ = "placeholders"
    
    id         = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    name       = db.Column(db.String(80))
    uuid       = db.Column(db.String(80), default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=DT.now())
    updated_at = db.Column(db.DateTime, default=DT.now(), onupdate=DT.now())

    components = relationship("Component", backref="placeholder")

    def get_component_for_segments(self, segments): # TODO
        """Return correct conponent for this segment set"""
        pass

    def __repr__(self):
        return 'Placeholder[%r] %r, %r, %r, %r' % \
            (self.id, self.name, self.uuid, self.created_at.isoformat(), self.updated_at.isoformat())