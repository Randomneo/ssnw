from flask import request
from flask.views import MethodView
from marshmallow import ValidationError

from .defaults import ModelListView
from .decorators import login_required, input_wrap
from ..db import db
from ..models.like import Like
from ..models.post import Post
from ..schemas.like import LikeSchema


class LikeListView(ModelListView(Like)):
    pass


class LikeAction(object):
    def get_like(self, post_id):
        post = db.session.query(Post).filter(Post.id == post_id).first()
        if post is None:
            raise ValidationError('Post not found')
        like = db.session.query(Like)\
            .filter(
                Like.post_id == post.id,
                Like.user_id == request.user.id,
            )\
            .first()
        return like


class LikePostView(MethodView, LikeAction):

    @login_required
    @input_wrap
    def post(self, post_id):
        like_schema = LikeSchema()
        like = self.get_like(post_id)
        if like is not None:
            raise ValidationError('Post already liked')
        like = Like(user_id=request.user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
        return like_schema.dump(like)


class DisLikePostView(MethodView, LikeAction):
    @login_required
    @input_wrap
    def post(self, post_id):
        like_schema = LikeSchema()
        like = self.get_like(post_id)
        if like is None:
            raise ValidationError('Post not yet liked')
        db.session.delete(like)
        db.session.commit()
        return like_schema.dump(like)
