# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# High-level models

from app import db

class Component(db.Model):
    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # TODO markup
    # TODO created at
    # TODO modified at

    def __repr__(self):
        return 'Component[%r] %r' % (self.id, self.name)