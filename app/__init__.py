from flask import Flask
from flask_restful import Api
from config import app_config
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
jwt = JWTManager()
api = Api(prefix='/api/')


def create_app(config_name):
    app = Flask(__name__)
    # enable cors
    CORS(app)
    app.config.from_object(app_config[config_name])
    db.init_app(app)
    jwt.init_app(app)

    # register blueprints
    from app.auth import auth as auth_blueprint
    from app.events import event
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(event)
    #
    api.init_app(app)


    return app

