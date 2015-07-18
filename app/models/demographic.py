# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# High-level models

from app import db

class Demographic(db.Model): # TODO rename to Segments
    __tablename__ = "demographics"
    
    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    
    # TODO rules (pickled dicts)
    # TODO enabled
    # TODO created at
    # TODO modified at

    def __repr__(self):
        return 'Demographic[%r] %r' % (self.id, self.name)