from sqlalchemy import func

from ..db import db


class Audit(object):
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


class Action(db.Model):
    __tablename__ = 'action'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    entity = db.Column(db.String)
    action = db.Column(db.String)
    data = db.Column(db.String)

    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())

    user = db.relationship('User', backref='user.id')
