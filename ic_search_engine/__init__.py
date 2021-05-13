from flask import Flask
from .main.routes import main
from .extensions import mongo
from dotenv import load_dotenv

def create_app(config_object='ic_search_engine.settings'):
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(config_object)
    mongo.init_app(app)
    app.register_blueprint(main)
    return app
