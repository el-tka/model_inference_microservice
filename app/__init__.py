"""Flask application factory."""

from flask import Flask
from flask_cors import CORS


def create_app(load_model=True):
    app = Flask(__name__)

    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024

    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": ["http://localhost:3000"]
            }
        },
    )

    # Existing imports use app/ as the import root.
    from api.health import bp as health_bp
    from api.prediction import bp as prediction_bp
    

    app.register_blueprint(health_bp)
    app.register_blueprint(prediction_bp)
    

    if load_model:
        from services import initialize_model
        initialize_model()

    return app