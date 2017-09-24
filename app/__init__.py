# third-party imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


from app.config import app_config

# db variable initialization
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)

    from app import models

    migrate = Migrate(app, db)

    from .bets import bets as bets_blueprint
    app.register_blueprint(bets_blueprint, url_prefix='/bets')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)


    return app
