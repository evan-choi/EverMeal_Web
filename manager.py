#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask.ext.script import Manager
# from flask.ext.migrate import MigrateCommand
from app import create_app
from app.database import DBManager
#
# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")

app = create_app()
manager = Manager(app)
# manager.add_command('db', MigrateCommand)

# 실행방법
# python manage.py init_db
@manager.command
def init_db():
    DBManager.init_db()

# 실행방법
# python manage.py clear_db
@manager.command
def clear_db():
    DBManager.clear_db()

if __name__ == '__main__':
    manager.run()
