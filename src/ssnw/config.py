import os


class LocalConfig(object):
    use_env = [
        'jwt_expiration_seconds',
    ]
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    def __init__(self):
        for var in self.use_env:
            setattr(self, var.upper(), os.environ.get(var.upper()))

    @property
    def JWT_SECRET(self):
        return os.environ.get('JWT_SECRET').encode('utf-8')

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        user = os.environ.get('POSTGRES_USER')
        password = os.environ.get('POSTGRES_PASSWORD')
        db = os.environ.get('POSTGRES_DB')
        port = os.environ.get('POSTGRES_PORT', 5432)
        return f'postgresql://{user}:{password}@database:{port}/{db}'


configs = {
    'default': LocalConfig,
}
