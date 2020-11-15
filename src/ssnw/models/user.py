from sqlalchemy.ext.hybrid import hybrid_property

from ..db import db, bcrypt
from .audit import Audit


class User(db.Model, Audit):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=True)
    surname = db.Column(db.String(64), nullable=True)

    login = db.Column(db.String(64), nullable=False, unique=True)
    _password = db.Column('password', db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)

    last_login = db.Column(db.DateTime, nullable=True)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = bcrypt.generate_password_hash(value).decode('utf-8')
