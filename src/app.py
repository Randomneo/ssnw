import os
from flask import Flask
from ssnw.db import db
from ssnw.config import configs

app = Flask(__name__)
config = (configs.get(os.getenv('FLASK_CONFIG'), '').lower() or configs['default'])()
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    db.session.query()
    return 'hello world'
