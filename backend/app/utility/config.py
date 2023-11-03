import json
import os
import platform

app_name = '/'.join(os.path.dirname(os.path.realpath(__file__)).split('\\' if platform.system() == 'Windows' else '/')[:-1])
with open(app_name + '/.secrets.json') as f:
    settings = json.load(f)
class Config:
    DEBUG = False

class DevelopmentConfig(Config):
    FLASK_ENV = settings.get("development").get("FLASK_ENV")
    SECRET_KEY =  settings.get("development").get("FLASK_SECRET_KEY")
    JWT_TOKEN_LOCATION =  ['headers']
    JWT_SECRET_KEY =  settings.get("development").get("FLASK_SECRET_KEY")
    DEBUG =  settings.get("development").get("FLASK_DEBUG") 
    DATABASE_URL =  settings.get("development").get("FLASK_DATABASE_URI")

class StagingConfig(Config):
    FLASK_ENV = settings.get("staging").get("FLASK_ENV")
    SECRET_KEY =  settings.get("staging").get("FLASK_SECRET_KEY")
    JWT_TOKEN_LOCATION =  ['headers']
    JWT_SECRET_KEY =  settings.get("staging").get("FLASK_SECRET_KEY")
    DEBUG =  settings.get("staging").get("FLASK_DEBUG") 
    DATABASE_URL =  settings.get("staging").get("FLASK_DATABASE_URI")

class ProductionConfig(Config):
    FLASK_ENV = settings.get("production").get("FLASK_ENV")
    SECRET_KEY =  settings.get("production").get("FLASK_SECRET_KEY")
    JWT_TOKEN_LOCATION =  ['headers']
    JWT_SECRET_KEY =  settings.get("production").get("FLASK_SECRET_KEY")
    DEBUG =  settings.get("production").get("FLASK_DEBUG") 
    DATABASE_URL =  settings.get("production").get("FLASK_DATABASE_URI")

config_by_name = dict(
    dev=DevelopmentConfig,
    test=StagingConfig,
    prod=ProductionConfig
)