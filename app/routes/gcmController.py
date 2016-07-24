# coding: utf-8
from pushjack import GCMClient

from app.blueprint import basic
from flask import request, jsonify, redirect, url_for

from app.database import DBManager
from app.model.user import Gcm, Push
from utils.dateUtils import datetimeEx

db = DBManager.db
client = GCMClient(api_key='AIzaSyBsj2v--Ul2ou5VVEhCFRJvEtC-u1dT9A4')

gTypePreset = ["Message", "Feed", "Review"]

class GcmType:
    Message = 0
    Feed = 1
    Review = 2

    @staticmethod
    def toStrig(self):
        return gTypePreset[int(self)]


@basic.route("/push/route", methods=['GET', 'POST'])
def route():
    fromWeb = False

    if request.method == 'GET':
        title = request.args.get("title")
        message = request.args.get("message")
    else:
        fromWeb = True
        title = request.form['title']
        message = request.form['message']

    tokens = []
    for gcm in Gcm.query.all():
        tokens.append(gcm.token)

    if fromWeb:
        sender = "admin"
    else:
        sender = "web"

    res = push(tokens, title, message, GcmType.Message, sender, None)

    if fromWeb:
        return redirect('/admin?menu=push')
    else:
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


def push(tokens, title, message, gcmtype, sender, params):
    alert = {'message': message, 'title': title, 'type': str(int(gcmtype))}

    if params is not None:
        alert.update(params)

    try:
        db.session.add(Push(title, message, GcmType.toStrig(gcmtype), sender, datetimeEx.now()))
        db.session.commit()
    except:
        pass

    return client.send(tokens, alert)
