import jwt
from flask import current_app

JWT_SECRET = current_app.config.get('JWT_SECRET')
JWT_ALGORITHM = 'HS256'


def jwt_encode(data):
    return jwt.encode(data, JWT_SECRET, JWT_ALGORITHM)


def jwt_decode(token):
    return jwt.decode(token, JWT_SECRET, JWT_ALGORITHM)
