# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Visitor Model

import uuid
from datetime import datetime as DT
from app import db
from app.models import Account

class Visitor(db.Model):
    __tablename__ = "visitors"
    
    id         = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    uuid       = db.Column(db.String(80), default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=DT.now())

    def store_payload(self, payload): # TODO
        """Adds payload to the stored data for this visitor, returns updated visitor data"""
        pass

    def guid(self):
        """Returns a uid for this visitor scoped to this account"""
        return "%s-%s" % (self.account.uuid, self.uuid)

    @classmethod
    def get_or_create(cls, account_uuid, visitor_uuid=None):
        """Returns visitor record with this uuid for account or create and return new"""
        account = Account.query.filter_by(uuid=unicode(account_uuid)).first()

        if account is None:
            raise ValueError("Unknown Account with uuid %s" % account_uuid)

        if visitor_uuid is None:
            visitor = Visitor()
        
        else:
            visitor = Visitor.query.filter_by(account_id=account.id, uuid=unicode(visitor_uuid)).first()
            if visitor:
                return visitor
            else:
                visitor = Visitor(uuid=unicode(visitor_uuid))

                
        account.visitors.append(visitor)
        db.session.add(visitor)
        db.session.commit()
        return visitor

    def __repr__(self):
        return 'Visitor[%r] %r, %r' % (self.id, self.uuid, self.created_at.isoformat())