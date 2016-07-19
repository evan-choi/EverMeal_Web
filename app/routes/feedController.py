from app.blueprint import basic
from flask import request, jsonify

# 깃에올리면 우짜노 다보이넹
from app.database import DBManager
from app.model.neis import ProviderInfo, Neis
from app.model.user import Provider, Gcm
from app.routes import gcmController

updateKey = "6041cef9600a531f527a69186b66bd21"
db = DBManager.db

@basic.route("/feed/update")
def update():
    result = False

    if request.args.get("key") == updateKey:
        result = True

        for token in getRegProviders():
            pi = ProviderInfo.query.filter(ProviderInfo.token == token).first()

            if pi.type == 0:
                processNeis(token)
            else:
                processRes(token)

    return jsonify({"result": result})


def processNeis(token):
    school = Neis.query.filter(Neis.token == token).first()
    gcms = []

    for p in Provider.query.filter(Provider.prov_token == token).all():
        gcm = Gcm.query.filter(Gcm.sid == p.sid).first()
        if gcm is not None:
            gcms.append(gcm.token)

    print(school.name + " : " + str(gcms))
    gcmController.push(gcms, "EverMeal", "'" + school.name + "' 오늘의 메뉴가 올라왔습니다.")

def processRes(token):
    pass

def getRegProviders():
    query = db.session.query(Provider.prov_token.distinct().label("prov_token"))

    return [row.prov_token for row in query.all()]
