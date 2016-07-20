# coding: utf-8
from pushjack import GCMClient

from app.blueprint import basic
from flask import request, jsonify

from app.database import DBManager
from app.model.user import Gcm

db = DBManager.db
client = GCMClient(api_key='AIzaSyBsj2v--Ul2ou5VVEhCFRJvEtC-u1dT9A4')


@basic.route("/push/route")
def route():
    title = request.args.get("title")
    message = request.args.get("message")

    tokens = []
    for gcm in Gcm.query.all():
        tokens.append(gcm.token)

    res = push(tokens, title, message)

    return str(res.responses)


@basic.route("/api/gcm", methods=['POST'])
def gcm_add():
    sid = request.json["sid"]
    token = request.json["token"]

    gcm = Gcm.query.filter_by(sid=sid).first()

    if gcm is None:
        db.session.add(Gcm(sid, token))
    else:
        gcm.token = token

    db.session.commit()

    return jsonify({"result": True})


def push(tokens, title, message):
    alert = {'message': message, 'title': title}
    return client.send(tokens, alert)
