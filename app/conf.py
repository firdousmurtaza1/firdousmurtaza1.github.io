import os
from pathlib import Path
from accounts.blueprint import account_blueprint
from .views import home as home_blueprint

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# BASE_DIR = Path(__file__).resolve().parent.parent
# BASE_DIR=os.path.dirname(os.path.abspath(__file__))
LOG_FILES_DIRECTORY = os.path.join(BASE_DIR, r'logs')

class BaseConfig(object):
    DEBUG = False
    VERSION = '1.1.1'
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    BASE_DIR = BASE_DIR
    SECRET_KEY = os.environ.get(r'FLASK_ENV_SECRET_KEY')
    SESSION_COOKIE_NAME = os.environ.get(r'FLASK_SESSION_COOKIE_NAME')
    SQLALCHEMY_DATABASE_URI = os.environ.get(r'FLASK_DATABASE_CONNECTION')
    FILES_STORAGE =  os.path.join(BASE_DIR,os.environ.get(r'FLASK_FILES_STORAGE'))
  

class Development(BaseConfig):
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    

class Production(BaseConfig):
    DEBUG = False


app_conf = {
    r'development': Development,
    r'production': Production
}

blueprints = {
    account_blueprint,
    home_blueprint
   
}