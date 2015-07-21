# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Visitor Model

import uuid
from app import db

class Visitor(db.Model):
    __tablename__ = "visitors"
    
    id         = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    uuid       = db.Column(db.String(80), default=lambda: str(uuid.uuid4())) # TODO account.id + random id

    # TODO created_at

    def __repr__(self):
        return 'Visitor[%r] %r' % (self.id, self.uuid)