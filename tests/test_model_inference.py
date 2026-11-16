from services.model_inference import ModelInferenceService


class CaptureModel:
    def predict(self, dataframe):
        self.columns = dataframe.columns.tolist()
        self.values = dataframe.iloc[0].tolist()
        return [100.0]


def test_feature_order():
    service = ModelInferenceService()

    model = CaptureModel()

    service.model = model
    service.model_name = "test"
    service.features = ["area", "bedrooms"]

    result = service.predict({
        "bedrooms": 2,
        "area": 75,
    })

    assert result[0] == 100.0
    assert model.columns == ["area", "bedrooms"]
    assert model.values == [75, 2]
