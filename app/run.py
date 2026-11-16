"""
Flask application entry point.

This module serves as an entry point for the Flask application.

Usage:
    The Flask application is created and initialized here.
    The prediction blueprint ('api.prediction.bp) is registered
    with the application.
"""

from flask import Flask
from flask_cors import CORS
from loguru import logger

from api.health import bp as health_bp
from api.prediction import bp as prediction_bp
from services import initialize_model


def create_app(load_model=True):
    app = Flask(__name__)

    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024

    CORS(
        app,
        resources={
            r"/*": {
                "origins": [
                    "http://localhost:3000",
                    "http://127.0.0.1:3000",
                ],
                "methods": ["GET", "POST", "OPTIONS"],
                "allow_headers": ["Content-Type"],
            }
        },
    )

    app.register_blueprint(health_bp)
    app.register_blueprint(prediction_bp)

    if load_model:
        initialize_model()

    return app


app = create_app()

if __name__ == "__main__":
    logger.info("Starting ML inference API")
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False,
    )
