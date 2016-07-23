# coding: utf-8

from flask import render_template, session, request, redirect
from app.blueprint import basic
from app.model.neis import ProviderInfo
from app.model.user import Gcm

list = ['User', 'Feed', 'Provider', 'Push']


@basic.route('/<name>')
def main(name):
    return render_template(name)


@basic.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'GET':
        return admin_get(None)
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

        pi = ProviderInfo.query.all()

        return render_template("index.html",
                               list=list,
                               selected=session['selected'],
                               pi=pi)
    else:
        return render_template("login.html")
