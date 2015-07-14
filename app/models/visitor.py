# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Visitor Model

import uuid
from app import db

class Visitor(db.Model):
    id   = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(80), default=lambda: str(uuid.uuid4()))

    # TODO nosql id

    def __repr__(self):
        return 'Visitor[%r] %r' % (self.id, self.uuid)