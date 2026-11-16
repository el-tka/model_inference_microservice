"""
Flask application entry point.

This module serves as an entry point for the Flask application.

Usage:
    The Flask application is created and initialized here.
    The prediction blueprint ('api.prediction.bp) is registered
    with the application.
"""

from flask import Flask
from loguru import logger

from api.health import bp as health_bp
from api.prediction import bp as prediction_bp
from services import initialize_model


def create_app(load_model=True):
    app = Flask(__name__)

    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024

    from flask_cors import CORS

    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": ["http://localhost:3000"]
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
