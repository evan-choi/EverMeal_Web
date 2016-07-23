# coding: utf-8
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = '6041cef9600a531f527a69186b66bd21'

    # Init Config
    from app.config.appConfig import AppConfig
    app.config.from_object(AppConfig)

    # Init Database
    from app.database import DBManager
    DBManager.init(app)

    # Init routes
    from app.routes import controller
    from app.routes import feedController
    from app.routes import gcmController
    from app.routes import providerController
    from app.routes.cms import loginController

    # Init Login
    from app.loginManager import LoginManager
    LoginManager.init(app)

    # Init Flask-restless
    from app.restless import initRestlessApi
    initRestlessApi(app)

    # Init Blueprint
    from app.blueprint import basic
    app.register_blueprint(basic)

    return app
