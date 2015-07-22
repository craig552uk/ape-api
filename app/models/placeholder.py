# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Placeholder Model

from sqlalchemy.orm import relationship
from app import db

class Placeholder(db.Model):
    __tablename__ = "placeholders"
    
    id         = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    name       = db.Column(db.String(80))

    components = relationship("Component", backref="placeholder")

    # TODO uuid (element class)
    # TODO created_at
    # TODO modified_at

    def __repr__(self):
        return 'Placeholder[%r] %r' % (self.id, self.name)