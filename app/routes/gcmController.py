from pushjack import GCMClient

from app.blueprint import basic
from flask import request

from app.model.user import Gcm


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


def push(tokens, title, message):
    alert = {'message': message, 'title': title}
    return client.send(tokens, alert)
