"""Model inference service initialization."""

from .model_inference import ModelInferenceService


model_inference_service = ModelInferenceService()


def initialize_model():
    """Load ML model during application startup."""
    model_inference_service.load_model()