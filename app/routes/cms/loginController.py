# coding: utf-8

from flask import render_template, session, request, redirect
from app.blueprint import basic
from app.model.article import Article
from app.model.neis import ProviderInfo
from app.model.user import Gcm, Provider

list = ['User', 'Feed', 'Provider', 'Push']


@basic.route('/<name>')
def main(name):
    return render_template(name)


@basic.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'GET':
        return admin_get(request.args.get('menu'))
    else:
        return admin_post()


@basic.route('/admin/<name>')
def admin_name(name):
    if name in list:
        session['selected'] = name
        return redirect('/admin')
    else:
        return 403


def admin_post():
    id = request.form['id']
    pwd = request.form['pass']

    session['selected'] = 'User'
    session['username'] = id

    return id


def admin_get(sel):
    if sel is None:
        sel = 'User'
    else:
        session['selected'] = sel

    if 'username' in session:
        if not 'selected' in session:
            session['selected'] = sel

        if sel == 'User':
            items = Gcm.query.all()
        elif sel == 'Feed':
            items = Article.query.all()
        elif sel == 'Provider':
            items = Provider.query.all()
        elif sel == 'Push':
            items = Gcm.query.all()
        else:
            return 403

        return render_template("index.html",
                               list=list,
                               selected=session['selected'],
                               items=items)
    else:
        return render_template("login.html")
