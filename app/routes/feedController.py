from datetime import datetime

from app.blueprint import basic
from flask import request, jsonify

from app.database import DBManager
from app.model.article import Article
from app.model.neis import ProviderInfo, Neis
from app.model.user import Provider, Gcm
from app.routes import gcmController

updateKey = "6041cef9600a531f527a69186b66bd21"
db = DBManager.db

msg_new = "%ec%98%a4%eb%8a%98%ec%9d%98+%eb%a9%94%eb%89%b4%ea%b0%80+%ec%98%ac%eb%9d%bc%ec%99%94%ec%8a%b5%eb%8b%88%eb%8b%a4!"
msg_com = "%ec%97%90+%eb%a6%ac%eb%b7%b0%ea%b0%80+%ec%9e%91%ec%84%b1%eb%90%ac%ec%8a%b5%eb%8b%88%eb%8b%a4!"

@basic.route("/feed/update", methods=['GET'])
def update():
    result = False

    if request.args.get("key") == updateKey:
        result = True

        for token in getRegProviders():
            pi = ProviderInfo.query.filter(ProviderInfo.token == token).first()

            if pi.type == 0:
                processNeis(token, msg_new)
            else:
                processRes(token)

    return jsonify({"result": result})


@basic.route("/feed/write", methods=['POST'])
def write():
    type = request.json["type"]
    uploader = request.json["uploader"]
    content = request.json["content"]
    image_url = request.json["image_url"]
    dependency = request.json["dependency"]
    upload_date = datetime.today()
    aid = str(Article.query.count()) + "_" + uploader

    a = Article(aid, type, uploader, content, image_url, dependency, upload_date)
    db.session.add(a)
    db.session.commit()

    if dependency is None:
        processNeis(uploader, msg_new)
    else:
        processNeis(dependency, msg_com)

    return jsonify({"result": True})


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

    gcmController.push(gcms, "EverMeal", "'" + school.name + "' " + message)

def processRes(token):
    pass

def getRegProviders():
    query = db.session.query(Provider.prov_token.distinct().label("prov_token"))

    return [row.prov_token for row in query.all()]
