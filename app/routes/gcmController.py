# coding: utf-8
from pushjack import GCMClient

from app.blueprint import basic
from flask import request, jsonify

from app.database import DBManager
from app.model.user import Gcm

db = DBManager.db
client = GCMClient(api_key='AIzaSyBsj2v--Ul2ou5VVEhCFRJvEtC-u1dT9A4')


class GcmType:
    Message = 0
    Feed = 1
    Review = 2


@basic.route("/push/route")
def route():
    title = request.args.get("title")
    message = request.args.get("message")

    tokens = []
    for gcm in Gcm.query.all():
        tokens.append(gcm.token)

    res = push(tokens, title, message, GcmType.Message)

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


def push(tokens, title, message, gcmtype):
    alert = {'message': message, 'title': title, 'type': str(int(gcmtype))}
    return client.send(tokens, alert)
