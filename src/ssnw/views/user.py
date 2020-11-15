import jwt
import json
import logging
import datetime
from flask import request, current_app, Response
from flask.views import MethodView
from marshmallow import ValidationError

from .decorators import input_wrap
from .defaults import ModelListView
from ..db import db, bcrypt
from ..schemas.user import UserSchema, LoginSchema
from ..models import User
from ..utils import jwt_encode, jwt_decode

log = logging.getLogger(__name__)


@current_app.before_request
def get_user():
    request.user = None
    try:
        auth_token = request.headers.get('Authorization')
        if not auth_token:
            return
        data = jwt_decode(auth_token)
        request.user = db.session.query(User).filter(User.id == data['user_id']).first()
    except (jwt.DecodeError, jwt.ExpiredSignatureError):
        return Response(
            status=401,
            response=json.dumps('Provided token is invalid'),
            content_type='application/json'
        )
    except Exception as e:
        log.exception(e)


class UserListView(ModelListView(User)):
    pass


class SignupView(MethodView):
    @input_wrap
    def post(self):
        user_schema = UserSchema()
        user = User(**user_schema.load(data=request.data))
        # TODO: Email confirmation
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user)


class LoginView(MethodView):
    @input_wrap
    def post(self):
        login_schema = LoginSchema()
        user_input = login_schema.load(data=request.data)
        user = db.session.query(User).filter(User.login == user_input.get('login')).first()
        if not bcrypt.check_password_hash(user.password, user_input.get('password')):
            raise ValidationError('Unable to login')
        jwt_exp_sec = current_app.config['JWT_EXPIRATION_SECONDS']
        data = {
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=int(jwt_exp_sec)),
        }
        token = jwt_encode(data)

        return {'token': token.decode('utf-8')}
