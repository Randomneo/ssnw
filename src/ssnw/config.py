import os


class LocalConfig(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

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
