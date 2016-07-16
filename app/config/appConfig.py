#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
class AppConfig(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)) + "/../", 'task.db')
