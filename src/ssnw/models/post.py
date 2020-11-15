from ..db import db
from .audit import Audit
from .user import User


class Post(db.Model, Audit):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)

    author_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
