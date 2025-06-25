from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from yacut.settings import Config


app = Flask(__name__)

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

BASE_URL = 'http://localhost/'

from . import api_views, error_handlers, models, views

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)