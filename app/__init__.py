from flask import Flask

def create_app():
    app = Flask(__name__)

    # Init Config
    from app.config.appConfig import AppConfig
    app.config.from_object(AppConfig)

    #init routes
    from app.routes import controller

    # Init Database
    from app.database import DBManager
    DBManager.init(app)

    # Init Flask-restless
    from app.restless import initRestlessApi
    initRestlessApi(app)

    # Init Blueprint
    from app.blueprint import basic
    app.register_blueprint(basic)
    return app

