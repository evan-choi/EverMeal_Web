#!/usr/bin/python
# -*- coding: utf-8 -*-
from app.database import DBManager
db = DBManager.db


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    aid = db.Column(db.Text)
    type = db.Column(db.Integer)
    uploader = db.Column(db.Text)
    content = db.Column(db.Text)
    image_url = db.Column(db.Text)
    dependency = db.Column(db.Text)
    upload_date = db.Column(db.Text)

    def __init__(self, aid, type, uploader, content, image_url, dependency, update_date):
        self.aid = aid
        self.type = type
        self.uploader = uploader
        self.content = content
        self.image_url = image_url
        self.dependency = dependency
        self.upload_date = update_date

    def __repr__(self):
        return "<Article %r>" % self.aid


class Rate(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    aid = db.Column(db.Text)
    sid = db.Column(db.Text)
    rate = db.Column(db.Text)

    def __init__(self, aid, sid, rate):
        self.aid = aid
        self.sid = sid
        self.rate = rate

    def __repr__(self):
        return "<Rate %r>" % self.rate