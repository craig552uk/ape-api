# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Placeholder Model

from app import db

class Placeholder(db.Model):
    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # TODO uid (element class)
    # TODO created at
    # TODO modified at

    def __repr__(self):
        return 'Placeholder[%r] %r' % (self.id, self.name)