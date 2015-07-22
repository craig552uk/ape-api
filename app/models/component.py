# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# High-level models

from app import db

class Component(db.Model):
    __tablename__ = "components"

    id             = db.Column(db.Integer, primary_key=True)
    placeholder_id = db.Column(db.Integer, db.ForeignKey('placeholders.id'))
    name           = db.Column(db.String(80))

    # TODO order
    # TODO markup
    # TODO created_at
    # TODO updated_at

    def __repr__(self):
        return 'Component[%r] %r' % (self.id, self.name)