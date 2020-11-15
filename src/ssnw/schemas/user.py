from marshmallow import fields, validate, Schema

from ..db import ma
from ..models.user import User


class LoginSchema(Schema):
    login = fields.String(validate=validate.Length(min=5, max=64), required=True)
    password = fields.String(load_only=True, validate=validate.Length(min=8, max=128), required=True)


class UserSchema(ma.SQLAlchemyAutoSchema, LoginSchema):
    class Meta:
        model = User
        include_fk = True
        exclude = ('_password',)

    email = fields.Email(validate=validate.Length(max=128))


User.__schema__ = UserSchema
