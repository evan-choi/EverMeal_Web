from flask_login import LoginManager

class LoginManager:
    manager = LoginManager()

    @staticmethod
    def init(app):
        LoginManager.manager.init_app(app)
