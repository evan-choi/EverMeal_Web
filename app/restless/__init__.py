from app.database import DBManager
from app.model.user import User, Allergy, Provider
from flask.ext.restless import APIManager

def initRestlessApi(app):
    manager = APIManager(app, flask_sqlalchemy_db=DBManager.db)
    manager.create_api(User, methods=['GET'])
    manager.create_api(Allergy, methods=['GET', 'PUT', 'DELETE'])
    manager.create_api(Provider, methods=['GET', 'PUT', 'DELETE'])
