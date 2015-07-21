# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Placeholder Model

from app import db

class Placeholder(db.Model):
    __tablename__ = "placeholders"
    
    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # TODO uuid (element class)
    # TODO created_at
    # TODO modified_at

    def __repr__(self):
        return 'Placeholder[%r] %r' % (self.id, self.name)