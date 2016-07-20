import os
from flask import send_file, request, jsonify

from app.blueprint import basic

updateKey = "6041cef9600a531f527a69186b66bd21"


@basic.route('/')
def index():
    return u"이건 되나"


@basic.route('/task', methods=['GET'])
def download():
    if request.args.get("key") == updateKey:
        filename = os.path.join(os.path.abspath(os.path.dirname(__file__)) + "/../", 'task.db')
        return send_file(filename, as_attachment=True)
    else:
        return jsonify({"result": False})
