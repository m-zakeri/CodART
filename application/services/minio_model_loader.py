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

    def load_model(self, model_type: str):
        """Load a model from MinIO"""
        model_path = f"models/DS{self.ds_number}/{model_type}_DS{self.ds_number}.joblib"
        try:
            model_data = self.minio_client.get_object(
                bucket_name=self.bucket_name, object_name=model_path
            )
            model = joblib.load(BytesIO(model_data.data))
            model_data.close()
            return model
        except Exception as e:
            logger.error(f"Error loading model {model_path}: {str(e)}")
            raise
