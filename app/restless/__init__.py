from app.database import DBManager
from app.model.user import User, Allergy, Provider, GCM
from app.model.neis import ProviderInfo, Neis
from flask_restless import APIManager


def initRestlessApi(app):
    manager = APIManager(app, flask_sqlalchemy_db=DBManager.db)
    manager.create_api(User, methods=['POST'])
    manager.create_api(User, methods=['GET'], include_columns=['sid', 'username', 'email'])

    manager.create_api(GCM, methods=['POST'])

    manager.create_api(Allergy, methods=['GET', 'POST', 'DELETE'])
    manager.create_api(Provider, methods=['GET', 'POST', 'DELETE'])

    manager.create_api(ProviderInfo, methods=['GET'])
    manager.create_api(Neis, methods=['GET'])
