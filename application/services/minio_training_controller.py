import os
import datetime
import joblib
import pandas as pd
from minio import Minio
from io import BytesIO

from codart.metrics.testability_learning import Regression  # Import from your existing ML script


class ModelTrainingController:
    def __init__(self,
                 minio_endpoint: str,
                 minio_access_key: str,
                 minio_secret_key: str,
                 bucket_name: str = 'ml-models'):
        """
        Initialize MinIO client and training controller

        Args:
            minio_endpoint (str): MinIO server endpoint
            minio_access_key (str): MinIO access key
            minio_secret_key (str): MinIO secret key
            bucket_name (str, optional): Bucket to store models. Defaults to 'ml-models'.
        """
        self.minio_client = Minio(
            endpoint=minio_endpoint,
            access_key=minio_access_key,
            secret_key=minio_secret_key,
            secure=False  # Set to True if using HTTPS
        )

        # Create bucket if not exists
        if not self.minio_client.bucket_exists(bucket_name):
            self.minio_client.make_bucket(bucket_name)

        self.bucket_name = bucket_name

    def download_dataset_from_minio(self, dataset_path: str):
        """
        Download dataset from MinIO

        Args:
            dataset_path (str): Path to dataset in MinIO

        Returns:
            str: Local path to downloaded dataset
        """
        local_path = f"/tmp/{os.path.basename(dataset_path)}"

        # Download dataset from MinIO
        self.minio_client.fget_object(
            bucket_name=self.bucket_name,
            object_name=dataset_path,
            file_path=local_path
        )

        return local_path

    def train_dataset_g7(self, ds_number: int, dataset_path: str):
        """
        Train dataset and save models to MinIO

        Args:
            ds_number (int): Dataset number to train
            dataset_path (str): Path to dataset in MinIO

        Returns:
            dict: Training results and model paths
        """
        start_time = datetime.datetime.now()

        # Download dataset
        local_dataset_path = self.download_dataset_from_minio(dataset_path)

        # Initialize Regression with the downloaded dataset
        reg = Regression(df_path=local_dataset_path)

        # Model training configurations
        model_configs = [
            {'model_number': 2, 'model_type': 'RFR1'},  # RandomForestRegressor
            {'model_number': 4, 'model_type': 'HGBR1'},  # HistGradientBoostingRegressor
            {'model_number': 6, 'model_type': 'MLPR1'},  # MLPRegressor
            {'model_type': 'VR1'}  # Voting Regressor
        ]

        results = {}

        for config in model_configs:
            model_type = config['model_type']
            local_model_path = f"sklearn_models{ds_number}/{model_type}_DS{ds_number}.joblib"

            # Create directory if not exists
            os.makedirs(os.path.dirname(local_model_path), exist_ok=True)

            try:
                if model_type == 'VR1':
                    # Voting Regressor
                    reg.vote(model_path=local_model_path, dataset_number=ds_number)
                else:
                    # Other Regressors
                    reg.regress(
                        model_path=local_model_path,
                        model_number=config['model_number']
                    )

                # Upload model to MinIO
                minio_model_path = f"models/DS{ds_number}/{model_type}_DS{ds_number}.joblib"
                self.minio_client.fput_object(
                    bucket_name=self.bucket_name,
                    object_name=minio_model_path,
                    file_path=local_model_path
                )

                results[model_type] = {
                    'local_path': local_model_path,
                    'minio_path': minio_model_path,
                    'trained_at': datetime.datetime.now().isoformat()
                }

            except Exception as e:
                results[model_type] = {
                    'error': str(e)
                }

        # Calculate total training time
        end_time = datetime.datetime.now()
        results['training_time'] = str(end_time - start_time)

        return results

    def list_trained_models(self, prefix: str = 'models/'):
        """
        List trained models in MinIO

        Args:
            prefix (str, optional): Prefix to filter models. Defaults to 'models/'.

        Returns:
            list: List of trained model paths
        """
        models = []
        objects = self.minio_client.list_objects(
            bucket_name=self.bucket_name,
            prefix=prefix,
            recursive=True
        )

        for obj in objects:
            models.append(obj.object_name)

        return models

    def get_model_from_minio(self, model_path: str):
        """
        Retrieve model from MinIO

        Args:
            model_path (str): Path to model in MinIO

        Returns:
            object: Loaded ML model
        """
        # Download model to memory
        model_data = self.minio_client.get_object(
            bucket_name=self.bucket_name,
            object_name=model_path
        )

        # Load model from bytes
        model = joblib.load(BytesIO(model_data.data))
        model_data.close()

        return model