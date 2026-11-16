import sys
from pathlib import Path

import pytest


ROOT_DIR = Path(__file__).resolve().parents[1]
APP_DIR = ROOT_DIR / "app"

sys.path.insert(0, str(APP_DIR))


class FakeModel:
    def predict(self, dataframe):
        return [125000.0]


@pytest.fixture
def client(monkeypatch):
    from services import model_inference_service

    monkeypatch.setattr(
        model_inference_service,
        "model",
        FakeModel(),
    )

    monkeypatch.setattr(
        model_inference_service,
        "features",
        [
            "area",
            "constraction_year",
            "bedrooms",
            "garden",
            "balcony_yes",
            "parking_yes",
            "furnished_yes",
            "garage_yes",
            "storage_yes",
        ],
    )

    monkeypatch.setattr(
        model_inference_service,
        "model_name",
        "test_model",
    )

    from run import create_app

    app = create_app(load_model=False)
    app.config["TESTING"] = True

    return app.test_client()


@pytest.fixture
def apartment_data():
    return {
        "area": 75,
        "constraction_year": 2015,
        "bedrooms": 2,
        "garden": 0,
        "balcony_yes": 1,
        "parking_yes": 1,
        "furnished_yes": 1,
        "garage_yes": 0,
        "storage_yes": 1,
    }