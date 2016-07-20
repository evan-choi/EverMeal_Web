from datetime import datetime
from flask import request, jsonify
from app.blueprint import basic
from app.database import DBManager
from app.model.user import Provider
from utils.datetime import datetimeEx

db = DBManager.db


@basic.route('/provider', methods=['POST'])
def provider():
    time = datetimeEx.intFromString(str(datetime.today()))
    sid = request.json['sid']
    prov_token = request.json['prov_token']

    if Provider.query.filter_by(sid=sid, prov_token=prov_token).count() == 0:
        p = Provider(sid, prov_token, time)

        db.session.add(p)
        db.session.commit()

        return jsonify(
            {
                "sid": sid,
                "prov_token": prov_token
            })
    else:
        return jsonify({"result": False})
