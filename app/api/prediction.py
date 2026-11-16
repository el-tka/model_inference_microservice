"""
Prediction API module.

This module contains endpoints to trigger a machine learning model
for predicting apartment price.

Endpoints:
    - GET /pred/:
        Returns a prediction for apartment price based on the query
        parameters provided in the request. Query parameters should
        match the schema defined in the Apartment class.
        Returns HTTP status 400 if input parameters are invalid.

    - POST /pred/:
        Returns a prediction for apartment price based on the JSON
        data provided in the request body. The request body should
        contain JSON data that matches the schema defined in the
        Apartment class.
        Returns HTTP status 400 if input parameters are invalid.
"""

from flask import abort, Blueprint, jsonify, request
from pydantic import ValidationError

from schema.apartment import Apartment
from services.model_inference import ModelInferenceService
from services import model_inference_service


bp = Blueprint('prediction', __name__, url_prefix='/pred')


@bp.get('/')
def get_prediction():
    """
    Return a prediction based on the query parameters.

    Returns:
        dict: A dictionary containing the prediction result.
    """
    try:
        apartment_features = Apartment(**request.args)
    except ValidationError:
        abort(code=400, description='Bad input parameters')  # noqa: WPS432

    prediction = model_inference_service.predict(
        apartment_features.model_dump()
    )

    return {'Model prediction': prediction.tolist()}


@bp.post("/")
def get_prediction_post():
    """
        Return a prediction based on the JSON data.
    
        Returns:
            json: A json containing the prediction result.
        """
    payload = request.get_json(silent=True)

    if payload is None or payload == {}:
        return jsonify({
            "error": "Request body is empty"
        }), 400

    if not isinstance(payload, dict):
        return jsonify({
            "error": "JSON body must be an object"
        }), 400

    try:
        apartment = Apartment.model_validate(payload)

    except ValidationError as exc:
        return jsonify({
            "error": "Validation error",
            "details": exc.errors(
                include_context=False,
                include_input=False,
            ),
        }), 422

    service = ModelInferenceService()
    service.load_model()

    prediction = service.predict(
        apartment.model_dump()
    )

    return jsonify({
        "prediction": prediction.tolist()
    }), 200

