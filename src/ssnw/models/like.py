from ..db import db
from .audit import Audit
from .user import User
from .post import Post


class Like(db.Model, Audit):
    __tablename__ = 'like'
    __table_args__ = (
        db.UniqueConstraint('user_id', 'post_id'),
    )

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(Post.id), nullable=False)

    user = db.relationship(User, backref='likers')
    post = db.relationship(Post, backref=db.backref('post', uselist=False))
