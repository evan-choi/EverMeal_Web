#!/usr/bin/python
# -*- coding: utf-8 -*-
from app.database import DBManager
db = DBManager.db


class Provider(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sid = db.Column(db.String(100))
    prov_token = db.Column(db.String(120))

    def __init__(self, sid, prov_token):
        self.sid = sid
        self.prov_token = prov_token

    def __repr__(self):
        return "<Provider %r>" % self.prov_token


class Allergy(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sid = db.Column(db.String(100))
    allergy = db.Column(db.Integer)

    def __init__(self, sid, allergy):
        self.sid = sid
        self.allergy = allergy

    def __repr__(self):
        return '<Allergy %r>' % self.allergy


class User(db.Model):
    sid = db.Column(db.String(100), primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(120))
    reg_date = db.Column(db.String(100))

    def __init__(self, sid, username, email, password):
        self.sid = sid
        self.email = email
        self.password = password
        self.username = username

    def __repr__(self):
        return '<User %r>' % self.username