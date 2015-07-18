# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# High-level models

from app import db

class User(db.Model):
    __tablename__ = "users"
    
    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # TODO email
    # TODO password
    # TODO is admin
    # TODO enabled
    # TODO created at
    # TODO modified at
    # TODO last logged in

    def __repr__(self):
        return 'User[%r] %r' % (self.id, self.name)