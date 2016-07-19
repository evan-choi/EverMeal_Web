from app.blueprint import basic
from flask import request, jsonify

from app.model.user import User


@basic.route('/')
def index():
    return "please"


@basic.route("/api/push")
def push():
    title = request.args.get("title")
    message = request.args.get("message")

    return str(User.query.all())
