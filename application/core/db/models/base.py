from datetime import datetime

from flask_restplus import fields

from application import db


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    api_created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    api_updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    api_status = db.Column(db.Boolean, nullable=False, default=True)

    @classmethod
    def schema(cls):
        schema = {'id': fields.Integer(readOnly=True, description="Identifier"),
                  'api_created_at': fields.DateTime(readOnly=True, description="Creation date and time")}
        return schema

    @classmethod
    def schema_paginated(cls):
        schema = {'items': fields.List(fields.Nested(cls.schema())),
                  'prev_page': fields.String(required=True),
                  'next_page': fields.String(required=True),
                  'total_items': fields.Integer(required=True)}
        return schema