# coding: utf-8
import hashlib
from collections import defaultdict

from sqlalchemy import text
from flask import render_template, session, request, redirect
from app.blueprint import basic
from app.database import DBManager
from app.model.admin import Admin
from app.model.article import Article, Rate
from app.model.neis import ProviderInfo, Neis
from app.model.user import Gcm, Provider, Push
from app.routes.feedController import getRate
from core.Core import EducationOffice
from utils.dateUtils import datetimeEx

db = DBManager.db
list = ['user', 'feed', 'provider', 'push']
titles = \
    {
        list[0]: u'유저 관리',
        list[1]: u'피드 관리',
        list[2]: u'업체 통계',
        list[3]: u'푸시 알림'
    }


@basic.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'GET':
        return admin_get(request.args.get('menu') or "provider")
    else:
        return admin_post()


def admin_post():
    id = request.form['id']
    pwd = hashlib.sha224(request.form['pass'] or "").hexdigest()

    if Admin.query.filter_by(username=id, password=pwd).count() == 1:
        session['selected'] = 'provider'
        session['username'] = id

        return admin_get(session['selected'])
    else:
        return redirect('/admin')


@basic.route('/admin/logout')
def admin_logout():
    if 'username' in session:
        session.clear()

    return redirect('/admin')


@basic.route('/admin/<menu>/command', methods=['GET'])
def admin_command(menu):
    action = request.args.get('action')
    arg = request.args.get('arg')

    if menu == 'user':
        if action == u'삭제':
            prov = request.args.get('prov')
            Provider.query.filter_by(sid=arg, prov_token=prov).delete()
            db.session.commit()
        return redirect('/admin/user?mode=1&arg=' + arg)

    elif menu == 'push':
        if action == u'삭제':
            Push.query.filter_by(id=arg).delete()
            db.session.commit()
        return redirect('/admin?menu=push')

    elif menu == 'feed':
        if action == u'삭제':
            isparent = request.args.get("isparent")

            if isparent is None:
                Article.query.filter_by(aid=arg).delete()
                db.session.commit()
                arg = request.args.get('dependency')
            else:
                Article.query.filter_by(dependency=arg).delete()
                Article.query.filter_by(aid=arg).delete()
                Rate.query.filter_by(aid=arg).delete()
                db.session.commit()
                return redirect('/admin?menu=feed')

        return redirect('/admin/feed?mode=1&arg=' + arg)

    return 'Command ' + menu


@basic.route('/admin/<menu>', methods=['GET'])
def admin_inline(menu):
    if 'username' in session:
        title = None
        showAddButton = False
        headers = [u"번호", u"아이디"]
        btns = [u'수정', u'삭제']
        btnDatas = []
        items = []

        try:
            try:
                mode = int(request.args.get("mode"))
            except:
                pass

            if menu == 'user':
                if mode == 1:
                    sid = request.args.get("arg")

                    title = sid + u" 업체 관리"
                    headers = [u'추가한 업체']
                    btns = [u'삭제']

                    for s in Provider.query.filter_by(sid=sid):
                        items.append(
                            [
                                [None, getSchool(s.prov_token).name]
                            ]
                        )
                        btnDatas.append(
                            [
                                [True, u'정말로 삭제하시겠습니까?', s.sid + '&prov=' + s.prov_token]
                            ]
                        )

            elif menu == 'feed':
                if mode == 1:
                    aid = request.args.get("arg")
                    article = Article.query.filter_by(aid=aid).first()
                    school = getSchool(article.uploader)

                    title = school.name + u' 피드 관리'
                    headers = [u'아이디', u'내용', u'시간']
                    btns = [u'삭제']

                    for a in Article.query.filter_by(dependency=aid):
                        items.append(
                            [
                                [None, a.uploader],
                                [None, a.content],
                                [None, datetimeEx.toDatetime(int(a.upload_date)).strftime('%Y-%m-%d %H:%M:%S')]
                            ]
                        )
                        btnDatas.append(
                            [
                                [True, u'정말로 삭제하시겠습니까?', a.aid + '&dependency=' + aid]
                            ]
                        )

            elif menu == 'provider':
                pass
            elif menu == 'push':
                pass
            else:
                return 403

            if title is None:
                title = titles[menu]

            return render_template("index.html",
                                   list=list,
                                   selected=menu,
                                   title=title,
                                   headers=headers,
                                   items=items,
                                   btns=btns,
                                   btnDatas=btnDatas,
                                   showAddButton=showAddButton)
        except:
            return redirect('/admin?menu=' + menu)
    else:
        return render_template('login.html')

