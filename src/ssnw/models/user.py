from ..db import db
from .audit import Audit


class User(db.Model, Audit):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    surname = db.Column(db.String, nullable=True)

    login = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)

    last_login = db.Column(db.DateTime, nullable=True)
