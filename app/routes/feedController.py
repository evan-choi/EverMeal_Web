# coding: utf-8
import json

from datetime import datetime
import time

from app.blueprint import basic
from flask import request, jsonify

from app.database import DBManager
from app.model.article import Article
from app.model.neis import ProviderInfo, Neis
from app.model.user import Gcm, Provider
from app.routes import gcmController
from utils.datetime import datetimeEx

updateKey = "6041cef9600a531f527a69186b66bd21"
db = DBManager.db

msg_day_new = "{0}%ec%9b%94{1}%ec%9d%bc+%eb%a9%94%eb%89%b4%ea%b0%80+%ec%98%ac%eb%9d%bc%ec%99%94%ec%8a%b5%eb%8b%88%eb%8b%a4!"
msg_new = "%ec%98%a4%eb%8a%98%ec%9d%98+%eb%a9%94%eb%89%b4%ea%b0%80+%ec%98%ac%eb%9d%bc%ec%99%94%ec%8a%b5%eb%8b%88%eb%8b%a4!"
msg_com = "%ec%97%90+%eb%a6%ac%eb%b7%b0%ea%b0%80+%ec%9e%91%ec%84%b1%eb%90%ac%ec%8a%b5%eb%8b%88%eb%8b%a4!"


@basic.route("/feed", methods=['GET'])
def feeds():
    sid = request.args.get("sid")
    rtime = int(request.args.get("date"))

    datas = []

    for p in Provider.query.filter_by(sid=sid):
        for a in Article.query.filter_by(uploader=p.prov_token):
            a_time = datetimeEx.intFromString(a.upload_date)
            if a_time > rtime:
                fdata = \
                    {
                        "aid": a.aid,
                        "type": a.type,
                        "uploader": a.uploader,
                        "content": a.content,
                        "image_url": a.image_url,
                        "dependency": a.dependency,
                        "upload_date": a_time
                    }
                datas.append(fdata)

    return jsonify(datas)


@basic.route("/feed/update", methods=['GET'])
def update():
    from core.Core import NeisEngine

    result = False

    if request.args.get("key") == updateKey:
        year = request.args.get("year")
        month = request.args.get("month")
        day = request.args.get("day")

        dateStr = "{0}-{1}-{2}".format(year, month, day)

        result = True
        for token in getRegProviders():
            pi = ProviderInfo.query.filter(ProviderInfo.token == token).first()

            if pi.type == 0:
                school = [s for s in NeisEngine.SearchFromToken(token)]

                if len(school) > 0:
                    data = json.loads(NeisEngine.GetJsonMeals(school[0], year, month))

                    for meal in data:
                        if meal['date'] == dateStr:
                            writeMeal(pi, token, meal, year, month, day)
            else:
                processRes(token)

    return jsonify({"result": result})


def writeMeal(pi, token, meal, year, month, day):
    content = json.dumps(meal)

    if write_raw(pi.type, token, content, '', ''):
        processNeis(token, msg_day_new.format(month, day))


@basic.route("/feed/write", methods=['POST'])
def write():
    type = request.json["type"]
    uploader = request.json["uploader"]
    content = request.json["content"]
    image_url = request.json["image_url"]
    dependency = request.json["dependency"]

    result = write_raw(type, uploader, content, image_url, dependency)

    return jsonify({"result": result})


def write_raw(type, uploader, content, image_url, dependency):
    upload_date = datetime.today()
    aid = str(time.mktime(upload_date.timetuple())).split(".")[0]

    a = Article(aid, type, uploader, content, image_url, dependency, upload_date.strftime("%Y-%m-%d %H:%M:%S.%f"))
    db.session.add(a)
    db.session.commit()

    if len(dependency) == 0:
        processNeis(uploader, msg_new)
    else:
        processNeis(dependency, msg_com)

    return True


def getGcmRelation(token):
    gcms = []

    for p in Provider.query.filter(Provider.prov_token == token).all():
        gcm = Gcm.query.filter(Gcm.sid == p.sid).first()
        if gcm is not None:
            gcms.append(gcm.token)

    return gcms


def processNeis(token, message):
    school = Neis.query.filter(Neis.token == token).first()
    gcms = getGcmRelation(token)

    if school is not None:
        gcmController.push(gcms, "EverMeal", "'" + school.name + "' " + message)


def processRes(token):
    pass


def getRegProviders():
    query = db.session.query(Provider.prov_token.distinct().label("prov_token"))

    return [row.prov_token for row in query.all()]
