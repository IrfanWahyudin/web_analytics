from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
app = Flask(__name__)

from flask_login import LoginManager
login = LoginManager(app)

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)
migrate.init_app(app)
from app import routes, models  

