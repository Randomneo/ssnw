import json
from flask import request, Response
from marshmallow import ValidationError


def login_required(func):
    def call(*args, **kwargs):
        if not hasattr(request, 'user') or request.user is None:
            return Response(
                status=401,
                response=json.dumps("Unable to authorize"),
                content_type='application/json',
            )
        return func(*args, **kwargs)
    return call


def input_wrap(func):
    def wrapper(*args, **kwargs):
        request.data = request.form or request.get_json()
        try:
            response = func(*args, **kwargs)
            if not isinstance(response, str):
                response = json.dumps(response)
            return Response(
                response=response,
                content_type='application/json',
            )
        except ValidationError as e:
            return Response(
                status=400,
                response=json.dumps(e.messages),
                content_type='application/json',
            )
    return wrapper