def admin_get(sel):
    """
    < Char Template >

    < List Template >
    headers 배열과 items 배열의 크기가 일치해야함

    headers = [header1, header2, ...]
    items.append(
        [
            [a tag 파라미터, 내용],  // td 첫번째
            [a tag 파라미터, 내용],  // td 두번째
                       .
                       .
                       .
        ]
    )

    < Button Template >p일치해야함

    btns = [name1, name2, ...]
    btnDatas.append(
        [
            [alert 여부, alert 확인 메세지, 파라미터],  // 첫번째 버튼
            [alert 여부, alert 확인 메세지, 파라미터],  // 두번째 버튼
                                   .
                                   .
                                   .
        ]
    )
    """

    if 'username' in session:
        if sel is None:
            sel = 'User'
        else:
            session['selected'] = sel

        showChart = False
        chartData = []
        showAddButton = False
        headers = [u"번호", u"아이디"]
        btns = [u'수정', u'삭제']
        btnDatas = []
        items = []

        if not 'selected' in session:
            session['selected'] = sel

        if sel == 'user':
            headers.append(u"업체")
            btns = [u'수정']
            i = 0
            for p in db.session.query(Provider).distinct(Provider.sid).group_by(Provider.sid):
                i += 1
                items.append(
                    [
                        [None, i],
                        [p.sid, p.sid],
                        [None, ",   ".join(
                            [getSchool(pv.prov_token).name for pv in Provider.query.filter_by(sid=p.sid).all()])]
                    ]
                )
                btnDatas.append(
                    [
                        [False, None, p.sid]
                    ]
                )

        elif sel == 'feed':
            headers = [u'번호', u'업체', u'별점', u'리뷰', u'날짜']

            for a in Article.query.filter().all():
                if len(a.dependency) == 0:
                    items.append(
                        [
                            [None, a.id],
                            [a.aid, getSchool(a.uploader).name],
                            [None, getRate(a.aid)],
                            [None, Article.query.filter_by(dependency=a.aid).count()],
                            [None, datetimeEx.toDatetime(int(a.upload_date)).strftime('%Y-%m-%d')]
                        ]
                    )
                    btnDatas.append(
                        [
                            [False, None, a.aid],
                            [True, u'모든 리뷰 및 해당 피드가 삭제됩니다.', a.aid + '&isparent=1']
                        ]
                    )

        elif sel == 'provider':
            showChart = True
            btns = []
            headers = [u'번호', u'업체', u'게시글 수', u'사용자 수']
            query = db.session.query(Provider.prov_token.distinct().label("prov_token"))
            chartData = [[], []]

            i = 1
            for p in query.all():
                a_count = Article.query.filter_by(uploader=p.prov_token).count()
                p_count = Provider.query.filter_by(prov_token=p.prov_token).count()
                school = getSchool(p.prov_token)

                items.append(
                    [
                        [None, i],
                        [None, school.name],
                        [None, a_count],
                        [None, p_count]
                    ]
                )
                chartData[0].append(
                    [school.name, a_count]
                )
                i += 1

            sql = text('SELECT prov_token, COUNT(*) FROM provider GROUP BY prov_token HAVING COUNT(*) > 0')
            result = DBManager.db.engine.execute(sql)

            chart = defaultdict(lambda: 42)

            for row in result:
                n = Neis.query.filter_by(token=row[0]).one()
                city = EducationOffice.toString(n.education_office)
                p = chart.get(city, 0)
                chart[city] = p + int(row[1])

            for key, value in chart.iteritems():
                chartData[1].append(
                    [key, value]
                )

        elif sel == 'push':
            btns = [u'삭제']
            headers = [u'번호', u'발송', u'제목', u'내용', u'메세지 타입', u'날짜']

            for p in Push.query.all():
                items.append(
                    [
                        [None, p.id],
                        [None, p.sender],
                        [None, p.title],
                        [None, p.message],
                        [None, p.type],
                        [None, datetimeEx.toDatetime(int(p.date)).strftime('%Y-%m-%d %H:%M:%S')]
                    ]
                )
                btnDatas.append(
                    [
                        [True, u'정말로 삭제하시겠습니까?', p.id]
                    ]
                )

        else:
            return 403

        return render_template("index.html",
                               list=list,
                               selected=session['selected'],
                               title=titles[sel],
                               headers=headers,
                               items=items,
                               btns=btns,
                               btnDatas=btnDatas,
                               showAddButton=showAddButton,
                               showChart=showChart,
                               chartData=chartData)
    else:
        return render_template("login.html")

def getSchool(token):
    return Neis.query.filter_by(token=token).first()
