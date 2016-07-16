# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy

class DBManager:
    db = None

    @staticmethod
    def init(app):
        db = SQLAlchemy(app)
        # migrate = Migrate(app, db)
        DBManager.db = db
        from app.model import user

    @staticmethod
    def init_db():
        db = DBManager.db
        db.create_all()

        #add init data
        DBManager.init_sample(db)

    @staticmethod
    def clear_db():
        DBManager.db.drop_all()

    @staticmethod
    def init_sample(db):
        from app.model.user import User
        admin = User('admin', 'admin@example.com')
        guest = User('guest', 'guest@example.com')
        db.session.add(admin)
        db.session.add(guest)
        db.session.commit()
