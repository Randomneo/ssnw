import os
from flask import Flask

from ssnw.db import init as db_init, db   # NOQA
from ssnw.models import *    # NOQA
from ssnw.config import configs


def create_app():
    app = Flask(__name__)
    config = (configs.get(os.getenv('FLASK_CONFIG'), '').lower() or configs['default'])()
    app.config.from_object(config)

    db_init(app)

    with app.app_context():
        import ssnw.urls   # NOQA

    return app
