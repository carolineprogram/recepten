import os
from flask_wtf import CSRFProtect

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '23FE02DD934'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'recepten.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

csrf = CSRFProtect()
