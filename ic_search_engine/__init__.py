from flask import Flask
from .main.routes import main
from .extensions import mongo
from dotenv import load_dotenv
from flask_cors import CORS

def create_app(config_object='ic_search_engine.settings'):
    load_dotenv()
    app = Flask(__name__,static_folder='frontend\\build\\',static_url_path='')
    CORS(app)
    app.config.from_object(config_object)
    #app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    mongo.init_app(app)
    app.register_blueprint(main)
    return app
