"""
Flask application entry point.

This module serves as an entry point for the Flask application.

Usage:
    The Flask application is created and initialized here.
    The prediction blueprint ('api.prediction.bp) is registered
    with the application.
"""

from flask import Flask
from loguru  import logger

from api.prediction import bp

app = Flask(__name__)
app.register_blueprint(bp)

logger.info("Flask application initialized")

if __name__ == '__main__':
    logger.info("Starting inference microservice")

    app.run(debug=True, use_reloader=False,)
