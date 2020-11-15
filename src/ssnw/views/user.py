import logging
from flask import request
from flask.views import MethodView

from .decorators import input_wrap
from .defaults import ModelListView
from ..db import db
from ..schemas.user import UserSchema
from ..models import User

log = logging.getLogger(__name__)


class UserView(ModelListView(User)):
    def get(self):
        return {'users': UserSchema(many=True).dump(db.session.query(User).all())}


class SignupView(MethodView):
    @input_wrap
    def post(self):
        user_schema = UserSchema()
        user = User(**user_schema.load(data=request.data))
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user)


class LoginView(MethodView):
    def post(self):
        print(request.form)
        return {'message': 'post login'}
