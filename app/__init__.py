# third-party imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app.config import app_config

# db variable initialization
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(app_config['development'])
    app.config.from_pyfile('config.py')
    db.init_app(app)

    from app import models

    migrate = Migrate(app, db)

    from .usersBp import userRoutes as user_blueprint
    app.register_blueprint(user_blueprint)

    from .friendBp import friendsRoutes as friends_blueprint
    app.register_blueprint(friends_blueprint, url_prefix='/friends')

    from .betsBp import betRoutes as bets_blueprint
    app.register_blueprint(bets_blueprint)

    from .authBp import authRoutes as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .likesBp import likeRoutes as likes_blueprint
    app.register_blueprint(likes_blueprint)

    from .transactionBp import transactionRoutes as transaction_routes
    app.register_blueprint(transaction_routes, url_prefix='/transaction')


    return app
