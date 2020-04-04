import os


DIRECTORY_PATH = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    sql_default_url = 'sqlite:///' + os.path.join(DIRECTORY_PATH, 'app.db')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or sql_default_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
