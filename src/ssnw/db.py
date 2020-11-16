from flask_alembic import Alembic
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from marshmallow import ValidationError
from sqlalchemy import MetaData, String

convention = {
  "ix": "ix_%(column_0_label)s",
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)
alembic = Alembic()
bcrypt = Bcrypt()
ma = Marshmallow()


class Column(db.Column):
    __mapping_filters__ = [
        ('__in__', 'in_',),
        ('__notin__', 'notin_',),
    ]

    def __init__(self, *args, **kwargs):
        for filter_mapper in self.__mapping_filters__:
            map_from, map_to = filter_mapper
            setattr(self, map_from, getattr(self, map_to))
        return super().__init__(*args, **kwargs)

    def validate_operation(type):
        def decorate(func):
            def call(self, *args, **kwargs):
                if isinstance(self.type, type):
                    return func(self, *args, **kwargs)
                raise ValidationError(f'{type.__name__} not support {func.__name__.strip("_")} operation')
            return call
        return decorate

    @validate_operation(String)
    def __like__(self, value):
        return self.like(f'%{value}%')


db.Column = Column


def init(app):
    extensions = [alembic, db, bcrypt, ma]
    for extension in extensions:
        extension.init_app(app)
