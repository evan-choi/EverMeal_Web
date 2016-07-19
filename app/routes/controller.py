from pushjack import GCMClient

from app.blueprint import basic
from flask import request
from app.model.user import Gcm


client = GCMClient(api_key='AIzaSyBsj2v--Ul2ou5VVEhCFRJvEtC-u1dT9A4')


@basic.route('/')
def index():
    return "please"


@basic.route("/push/route")
def push():
    title = request.args.get("title")
    message = request.args.get("message")

    alert = {'message': message, 'title': title}

    for gcm in Gcm.query.all():
        res = client.send(gcm.token, alert)

    return str(res.responses)
