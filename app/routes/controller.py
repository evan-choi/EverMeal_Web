# coding: utf-8

import os
from flask import send_file, request, jsonify

from app.blueprint import basic
from app.database import DBManager
from app.model.article import Article
from app.model.user import Gcm, Provider
from core.Core import Allergy

updateKey = "6041cef9600a531f527a69186b66bd21"


@basic.route('/')
def index():
    return "될까?"


@basic.route('/task', methods=['GET'])
def download():
    if request.args.get("key") == updateKey:
        filename = os.path.join(os.path.abspath(os.path.dirname(__file__)) + "/../", 'task.db')
        return send_file(filename, as_attachment=True)
    else:
        return jsonify({"result": False})


@basic.route('/task', methods=['DELETE'])
def init():
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