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


class LikePostView(MethodView):

    @login_required
    @input_wrap
    def post(self, id):
        like_schema = LikeSchema()
        post = db.session.query(Post).filter(Post.id == id).first()
        if post is None:
            raise ValidationError('Post not found')
        like = db.session.query(Like)\
            .filter(
                Like.post_id == post.id,
                Like.user_id == request.user.id,
            )\
            .first()
        if like is not None:
            db.session.delete(like)
            db.session.commit()
            return {"message": "Like sucessfully deleted"}
        like = Like(user_id=request.user.id, post_id=post.id)
        db.session.add(like)
        db.session.commit()
        return like_schema.dump(like)
