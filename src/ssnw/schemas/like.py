from marshmallow import fields
from ..db import ma
from ..models.like import Like


class LikeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Like
        include_fk = True

    author_id = fields.Integer(dumps_only=True)


Like.__schema__ = LikeSchema
