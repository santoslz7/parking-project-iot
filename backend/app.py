from flask import Flask, jsonify
from flask_cors import CORS

from config import Config
from routes.parking_lots import bp as parking_lots_bp


def create_app():
    app = Flask(__name__)
    CORS(app, origins=Config.CORS_ORIGINS)

    app.register_blueprint(parking_lots_bp)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=(Config.FLASK_ENV == "development"), port=5000)
