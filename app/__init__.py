from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config, csrf
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object((Config))
db = SQLAlchemy(app)
migrate = Migrate(app, db)
boostrap = Bootstrap(app)

csrf.init_app(app)

from app import routes, models