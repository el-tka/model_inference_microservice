"""Health and readiness endpoints."""

from flask import Blueprint, jsonify

from services import model_inference_service


bp = Blueprint("health", __name__)


@bp.get("/health")
def health():
    return jsonify({
        "status": "ok"
    }), 200


@bp.get("/ready")
def ready():
    if model_inference_service.model is None:
        return jsonify({
            "status": "not_ready"
        }), 503

    return jsonify({
        "status": "ready",
        "model": model_inference_service.model_name,
    }), 200