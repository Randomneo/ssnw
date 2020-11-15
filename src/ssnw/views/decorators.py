from flask import request
from marshmallow import ValidationError


def input_wrap(func):
    def wrapper(*args, **kwargs):
        request.data = request.form or request.get_json()
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            return e.messages
    return wrapper
