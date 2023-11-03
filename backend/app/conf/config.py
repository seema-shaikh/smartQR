import os
from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

from app.utility.config import DevelopmentConfig, ProductionConfig, StagingConfig

load_dotenv()


def create_app():
    app = Flask(__name__)
    if os.environ.get('FLASK_ENV')== 'staging':
        app.config.from_object(StagingConfig)
    elif os.environ.get('FLASK_ENV')== 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)
    return app

app = create_app() 
jwt_manager = JWTManager(app)