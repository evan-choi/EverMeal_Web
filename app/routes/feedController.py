# coding: utf-8
import json

from datetime import datetime
import time

from sqlalchemy import func

from app.blueprint import basic
from flask import request, jsonify

from app.database import DBManager
from app.model.article import Article, Rate
from app.model.neis import ProviderInfo, Neis
from app.model.user import Gcm, Provider
from app.routes import gcmController
from app.routes.gcmController import GcmType
from utils.dateUtils import datetimeEx

updateKey = "6041cef9600a531f527a69186b66bd21"
db = DBManager.db

msg_day_new = u"{0}월{1}일 메뉴가 올라왔습니다!"
msg_new = u"오늘의 메뉴가 올라왔습니다!"
msg_com = u"에 리뷰가 작성됬습니다!"


@basic.route("/comment", methods=['GET'])
def comments():
    aid = request.args.get("aid")
    rtime = int(request.args.get("date"))

    datas = []

    for cmt in Article.query.filter_by(dependency=aid):
        a_time = int(str(cmt.upload_date).split(".")[0])
        if a_time > rtime:
            fdata = \
                {
                    "aid": cmt.aid,
                    "content": cmt.content,
                    "dependency": cmt.dependency,
                    "upload_date": a_time
                }
            datas.append(fdata)

    return jsonify(datas)


@basic.route("/feed", methods=['GET'])
def feeds():
    sid = request.args.get("sid")
    rtime = int(request.args.get("date"))

    datas = []

    for p in Provider.query.filter_by(sid=sid):
        for a in Article.query.filter_by(uploader=p.prov_token):
            a_time = int(str(a.upload_date).split(".")[0])
            if a_time > rtime and len(a.dependency) == 0:
                a_rate = getRate(a.aid)
                a_user_rate = getUserRate(sid, a.aid)

                fdata = \
                    {
                        "aid": a.aid,
                        "type": a.type,
                        "uploader": a.uploader,
                        "content": a.content,
                        "image_url": a.image_url,
                        "dependency": a.dependency,
                        "upload_date": a_time,
                        "rate": a_rate,
                        "u_rate": a_user_rate
                    }
                datas.append(fdata)

    return jsonify(datas)


@basic.route("/feed/update", methods=['GET'])
def update():
    if request.args.get("key") == updateKey:
        year = request.args.get('year')
        month = request.args.get('month')
        day = request.args.get('day')

        result = update_raw(year, month, day, getRegProviders())
    else:
        result = False

    return jsonify({"result": result})


def update_raw(year, month, day, targets):
    from core.Core import NeisEngine

    result = False

    if year is None or month is None or day is None:
        result = False
    else:
        dateStr = "{0}-{1}-{2}".format(year, month, day)

        result = True
        for token in targets:
            pi = ProviderInfo.query.filter(ProviderInfo.token == token).first()
            if pi is not None:
                if str(pi.type) == "0":
                    school = [s for s in NeisEngine.SearchFromToken(token)]

                    if len(school) > 0:
                        data = json.loads(NeisEngine.GetJsonMeals(school[0], year, month))

                        for meal in data:
                            if meal['date'] == dateStr:
                                writeMeal(pi, token, meal, year, month, day)
                else:
                    processRes(token)
    return result

@basic.route("/feed/write", methods=['POST'])
def write():
    type = request.json["type"]
    uploader = request.json["uploader"]
    content = request.json["content"]
    image_url = request.json["image_url"]
    dependency = request.json["dependency"]

    result = write_raw(type, uploader, content, image_url, dependency, datetimeEx().now())

    if result:
        if len(dependency) > 0:
            prov = getProviderFromAid(dependency)
            gcms = getGcmRelation(prov, uploader)

            school = ProviderInfo.query.filter_by(token=prov).first()

            if school is not None:
                gcmController.push(gcms, "EverMeal", "'" + school.name + "' " + msg_com,
                                   GcmType.Review,
                                   school.name,
                                   {"aid": dependency})

    return jsonify({"result": result})


@basic.route("/feed/rate", methods=['POST'])
def wRate():
    result = False
    aid = ""

    try:
        aid = request.json["aid"]
        sid = request.json["sid"]
        rate = int(request.json["rate"])

        if Rate.query.filter_by(sid=sid, aid=aid).count() == 0:
            if rate >= 0 and rate <= 5:
                db.session.add(Rate(aid, sid, rate))
                db.session.commit()

                result = True
    except:
        pass

    if not result:
        return jsonify({"result": result})
    else:
        return jsonify(
            {
                "result": result,
                "aid": aid,
                "rate": str(getRate(aid))
            })


def getUserRate(sid, aid):
    r = Rate.query.filter_by(sid=sid, aid=aid).first()

    if r is not None:
        return r.rate

    return 0


def getRate(aid):
    result = 0

    rates = [int(r.rate) for r in Rate.query.filter_by(aid=aid).all()]
    if len(rates) > 0:
        result = sum(rates) / float(len(rates))

    return result


def writeMeal(pi, token, meal, year, month, day):
    content = json.dumps(meal)

    t = datetimeEx.localize(datetime(int(year), int(month), int(day)))

    if write_raw(pi.type, token, content, '', '', datetimeEx.totimestamp(t)):
        processNeis(token, msg_day_new.format(month, day))


def write_raw(type, uploader, content, image_url, dependency, date):
    aid = str(datetimeEx.now()).split(".")[0] + str(DBManager.db.session.query(func.max(Article.id).label("max_id")).one().max_id + 1)

    a = Article(aid, type, uploader, content, image_url, dependency, date)
    db.session.add(a)
    db.session.commit()

    if len(dependency) == 0:
        processNeis(uploader, msg_new)
    else:
        processNeis(dependency, msg_com)

    return True


def getProviderFromAid(aid):
    a = Article.query.filter_by(aid=aid).first()
    if a is not None:
        return a.uploader
    else:
        return None

"""
def getGcmCmtRelation(uploader, dependency):
    gcms = []

    #for a in Article.query.filter_by(dependency=dependency).all():
    for a in Provider.query.filter_by
        if a.uploader != uploader:
            gcm = Gcm.query.filter_by(sid=a.uploader).first()
            if gcm is not None:
                gcms.append(gcm.token)

    return list(set(gcms))
"""

def getGcmRelation(token, ignore_sid):
    gcms = []

    for p in Provider.query.filter(Provider.prov_token == token).all():
        if p.sid != ignore_sid:
            gcm = Gcm.query.filter_by(sid=p.sid).first()
            if gcm is not None:
                gcms.append(gcm.token)

    return gcms


def processNeis(token, message):
    school = Neis.query.filter(Neis.token == token).first()
    gcms = getGcmRelation(token, None)

    if school is not None:
        gcmController.push(gcms, "EverMeal", "'" + school.name + "' " + message, GcmType.Feed, school.name, None)


def processRes(token):
    pass


def getRegProviders():
    query = db.session.query(Provider.prov_token.distinct().label("prov_token"))

    return [row.prov_token for row in query.all()]
