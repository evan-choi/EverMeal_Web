# coding: utf-8
import datetime
from flask import request, jsonify
from app.blueprint import basic
from app.database import DBManager
from app.model.user import Provider
from app.routes.feedController import update_raw
from utils.dateUtils import datetimeEx

db = DBManager.db


@basic.route('/provider', methods=['POST'])
def provider():
    time = datetimeEx.now()
    sid = request.json['sid']
    prov_token = request.json['prov_token']

    isNew = (Provider.query.filter_by(prov_token=prov_token).count() == 0)

    if isNew:
        d = datetimeEx.localize(datetime.datetime.now())
        tday = d.day

        if d.hour >= 7:
            tday += 1

        sday = max(tday - 7, 1)

        for i in range(sday, tday):
            update_raw(d.year, d.month, i, [prov_token])

    if Provider.query.filter_by(sid=sid, prov_token=prov_token).count() == 0:
        p = Provider(sid, prov_token, time)

        db.session.add(p)
        db.session.commit()

    return jsonify(
        {
            "sid": sid,
            "prov_token": prov_token
        })
