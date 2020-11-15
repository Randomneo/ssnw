from marshmallow import fields
from ..db import ma
from ..models.post import Post


class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        include_fk = True

    author_id = fields.Integer(dumps_only=True)


Post.__schema__ = PostSchema
