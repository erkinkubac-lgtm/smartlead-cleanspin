from flask import Flask
from flask_cors import CORS
from config import config
from app.routes import api, sayfalar
from app.database import init_db

def create_app(ortam="development"):
    app = Flask(__name__)
    app.config.from_object(config[ortam])  

    CORS(app, origins=app.config["CORS_ORIGINS"])

    with app.app_context():
        init_db(app)

    app.register_blueprint(api)
    app.register_blueprint(sayfalar)

    @app.route("/health")
    def health():
            return {"durum": "ayakta"}, 200

    return app
