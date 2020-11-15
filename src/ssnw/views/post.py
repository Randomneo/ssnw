from flask import request
from flask.views import MethodView

from .defaults import ModelListView
from .decorators import login_required, input_wrap
from ..db import db
from ..models.post import Post
from ..schemas.post import PostSchema



class PostListView(ModelListView(Post)):

    @login_required
    @input_wrap
    def post(self):
        post_schema = PostSchema()
        post = Post(**post_schema.load(data=request.data), author_id=request.user.id)
        db.session.add(post)
        db.session.commit()
        return post_schema.dump(post)


class PostDetailView(MethodView):

    @login_required
    @input_wrap
    def get(self, id):
        post_schema = PostSchema()
        post = db.session.query(Post).filter(Post.id == id).first()
        return post_schema.dump(post)
