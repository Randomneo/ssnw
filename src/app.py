import os
from flask import Flask
from flask_alembic import Alembic

from ssnw.db import db
from ssnw.config import configs
from ssnw.models import *    # NOQA

app = Flask(__name__)
config = (configs.get(os.getenv('FLASK_CONFIG'), '').lower() or configs['default'])()
app.config.from_object(config)

alembic = Alembic()
alembic.init_app(app)
db.init_app(app)


@app.route('/')
def index():
    db.session.query()
    return 'hello world'
