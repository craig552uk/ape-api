# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Visitor Model

import uuid
import shelve
from datetime import datetime as DT
from app import app, db
from app.models import Account

class Visitor(db.Model):
    __tablename__ = "visitors"
    
    id         = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    uuid       = db.Column(db.String(80), default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=DT.now())


    DEFAULT_DATA = dict(visitor_id=None, account_id=None, sessions=[])

    def store_payload(self, payload):
        """Adds payload to the stored data for this visitor, returns updated visitor data"""
        s = shelve.open(app.config.get('SHELVE_PATH'))
        data = s.get(self.guid(), dict())
        # data = Visitor.insert_payload_to_data(data, payload) # TODO
        s[self.guid()] = data
        s.close()
        return data

    def guid(self):
        """Returns a uid for this visitor scoped to this account"""
        return str("%s-%s" % (self.account.uuid, self.uuid))

    @classmethod
    def get_or_create(cls, account, visitor_uuid=None):
        """Returns visitor record with this uuid for account or create and return new"""

        if visitor_uuid:
            visitor = Visitor.query.filter_by(account_id=account.id, uuid=unicode(visitor_uuid)).first()
            if visitor:
                return visitor
            else:
                visitor = Visitor(uuid=unicode(visitor_uuid))
    
        else:
            visitor = Visitor()

        account.visitors.append(visitor)
        db.session.add(visitor)
        db.session.commit()
        return visitor

    def __repr__(self):
        return 'Visitor[%r] %r, %r' % (self.id, self.uuid, self.created_at.isoformat())