import os
import joblib
from app.core.logging import logger


def load_joblib_model(model_path: str):
    if not os.path.exists(model_path):
        logger.info(f"No trained model found at {model_path}. Using fallback rules.")
        return None

    try:
        return joblib.load(model_path)
    except Exception as error:
        logger.error(f"Failed to load model at {model_path}: {error}")
        return None
