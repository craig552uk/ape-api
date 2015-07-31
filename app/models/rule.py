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


    def compare(self, field_value):
        """Compare configured value to field value using comparator"""
        test_value = self.value # Easier to read variable name
        try:
            if   self.comparator == "MATCH":          return test_value == field_value
            elif self.comparator == "NOT_MATCH":      return test_value != field_value
            elif self.comparator == "CONTAIN":        return test_value in field_value
            elif self.comparator == "NOT_CONTAIN":    return test_value not in field_value
            elif self.comparator == "START_WITH":     return field_value.startswith(test_value)
            elif self.comparator == "NOT_START_WITH": return not field_value.startswith(test_value)
            elif self.comparator == "END_WITH":       return field_value.endswith(test_value)
            elif self.comparator == "NOT_END_WITH":   return not field_value.endswith(test_value)
            elif self.comparator == "LESS_THAN":      return int(test_value) < int(field_value)
            elif self.comparator == "GREATER_THAN":   return int(test_value) > int(field_value)
            else: return False
        except Exception as e:
            print e # TODO logging
            return False


    def __repr__(self):
        return 'Rule[%r] %r, %r, %r, %r, %r, %r, %r' % \
            (self.id, self.segment_id, self.group_id, self.field, self.comparator, self.value, self.created_at.isoformat(), self.updated_at.isoformat())