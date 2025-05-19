import os
import datetime
import joblib
from minio import Minio
from io import BytesIO
from codart.metrics.testability_learning import Regression


class ModelTrainingService:
    def __init__(
        self,
        minio_endpoint: str,
        minio_access_key: str,
        minio_secret_key: str,
        bucket_name: str = "ml-models",
    ):
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
            secure=False,  # Set to True if using HTTPS
        )

        # Create bucket if not exists
        if not self.minio_client.bucket_exists(bucket_name):
            self.minio_client.make_bucket(bucket_name)

        self.bucket_name = bucket_name
        # Dictionary to store models in memory
        self.models_cache = {}

    def download_dataset_from_minio(self, dataset_path: str):
        """
        Download dataset from MinIO

        Args:
            dataset_path (str): Path to dataset in MinIO

        Returns:
            str: Local path to downloaded dataset
        """
        # Create temp directory if it doesn't exist
        os.makedirs("/tmp", exist_ok=True)

        local_path = f"/tmp/{os.path.basename(dataset_path)}"

        # Ensure the directory for the local path exists
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        # Download dataset from MinIO
        self.minio_client.fget_object(
            bucket_name="metrics", object_name=dataset_path, file_path=local_path
        )

        return local_path

    def train_dataset_g7(
        self,
        ds_number: int,
        dataset_path: str,
        project_name: str = None,
        project_version: str = None,
    ):
        """
        Train dataset and save models directly to MinIO without local files

        Args:
            ds_number (int): Dataset number to train
            dataset_path (str): Path to dataset in MinIO
            project_name (str, optional): Project name to include in model paths
            project_version (str, optional): Project version to include in model paths

        Returns:
            dict: Training results and model paths
        """
        start_time = datetime.datetime.now()

        # Create project directory structure
        project_dir = ""
        if project_name and project_version:
            project_dir = f"{project_name}/{project_version}/"
        elif project_name:
            project_dir = f"{project_name}/"

        # Ensure temporary directory exists for download
        os.makedirs("/tmp", exist_ok=True)

        # Create temp directory if it doesn't exist
        os.makedirs("/tmp", exist_ok=True)

        # Download dataset
        local_dataset_path = self.download_dataset_from_minio(dataset_path)

        # Initialize Regression with the downloaded dataset
        reg = Regression(df_path=local_dataset_path)

        # Model training configurations
        model_configs = [
            {"model_number": 2, "model_type": "RFR1"},  # RandomForestRegressor
            {"model_number": 4, "model_type": "HGBR1"},  # HistGradientBoostingRegressor
            {"model_number": 6, "model_type": "MLPR1"},  # MLPRegressor
            {"model_type": "VR1"},  # Voting Regressor
        ]

        results = {}
        trained_models = {}

        # First, train all the base models and save them to memory
        for config in model_configs:
            if config["model_type"] == "VR1":
                continue  # Skip VR1 for now, it will be trained after the base models

            model_type = config["model_type"]
            minio_model_path = (
                f"models/DS{ds_number}/{project_dir}{model_type}_DS{ds_number}.joblib"
            )

            try:
                # Train the model without saving to file, but return it
                model = reg.regress(
                    model_path=None,  # Don't save to file
                    model_number=config["model_number"],
                    return_model=True,  # Return the trained model
                )

                # Store the trained model in memory cache for VR1
                model_key = f"{model_type}_DS{ds_number}"
                trained_models[model_key] = model

                # Create a buffer for serializing the model
                model_buffer = BytesIO()
                joblib.dump(model, model_buffer)
                model_buffer.seek(0)

                # Upload directly to MinIO
                self.minio_client.put_object(
                    bucket_name=self.bucket_name,
                    object_name=minio_model_path,
                    data=model_buffer,
                    length=model_buffer.getbuffer().nbytes,
                    content_type="application/octet-stream",
                )

                results[model_type] = {
                    "minio_path": minio_model_path,
                    "trained_at": datetime.datetime.now().isoformat(),
                }

            except Exception as e:
                results[model_type] = {"error": str(e)}

        # Now train the Voting Regressor using the models in memory
        try:
            vr_model_type = "VR1"
            vr_minio_path = f"models/DS{ds_number}/{project_dir}{vr_model_type}_DS{ds_number}.joblib"

            # Train VR model using in-memory models
            vr_model = reg.vote(
                model_path=None,  # Don't save to file
                dataset_number=ds_number,
                models_dict=trained_models,  # Pass in-memory models
                return_model=True,  # Return the trained model
            )

            # Serialize and upload to MinIO
            vr_buffer = BytesIO()
            joblib.dump(vr_model, vr_buffer)
            vr_buffer.seek(0)

            self.minio_client.put_object(
                bucket_name=self.bucket_name,
                object_name=vr_minio_path,
                data=vr_buffer,
                length=vr_buffer.getbuffer().nbytes,
                content_type="application/octet-stream",
            )

            results[vr_model_type] = {
                "minio_path": vr_minio_path,
                "trained_at": datetime.datetime.now().isoformat(),
            }

        except Exception as e:
            results["VR1"] = {"error": str(e)}

        # Calculate total training time
        end_time = datetime.datetime.now()
        results["training_time"] = str(end_time - start_time)

        # Add project info to results
        if project_name or project_version:
            results["project_info"] = {"name": project_name, "version": project_version}

        # Clean up memory cache
        trained_models.clear()

        return results

    def list_trained_models(self, prefix: str = "models/"):
        """
        List trained models in MinIO

        Args:
            prefix (str, optional): Prefix to filter models. Defaults to 'models/'.

        Returns:
            list: List of trained model paths
        """
        models = []
        objects = self.minio_client.list_objects(
            bucket_name=self.bucket_name, prefix=prefix, recursive=True
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
            bucket_name=self.bucket_name, object_name=model_path
        )

        # Load model from bytes
        model = joblib.load(BytesIO(model_data.data))
        model_data.close()

        return model
