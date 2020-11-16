import re
import json
from flask import request
from flask.views import MethodView
from marshmallow import ValidationError

from .decorators import login_required
from ..db import db


class Filter(object):
    in_action_split_re = r'[^\\],'
    in_action_escape_clean_re = re.compile(r'\\,')
    bulk_actions = (
        'in', 'notin',
    )
    allowed_actions = [
        'in', 'notin', 'eq', 'ne', 'gt', 'ge', 'lt', 'le', 'like'
    ]

    def bulk_value(func):
        def call(self, model_field, value):
            p = self.in_action_escape_clean_re
            values = [p.sub(',', val) for val in re.split(self.in_action_split_re, value)]
            return func(self, model_field, values)
        return call

    def __init__(self, arg):
        arg_string, self.value = arg
        self.field, action = arg_string.split(':')
        if action not in self.allowed_actions:
            raise ValidationError(f'Not allowed filter action {action}')
        self.action = f'__{action or "eq"}__'
        for action_method in self.bulk_actions:
            setattr(
                self,
                f'__{action_method}__apply__',
                lambda model_field, value: Filter.bulk_value(Filter._apply)(self, model_field, value)
            )

    def _apply(self, model_field, value):
        return getattr(model_field, self.action)(value)

    def apply(self, query, model):
        model_field = getattr(model, self.field)
        schema = getattr(model, '__filter_schema__', model.__schema__)()
        schema_field = schema.fields.get(self.field)
        try:
            value = schema_field.deserialize(self.value)
            applyer = getattr(self, f'{self.action}apply__', self._apply)
            return query.filter(applyer(model_field, value))
        except ValidationError as e:
            raise ValidationError({self.field: e.messages})
        except AttributeError:
            raise ValidationError({self.field: f'Wrong action {self.action.strip("_")}'})


def ModelListView(model):

    class ModelListView(MethodView):
        def build_query(self):
            return db.session.query(model)

        def get_filters(self):
            filters = []
            for arg in request.args.items():
                filters.append(Filter(arg))
            return filters

        def query(self):
            query = self.build_query()
            filters = self.get_filters()
            for filter in filters:
                query = filter.apply(query, model)
            return query

        @login_required
        def get(self):
            schema = model.__schema__(many=True)
            list_name = getattr(model, '__list_name__', f'{model.__name__.lower()}s')
            try:
                response = {
                    list_name: schema.dump(self.query().all())
                }
            except ValidationError as e:
                response = json.dumps(e.messages)
            return response

    return ModelListView
