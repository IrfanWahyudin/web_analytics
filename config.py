import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123@localhost/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False