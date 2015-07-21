# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Segment models

from app import db

class Segment(db.Model): # TODO rename to Segments
    __tablename__ = "segments"
    
    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    
    # TODO enabled
    # TODO created at
    # TODO modified at

    # TODO Segment <has> Rules

    def __repr__(self):
        return 'Segment[%r] %r' % (self.id, self.name)