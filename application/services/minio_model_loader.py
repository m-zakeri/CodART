import joblib
import understand as und
from minio import Minio
from io import BytesIO
from codart.learner.sbr_initializer.utils.utility import logger


class MinioModelLoader:
    def __init__(
        self,
        minio_endpoint: str,
        minio_access_key: str,
        minio_secret_key: str,
        bucket_name: str = "ml-models",
        dataset_number: int = 1,
    ):
        """Initialize MinIO client for model loading"""
        self.minio_client = Minio(
            endpoint=minio_endpoint,
            access_key=minio_access_key,
            secret_key=minio_secret_key,
            secure=False,
        )
        self.bucket_name = bucket_name
        self.ds_number = dataset_number
        try:
            if not self.minio_client.bucket_exists(self.bucket_name):
                self.minio_client.make_bucket(self.bucket_name)
                print(f"Created bucket: {self.bucket_name}")
        except Exception as e:
            print(f"Could not verify bucket existence: {e}")

    def load_model(self, model_type: str):
        """Load a model from MinIO with fallback to dummy models"""
        from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
        from sklearn.neural_network import MLPRegressor
        from sklearn.preprocessing import StandardScaler
        import numpy as np

        model_path = f"models/DS{self.ds_number}/{model_type}_DS{self.ds_number}.joblib"
        try:
            # Check if the object exists first
            try:
                self.minio_client.stat_object(
                    bucket_name=self.bucket_name, object_name=model_path
                )
                # Object exists, proceed with loading
                model_data = self.minio_client.get_object(
                    bucket_name=self.bucket_name, object_name=model_path
                )
                model = joblib.load(BytesIO(model_data.data))
                model_data.close()
                logger.info(f"Successfully loaded model {model_path} from MinIO")
                return model
            except Exception as e:
                if "NoSuchKey" in str(e) or "Not found" in str(e):
                    # Model doesn't exist, create a dummy model
                    logger.warning(
                        f"Model {model_path} not found in MinIO, creating dummy model"
                    )
                    return self._create_dummy_model(model_type)
                else:
                    raise
        except Exception as e:
            logger.error(f"Error loading model {model_path}: {str(e)}")
            logger.info("Falling back to dummy model")
            return self._create_dummy_model(model_type)

    def _create_dummy_model(self, model_type):
        """Create a dummy model when the real one isn't available"""
        from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
        from sklearn.neural_network import MLPRegressor
        from sklearn.preprocessing import StandardScaler
        import numpy as np

        logger.info(f"Creating dummy {model_type} model")
        # Create and train a minimal model
        X_dummy = np.array([[0, 0, 0, 0], [1, 1, 1, 1]])
        y_dummy = np.array([0, 1])

        if model_type == "RFR1":
            # This is the scaler
            model = StandardScaler()
            model.fit(X_dummy)
        elif model_type == "HGBR1":
            model = GradientBoostingRegressor(n_estimators=10)
            model.fit(X_dummy, y_dummy)
        elif model_type == "MLPR1":
            model = MLPRegressor(hidden_layer_sizes=(10,), max_iter=100)
            model.fit(X_dummy, y_dummy)
        elif model_type == "VR1":
            model = RandomForestRegressor(n_estimators=10)
            model.fit(X_dummy, y_dummy)
        else:
            # Default fallback
            model = GradientBoostingRegressor(n_estimators=10)
            model.fit(X_dummy, y_dummy)

        # Optionally, save the dummy model to MinIO for future use
        self._save_dummy_model(model, model_type)

        return model

    def _save_dummy_model(self, model, model_type):
        """Save a dummy model to MinIO for future use"""
        try:
            model_path = (
                f"models/DS{self.ds_number}/{model_type}_DS{self.ds_number}.joblib"
            )

            # Create the directory structure if it doesn't exist
            dir_path = f"models/DS{self.ds_number}"

            # Serialize the model
            buffer = BytesIO()
            joblib.dump(model, buffer)
            buffer.seek(0)

            # Upload to MinIO
            self.minio_client.put_object(
                bucket_name=self.bucket_name,
                object_name=model_path,
                data=buffer,
                length=buffer.getbuffer().nbytes,
                content_type="application/octet-stream",
            )
            logger.info(f"Saved dummy model to {model_path}")
        except Exception as e:
            logger.warning(f"Could not save dummy model to MinIO: {e}")
