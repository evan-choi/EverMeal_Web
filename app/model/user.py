#!/usr/bin/python
# -*- coding: utf-8 -*-
from app.database import DBManager
db = DBManager.db


class Provider(db.Model):
    id = db.Column(db.String(100), db.ForeignKey('user.id'), primary_key=True)
    prov_token = db.Column(db.String(120))

    user = db.relationship('User', backref=db.backref('providers', lazy='dynamic'))

    def __init__(self, prov_token, user):
        self.id = user.id
        self.prov_token = prov_token
        self.user = user

    def __repr__(self):
        return "<Provider %r>" % self.prov_token


class Allergy(db.Model):
    id = db.Column(db.String(100), db.ForeignKey('user.id'), primary_key=True)
    allergy = db.Column(db.Integer)

    user = db.relationship('User', backref=db.backref('allergies', lazy='dynamic'))

    def __init__(self, allergy, user):
        self.id = user.id
        self.allergy = allergy
        self.user = user

    def __repr__(self):
        return '<Allergy %r>' % self.allergy


class User(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(120))
    reg_date = db.Column(db.String(100))

    def __init__(self, sid, username, email, password):
        self.id = sid
        self.email = email
        self.password = password
        self.username = username

    def __repr__(self):
        return '<User %r>' % self.username