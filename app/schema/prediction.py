"""Prediction response schema."""

from pydantic import BaseModel


class PredictionResponse(BaseModel):
    prediction: float
    model_name: str
    model_version: str
