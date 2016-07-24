#!/usr/bin/python
# coding: utf-8

from app.database import DBManager
db = DBManager.db


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return "<Admin %r>" % self.username
