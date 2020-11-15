from marshmallow import fields

from ..db import ma
from ..models.user import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True

    email = fields.Email()


User.__schema__ = UserSchema
