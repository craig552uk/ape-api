# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# High-level models

from app import db

class Component(db.Model):
    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __repr__(self):
        return '<Component [%s] %s>' % (self.id, self.name)