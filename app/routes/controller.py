# coding: utf-8
import json
import os
from flask import send_file, request, jsonify
from app.blueprint import basic
from utils.dateUtils import datetimeEx
from core.Core import NeisEngine

updateKey = "6041cef9600a531f527a69186b66bd21"


@basic.route('/')
def index():
    return str(datetimeEx.now())


@basic.route('/task', methods=['GET'])
def download():
    if request.args.get("key") == updateKey:
        filename = os.path.join(os.path.abspath(os.path.dirname(__file__)) + "/../", 'task.db')
        return send_file(filename, as_attachment=True)
    else:
        return jsonify({"result": False})


@basic.route('/clean', methods=['GET'])
def init():
    from app.database import DBManager
    from app.model.article import Article
    from app.model.user import Gcm, Provider
    from core.Core import Allergy

    if request.args.get("key") == updateKey:
        try:
            Allergy.query.delete()
            Gcm.query.delete()
            Provider.query.delete()
            Article.query.delete()

            DBManager.db.session.commit()

            return jsonify({"result": True})
        except:
            DBManager.db.session.rollback()

    return jsonify({"result": False})


# heroku 테스트용
@basic.route('/meal', methods=['GET'])
def meal():
    for s in NeisEngine.SearchFromName("장곡고등학교"):
        return json.dumps(NeisEngine.GetJsonMeals(s, 2016, 7))
