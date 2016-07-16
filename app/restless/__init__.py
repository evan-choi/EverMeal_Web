from app.database import DBManager
from app.model.user import User
from flask.ext.restless import APIManager

def initRestlessApi(app):
    manager = APIManager(app, flask_sqlalchemy_db=DBManager.db)
    manager.create_api(User, methods=['GET', 'POST', 'DELETE'])