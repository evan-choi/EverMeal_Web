#!/usr/bin/python
# -*- coding: utf-8 -*-
from app.database import DBManager
db = DBManager.db


class MealCache(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.Text)
    json = db.Column(db.Text)
    update_date = db.Column(db.Text)

    def __init__(self, code, json, update_date):
        self.code = code
        self.json = json
        self.update_date = update_date

    def __repr__(self):
        return "<MealCache %r>" % self.code


class Neis(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    zip_address = db.Column(db.Text)
    code = db.Column(db.Text)
    education_office = db.Column(db.Text)
    education_code = db.Column(db.Text)
    kind_sc_code = db.Column(db.Text)
    crse_sc_Code = db.Column(db.Text)
    token = db.Column(db.Text)

    def __init__(self, name, zip_address, code, education_office, kind_sc_code, crse_sc_Code, token):
        self.name = name
        self.zip_address = zip_address
        self.code = code
        self.education_office = education_office
        self.kind_sc_code = kind_sc_code
        self.crse_sc_Code = crse_sc_Code
        self.token = token

    def __repr__(self):
        return "<Neis %r>" % self.name


class ProviderInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    token = db.Column(db.Text)
    type = db.Column(db.Integer)

    def __init__(self, name, token, type):
        self.name = name
        self.token = token
        self.type = type

    def __repr__(self):
        return "<ProviderInfo %r>" % self.name

