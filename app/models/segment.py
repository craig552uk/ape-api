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

    def matches_data(self, visitor_data):
        """Return true if segment rules accept visitor_data, return false otherwise"""
        results = dict()

        # Always false if no rules defined
        if not self.rules: return False
        
        # Apply each child rule to visitor_data
        for rule in self.rules:
            # Logical OR results within the same group
            gid = rule.group_id
            results[gid] = results.get(gid, False) or rule.apply(visitor_data)

        # Logical AND results between groups
        return False not in results.values()

    def rules_in_groups(self):
        """
            Return dict of rules grouped by group id.
            Useful for presenting rules in views
        """
        groups = dict()
        for rule in self.rules:
            gid = rule.group_id
            groups[gid] = groups.get(gid, list()) + [rule]
        return groups

    def __repr__(self):
        return 'Segment[%r] %r, %r, %r' % (self.id, self.name, self.created_at.isoformat(), self.updated_at.isoformat())