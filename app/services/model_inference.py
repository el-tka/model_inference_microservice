"""
This module provides functionality for managing the ML model,
including loading the model and making predictions.

It contains the ModelInferenceService class, which handles loading and
using the pre-trained model. The class offers methods
to load the model from a file, checking if it does exist,
and making predictions using the loaded model.
"""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from loguru import logger

from config import model_settings


class ModelInferenceService:
    """
    A service class for managing the ML model, including loading and
    making predictions.

    This class provides functionality to load a pre-trained model from a
    specified path, check if it exists, and make predictions
    using the loaded model.

    Attributes:
        model (object): The loaded ML model. Initially set to None until the
            model is loaded.
        model_path (Path): The path to the model file.
        features (list): The list of feature names used for predictions.
        model_name (str): The name of the loaded model.

    Methods:
        __init__(self, model_path): Initializes the ModelService instance with
            the specified model path.
        load_model(self): Loads the model from the specified path, building it
            if it doesn't exist.
        predict(self, input_variables): Makes predictions using the loaded
            model based on the provided input variables.
    """

    def __init__(self, model_path: str | Path | None = None) -> None:
        """
        Initializes the ModelInferenceService instance.
        """
        self.model = None
        self.features = None
        self.model_name = None

        # Absolute path to the app directory
        base_dir = Path(__file__).resolve().parent.parent

        if model_path is None:
            model_path = (
                Path(model_settings.model_output_path)
                / model_settings.model_name
            )

        model_path = Path(model_path)

        if not model_path.is_absolute():
            model_path = base_dir / model_path

        self.model_path = model_path.resolve()

    def load_model(self) -> None:
        """Loads the model and metadata, checks if the model exists.
       
           Raises:
                FileNotFoundError: if the model file doesn't exist at the 
                                   specified directory"""
        logger.info(
            f'Checking if model exists at {self.model_path}',
            )
                    
        # 1. Check if model exists
        if not self.model_path.exists():
            logger.error(
                f'Model not found at {self.model_path}.'
                )
            raise FileNotFoundError('Model file does not exist!')

        # 2. Load artifact
        with open(self.model_path, 'rb') as model_file:
            logger.info(
                f'Loading model from {self.model_path}',
                )
            artifact = joblib.load(model_file)

        # 3. Extract trained model
        self.model = artifact['model']
        self.features = artifact['features']
        self.model_name = artifact['model_name']

        logger.info(
            f'Model loaded: {self.model_name}',
            )

    def predict(self, input_variables: dict) -> np.ndarray:
        """
        Makes predictions using the loaded model based on the provided
        input variables.
        
        Takes a list of input variables, converts them into a DataFrame, and
        uses the loaded model to make predictions.
        Returns the predictions as a NumPy array.

        Args:
        input_variables (dict): A dictionary of input variables for making
        predictions.

        Returns:
        numpy.ndarray: An array of predictions made by the model.
        """

        if self.model is None:
            logger.error("Model is not loaded")
            raise RuntimeError("Model is not loaded")

        if not self.features:
            raise RuntimeError("Model features are not loaded")

        missing = set(self.features) - set(input_variables)

        if missing:
            raise ValueError(
                f"Missing model features: {sorted(missing)}"
            )

        x = pd.DataFrame([input_variables])
        x = x.loc[:, self.features]

        logger.info(
            "Making prediction using model: {}",
            self.model_name,
        )

        return self.model.predict(x)
