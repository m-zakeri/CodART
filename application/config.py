from pydantic import BaseSettings

class Settings:
    MODEL_VERSIONS = {
        "DS8": {
            "model_path": "sklearn_models8/VR1_DS8.joblib",
            "scaler_path": "data_model/DS_ALL_METRICS_JFLEX.joblib"
        },
        "DS9": {
            "model_path": "sklearn_models9/VR1_DS9.joblib",
            "scaler_path": "data_model/DS_EVO_METRICS_JFLEX.joblib"
        }
    }

settings = Settings()