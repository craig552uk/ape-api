# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Rule models

from app import db

class Rule(db.Model): # TODO rename to Rules
    __tablename__ = "rules"
    
    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    
    # TODO created at
    # TODO modified at
    # TODO group_id
    # TODO field
    # TODO comparator
    # TODO value

    def __repr__(self):
        return 'Rule[%r] %r' % (self.id, self.name)