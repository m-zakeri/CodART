import re
import random
from codart.utility.directory_utils import reset_project, update_understand_database2
from codart.learner.sbr_initializer.abstraction import Initializer
import understand as und
import pandas as pd
from codart.refactorings.handler import MoveMethod, PullupMethod, PushdownMethod, MoveClass, ExtractMethod, ExtractClass
from codart.refactorings.abstraction import EmptyRefactoring
import os
from codart.learner.sbr_initializer.utils.utility import Utils, logger, config
from collections import Counter
import time
from codart.refactorings import (
    move_method,
    extract_method,
    extract_class,
    pullup_method,
    pushdown_method2,
)
import requests
from requests.auth import HTTPBasicAuth
import redis
from io import StringIO
from minio import Minio
from datetime import timedelta


minio_endpoint = os.getenv("MINIO_ENDPOINT", "minio:9000")
minio_access_key = os.getenv("MINIO_ACCESS_KEY", "00jFBl7n9Jn0ex0XL7m1")
minio_secret_key = os.getenv("MINIO_SECRET_KEY", "kYfujzkdSGjXKLN9oQhPDIVgRUaZRijvj1yaXmIZ")
minio_bucket = os.getenv("MINIO_BUCKET", "code-smells")


class SmellInitialization(Initializer):

    def __init__(self, *args, **kwargs):
        super(SmellInitialization, self).__init__(
            *args,
            **kwargs,
        )
        self.project_path = kwargs.get('project_path', '')
        self.utils = Utils(
            logger=logger,
            initializers=self.initializers,
            population=self.population,
            project_name=kwargs.get('project_name', ''),
            version_id=kwargs.get('version_id', ''),
            project_dir= self.project_path
        )
        self.minio_client = Minio(
            minio_endpoint,
            access_key=minio_access_key,
            secret_key=minio_secret_key,
            secure=False,
        )
        self.redis_client = redis.Redis(
            host=os.getenv("REDIS_HOST", "redis"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            db=0,
            decode_responses=True,
        )

        # Track selected items to prevent reselection
        self.selected_classes = set()
        self.selected_methods = set()
        self.selected_files = set()

        # Cache for CSV data to avoid multiple downloads
        self._csv_cache = None
        self._csv_cache_timestamp = None

    def _get_cache_key(self, project_name: str, version_id: str) -> str:
        """Generate a cache key for the CSV data"""
        return f"csv_cache_{project_name}_{version_id}"

    def _is_cache_valid(self) -> bool:
        """Check if the cached CSV data is still valid (less than 5 minutes old)"""
        if self._csv_cache is None or self._csv_cache_timestamp is None:
            return False

        current_time = time.time()
        return (current_time - self._csv_cache_timestamp) < 300  # 5 minutes

    def remove_from_csv_and_upload(self, project_name: str, version_id: str, removal_criteria: dict):
        """
        Remove entries from CSV based on criteria and upload updated CSV back to MinIO

        Args:
            project_name (str): Name of the project
            version_id (str): Version ID of the project
            removal_criteria (dict): Dictionary with keys like 'class_name', 'method_name', 'file_path'
        """
        try:
            # Get the current CSV data
            df = self.get_code_smells_csv(project_name, version_id)

            if df.empty:
                logger.warning("CSV is empty, nothing to remove")
                return

            original_count = len(df)

            # Apply removal criteria
            if 'class_name' in removal_criteria:
                class_name = removal_criteria['class_name']
                # Remove entries where File contains the class name
                df = df[~df['File'].str.contains(f"{class_name}.java", case=False, na=False)]
                logger.info(f"Removed entries for class: {class_name}")

            if 'method_name' in removal_criteria and 'line' in removal_criteria:
                method_name = removal_criteria['method_name']
                line_number = removal_criteria['line']
                # Remove specific line entries (approximate match)
                df = df[~((df['Line'] == line_number) &
                          (df['Description'].str.contains(method_name, case=False, na=False)))]
                logger.info(f"Removed entries for method: {method_name} at line: {line_number}")

            if 'file_path' in removal_criteria:
                file_path = removal_criteria['file_path']
                file_name = os.path.basename(file_path)
                df = df[~df['File'].str.contains(file_name, case=False, na=False)]
                logger.info(f"Removed entries for file: {file_name}")

            removed_count = original_count - len(df)
            logger.info(f"Removed {removed_count} entries from CSV. Remaining: {len(df)} entries")

            # Upload the updated CSV back to MinIO
            if removed_count > 0:
                self._upload_updated_csv(df, project_name, version_id)
                # Clear cache to force reload of updated CSV
                self._csv_cache = None
                self._csv_cache_timestamp = None

        except Exception as e:
            logger.error(f"Error removing from CSV: {str(e)}", exc_info=True)

    def _upload_updated_csv(self, df: pd.DataFrame, project_name: str, version_id: str):
        """Upload the updated CSV back to MinIO"""
        try:
            # Convert DataFrame to CSV string
            csv_string = df.to_csv(index=False)
            csv_bytes = csv_string.encode('utf-8')

            # Define the object path
            object_path = f"{project_name}/{version_id}/code_smells_{project_name}_{version_id}.csv"

            # Upload to MinIO
            from io import BytesIO
            csv_stream = BytesIO(csv_bytes)

            self.minio_client.put_object(
                minio_bucket,
                object_path,
                csv_stream,
                length=len(csv_bytes),
                content_type='text/csv'
            )

            logger.info(f"Successfully uploaded updated CSV to MinIO: {object_path}")

            # Generate a new presigned URL and update Redis
            fresh_url = self.minio_client.presigned_get_object(
                minio_bucket,
                object_path,
                expires=timedelta(hours=24)
            )

            # Update Redis with the new URL
            redis_key = f"project:{project_name}:version:{version_id}:code_smells_url"
            self.redis_client.set(redis_key, fresh_url, ex=86400)  # 24 hours expiry

            logger.info(f"Updated Redis with new CSV URL: {redis_key}")

        except Exception as e:
            logger.error(f"Error uploading updated CSV: {str(e)}", exc_info=True)

    def generate_population(self):
        logger.debug(f"Generating a biased initial population ...")
        for _ in range(0, self.population_size):
            individual = []
            individual_size = random.randint(self.lower_band, self.upper_band)
            for j in range(individual_size):
                main, params, name = self.utils.select_random()
                logger.debug(f"Refactoring name: {name}")
                logger.debug(f"Refactoring params: {params}")
                is_correct_refactoring = main(**params)
                while is_correct_refactoring is False:
                    reset_project(project_path=self.project_path, udb_path=self.udb_path)
                    main, params, name = self.utils.select_random()
                    logger.debug(f"Refactoring name: {name}")
                    logger.debug(f"Refactoring params: {params}")
                    is_correct_refactoring = main(**params)
                update_understand_database2(self.udb_path)
                individual.append((main, params, name))
                logger.debug(
                    f'Append a refactoring "{name}" to "{j}th" gene of the individual {_}.'
                )
                reset_project(project_path=self.project_path, udb_path=self.udb_path)
                logger.debug("-" * 100)
            self.population.append(individual)
            logger.debug(f"Append individual {_} to population, s")
        logger.debug("=" * 100)
        initial_pop_path = f"{config['Config']['PROJECT_LOG_DIR']}initial_population_{time.time()}.json"
        self.utils.dump_population(path=initial_pop_path)
        logger.debug(f"Generating a biased initial population was finished.")
        return self.population

    def generate_an_action(self):
        """Enhanced action generation with better error handling and consistent tensor structure"""
        logger.debug("Generating one random refactoring...")
        available_initializers = [
            (self.init_move_method, "Move Method"),
            (self.init_extract_class, "Extract Class"),
            # (self.init_extract_method, "Extract Method"),
            (self.init_pull_up_method, "Pull Up Method"),
            (self.init_push_down_method, "Push Down Method")
        ]

        if not available_initializers:
            logger.error("No refactoring candidates available for any refactoring type!")
            return EmptyRefactoring()

        # Try each available initializer until one works
        random.shuffle(available_initializers)
        max_attempts = 3  # Limit attempts to prevent infinite loops

        try:
            attempt_count = 0
            for initializer, initializer_name in available_initializers:
                if attempt_count >= max_attempts:
                    logger.warning(f"Max attempts ({max_attempts}) reached")
                    break

                try:
                    logger.debug(f"Trying initializer: {initializer_name}")
                    result = initializer()

                    # Check if initializer returned None (no candidates)
                    if result is None or result[0] is None:
                        logger.warning(f"No candidates for {initializer_name}, skipping")
                        continue

                    main, params, name = result
                    logger.debug(f"Selected refactoring name: {name}")
                    logger.debug(f"Selected refactoring params: {params}")

                    # Reset project state before attempting refactoring
                    reset_project(project_path=self.project_path, udb_path=self.udb_path)

                    try:
                        is_correct_refactoring = main(**params, project_dir=self.project_path)
                        if is_correct_refactoring is None:
                            logger.error("Refactoring returned None for success status")
                            is_correct_refactoring = False
                        elif not isinstance(is_correct_refactoring, bool):
                            logger.warning(f"Refactoring returned non-boolean: {is_correct_refactoring}")
                            is_correct_refactoring = bool(is_correct_refactoring)

                        if is_correct_refactoring:
                            # Success! Update database and return RefactoringOperation
                            update_understand_database2(self.udb_path)
                            logger.debug(f"Successfully generated refactor: {name}")

                            # Track the selection and remove from CSV
                            self._track_and_remove_selection(name, params)

                            # Create a RefactoringOperation based on the type with consistent structure
                            if name == "Move Method":
                                return MoveMethod(
                                    source_class=params.get("source_class", ""),
                                    method_name=params.get("method_name", ""),
                                    udb_path=params.get("udb_path", ""),
                                    source_package=params.get("source_package", ""),
                                    target_package=params.get("target_package", ""),
                                    target_class=params.get("target_class", ""),
                                    project_dir=self.project_path
                                )
                            elif name == "Extract Class":
                                return ExtractClass(
                                    udb_path=params.get("udb_path", ""),
                                    moved_methods=params.get("moved_methods", []),
                                    source_class=params.get("source_class", ""),
                                    file_path=params.get("file_path", ""),
                                    moved_fields=params.get("moved_fields", []),
                                    project_dir=self.project_path
                                )
                            elif name == "Extract Method":
                                return ExtractMethod(
                                    file_path=params.get("file_path", ""),
                                    lines=params.get("lines", {})
                                )
                            elif name == "Pull Up Method":
                                return PullupMethod(
                                    udb_path=params.get("udb_path", ""),
                                    method_name=params.get("method_name", ""),
                                    children_classes=params.get("children_classes", [])
                                )
                            elif name == "Push Down Method":
                                return PushdownMethod(
                                    udb_path=params.get("udb_path", ""),
                                    method_name=params.get("method_name", ""),
                                    source_class=params.get("source_class", ""),
                                    source_package=params.get("source_package", ""),
                                    target_classes=params.get("target_classes", [])
                                )
                            elif name == "Move Class":
                                return MoveClass(
                                    udb_path=params.get("udb_path", ""),
                                    class_name=params.get("source_class", ""),
                                    source_package=params.get("source_package", ""),
                                    target_package=params.get("target_classes", [])
                                )
                            else:
                                logger.warning(f"Unknown refactoring type: {name}, creating empty operation")
                                return EmptyRefactoring()
                        else:
                            logger.warning(f"{initializer_name} returned False - resetting project")
                            reset_project(project_path=self.project_path, udb_path=self.udb_path)

                    except Exception as inner_e:
                        logger.error(f"Error executing {initializer_name}: {str(inner_e)}")
                        import traceback
                        logger.error(f"Traceback: {traceback.format_exc()}")
                        reset_project(project_path=self.project_path, udb_path=self.udb_path)
                        continue

                except Exception as e:
                    logger.error(f"Error in {initializer_name}: {str(e)}")
                    import traceback
                    logger.error(f"Traceback: {traceback.format_exc()}")
                    reset_project(project_path=self.project_path, udb_path=self.udb_path)
                    continue

                attempt_count += 1

            # If all initializers failed, return an empty RefactoringOperation
            logger.warning("All refactoring initializers failed, returning an empty operation")
            return EmptyRefactoring()

        except Exception as e:
            logger.error(f"Error generating refactoring action: {str(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return EmptyRefactoring()

        # Try each available initializer until one works
        random.shuffle(available_initializers)

        try:
            # Try each available initializer until one works
            for initializer, initializer_name in available_initializers:
                try:
                    logger.debug(f"Trying initializer: {initializer_name}")
                    result = initializer()

                    # Check if initializer returned None (no candidates)
                    if result is None or result[0] is None:
                        logger.warning(f"No candidates for {initializer_name}, skipping")
                        continue

                    main, params, name = result
                    logger.debug(f"Selected refactoring name: {name}")
                    logger.debug(f"Selected refactoring params: {params}")

                    try:
                        is_correct_refactoring = main(**params)
                        if is_correct_refactoring:
                            # Success! Update database and return RefactoringOperation
                            update_understand_database2(self.udb_path)
                            logger.debug(f"Successfully generated refactor: {name}")

                            # Track the selection and remove from CSV
                            self._track_and_remove_selection(name, params)

                            # Create a RefactoringOperation based on the type
                            if name == "Move Method":
                                return MoveMethod(
                                    source_class=params.get("source_class", ""),
                                    method_name=params.get("method_name", ""),
                                    udb_path=params.get("udb_path", ""),
                                    source_package=params.get("source_package", ""),
                                    target_package=params.get("target_package", ""),
                                    target_class=params.get("target_class", ""),
                                    project_dir=self.project_path
                                )
                            elif name == "Extract Class":
                                return ExtractClass(
                                    udb_path=params.get("udb_path", ""),
                                    moved_methods=params.get("moved_methods", []),
                                    source_class=params.get("source_class", ""),
                                    file_path=params.get("file_path", ""),
                                    moved_fields=params.get("moved_fields", [])
                                )
                            elif name == "Extract Method":
                                return ExtractMethod(
                                    file_path=params.get("file_path", ""),
                                    lines=params.get("lines", {})
                                )
                            elif name == "Pull Up Method":
                                return PullupMethod(
                                    udb_path=params.get("udb_path", ""),
                                    method_name=params.get("method_name", ""),
                                    children_classes=params.get("children_classes", [])
                                )
                            elif name == "Push Down Method":
                                return PushdownMethod(
                                    udb_path=params.get("udb_path", ""),
                                    method_name=params.get("method_name", ""),
                                    source_class=params.get("source_class", ""),
                                    source_package=params.get("source_package", ""),
                                    target_classes=params.get("target_classes", [])
                                )
                            elif name == "Move Class":
                                return MoveClass(
                                    udb_path=params.get("udb_path", ""),
                                    class_name=params.get("source_class", ""),
                                    source_package=params.get("source_package", ""),
                                    target_package=params.get("target_classes", [])
                                )
                            else:
                                logger.warning(f"Unknown refactoring type: {name}, creating empty operation")
                                return EmptyRefactoring()
                        else:
                            logger.warning(f"{initializer_name} returned False - resetting project")
                            reset_project(project_path=self.project_path, udb_path=self.udb_path)
                    except Exception as inner_e:
                        logger.error(f"Error executing {initializer_name}: {str(inner_e)}")
                        import traceback
                        logger.error(f"Traceback: {traceback.format_exc()}")
                        reset_project(project_path=self.project_path, udb_path=self.udb_path)
                        continue
                except Exception as e:
                    logger.error(f"Error in {initializer_name}: {str(e)}")
                    import traceback
                    logger.error(f"Traceback: {traceback.format_exc()}")
                    reset_project(project_path=self.project_path, udb_path=self.udb_path)
                    continue

            # If all initializers failed, return an empty RefactoringOperation
            logger.warning("All refactoring initializers failed, returning an empty operation")
            return EmptyRefactoring()

        except Exception as e:
            logger.error(f"Error generating refactoring action: {str(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return EmptyRefactoring()

    def _track_and_remove_selection(self, refactoring_name: str, params: dict):
        """Track selected items and remove them from CSV to prevent reselection"""
        try:
            removal_criteria = {}

            if refactoring_name == "Move Method":
                class_name = params.get("source_class", "")
                method_name = params.get("method_name", "")
                if class_name and method_name:
                    self.selected_classes.add(class_name)
                    self.selected_methods.add(f"{class_name}.{method_name}")
                    removal_criteria = {"class_name": class_name}

            elif refactoring_name == "Extract Class":
                class_name = params.get("source_class", "")
                file_path = params.get("file_path", "")
                if class_name:
                    self.selected_classes.add(class_name)
                    removal_criteria = {"class_name": class_name}
                elif file_path:
                    self.selected_files.add(file_path)
                    removal_criteria = {"file_path": file_path}

            elif refactoring_name == "Extract Method":
                file_path = params.get("file_path", "")
                if file_path:
                    self.selected_files.add(file_path)
                    removal_criteria = {"file_path": file_path}

            elif refactoring_name in ["Pull Up Method", "Push Down Method"]:
                method_name = params.get("method_name", "")
                source_class = params.get("source_class", "")
                if source_class:
                    self.selected_classes.add(source_class)
                    removal_criteria = {"class_name": source_class}
                if method_name:
                    self.selected_methods.add(method_name)

            # Remove from CSV if we have criteria
            if removal_criteria:
                self.remove_from_csv_and_upload(
                    self.utils.project_name,
                    self.utils.version_id,
                    removal_criteria
                )

        except Exception as e:
            logger.error(f"Error tracking and removing selection: {str(e)}", exc_info=True)

    def get_code_smells_csv(self, project_name: str, version_id: str):
        """
        Centralized method to download code smells CSV from MinIO or Redis URL.
        Uses caching to avoid multiple downloads of the same data.
        """
        try:
            # Check if we have valid cached data
            if self._is_cache_valid():
                logger.debug("Using cached CSV data")
                return self._csv_cache.copy()  # Return a copy to prevent modifications

            object_paths = [
                f"{project_name}/{version_id}/code_smells_{project_name}_{version_id}.csv",
                f"{project_name}/{version_id}/pmd_results.csv",
            ]

            # Try to get CSV data using direct MinIO access
            csv_data = None
            for object_path in object_paths:
                try:
                    logger.info(f"Trying to download {object_path} from MinIO")
                    response = self.minio_client.get_object(minio_bucket, object_path)
                    data = response.read()
                    csv_data = StringIO(data.decode('utf-8'))
                    logger.info(f"Successfully downloaded {object_path} from MinIO")
                    break
                except Exception as e:
                    logger.warning(f"Could not download {object_path}: {str(e)}")
                    continue

            # If direct MinIO access failed, try Redis URL as fallback
            if csv_data is None:
                logger.info("Direct MinIO access failed, trying Redis URL")

                # Get the URL from Redis
                csv_url = self.redis_client.get(f"project:{project_name}:version:{version_id}:code_smells_url")

                if csv_url:
                    logger.info(f"Got URL from Redis: {csv_url}")

                    # Try to extract object path from URL and generate a fresh presigned URL
                    try:
                        from urllib.parse import urlparse
                        parsed_url = urlparse(csv_url)
                        path = parsed_url.path
                        # Remove leading slash and bucket name
                        parts = path.split('/')
                        if len(parts) > 2:  # We expect at least /bucket/path
                            bucket_name = parts[1]
                            object_name = '/'.join(parts[2:])

                            if bucket_name == minio_bucket:
                                # Generate a fresh presigned URL
                                fresh_url = self.minio_client.presigned_get_object(
                                    minio_bucket,
                                    object_name,
                                    expires=timedelta(hours=1)  # 1 hour
                                )
                                logger.info(f"Generated fresh presigned URL: {fresh_url}")

                                # Try the fresh URL
                                response = requests.get(fresh_url)
                                if response.status_code == 200:
                                    csv_data = StringIO(response.text)
                                    logger.info("Successfully downloaded using fresh presigned URL")
                    except Exception as e:
                        logger.warning(f"Error generating fresh presigned URL: {str(e)}")

                    # If we still don't have the data, try the original URL with different auth methods
                    if csv_data is None:
                        # Try without auth
                        try:
                            logger.info("Trying original URL without auth")
                            response = requests.get(csv_url)
                            if response.status_code == 200:
                                csv_data = StringIO(response.text)
                                logger.info("Successfully downloaded using original URL without auth")
                            else:
                                logger.warning(f"HTTP error {response.status_code} when downloading without auth")
                        except Exception as e:
                            logger.warning(f"Error with original URL: {str(e)}")

                        # Try with basic auth as last resort
                        if csv_data is None:
                            try:
                                logger.info("Trying with basic auth")
                                response = requests.get(
                                    csv_url,
                                    auth=HTTPBasicAuth(minio_access_key, minio_secret_key)
                                )
                                if response.status_code == 200:
                                    csv_data = StringIO(response.text)
                                    logger.info("Successfully downloaded using basic auth")
                                else:
                                    logger.warning(
                                        f"HTTP error {response.status_code} when downloading with basic auth")
                            except Exception as e:
                                logger.warning(f"Error with basic auth: {str(e)}")

            # If we still don't have CSV data, create minimal empty DataFrame with expected columns
            if csv_data is None:
                logger.error("All attempts to get CSV data failed, using empty DataFrame")
                empty_data = "Rule,Line,Package,File,Priority,Description\n"
                csv_data = StringIO(empty_data)

            # Parse the CSV data
            df = pd.read_csv(csv_data)
            logger.info(f"Loaded CSV with {len(df)} rows")

            # Cache the data
            self._csv_cache = df.copy()
            self._csv_cache_timestamp = time.time()

            return df

        except Exception as e:
            logger.error(f"Error in get_code_smells_csv: {str(e)}", exc_info=True)
            # Return an empty DataFrame with the expected columns
            return pd.DataFrame(columns=["Rule", "Line", "Package", "File", "Priority", "Description"])

    def load_move_method_candidates_improved(self, project_name: str = "", version_id: str = ""):
        """Load move method candidates with better validation and fallback strategies"""
        try:
            candidates = []

            # Strategy 1: Try to get from PMD data
            try:
                pmd_results = self.get_code_smells_csv(project_name, version_id)
                feature_envies = pmd_results[pmd_results['Rule'].str.contains('LawOfDemeter', case=False, na=False)]
                logger.info(f"Found {len(feature_envies)} Law of Demeter violations")

                if len(feature_envies) > 0:
                    candidates = self._extract_candidates_from_pmd(feature_envies)
            except Exception as e:
                logger.warning(f"Failed to get PMD candidates: {str(e)}")

            # Strategy 2: If no PMD candidates or they all failed, generate from UDB
            if not candidates:
                logger.info("No PMD candidates available, generating from UDB analysis")
                candidates = self._generate_smart_move_candidates()

            # Strategy 3: If still no candidates, use simple fallback
            if not candidates:
                logger.info("Generating simple fallback candidates")
                candidates = self._generate_simple_fallback_candidates()

            logger.info(f"Total move method candidates: {len(candidates)}")
            return candidates

        except Exception as e:
            logger.error(f"Error in load_move_method_candidates_improved: {str(e)}")
            return self._generate_simple_fallback_candidates()

    def _extract_candidates_from_pmd(self, feature_envies):
        """Extract candidates from PMD data with validation"""
        candidates = []
        db = und.open(self.udb_path)

        try:
            for index, row in feature_envies.head(10).iterrows():  # Limit to first 10 for performance
                try:
                    source_package = row['Package']
                    file_path = row['File']
                    source_class_name = os.path.basename(file_path).replace('.java', '')

                    # Skip if already selected
                    if source_class_name in self.selected_classes:
                        continue

                    # Find class in UDB
                    class_entities = db.lookup(f"{source_package}.{source_class_name}", "Class")
                    if not class_entities:
                        class_entities = db.lookup(source_class_name, "Class")

                    if not class_entities:
                        continue

                    source_class_ent = class_entities[0]

                    # Get all non-constructor, non-static methods
                    methods = []
                    for ref in source_class_ent.refs("Define", "Method"):
                        method_ent = ref.ent()
                        if (method_ent.simplename() != source_class_name and  # Not constructor
                                "Static" not in method_ent.kindname() and  # Not static
                                "Abstract" not in method_ent.kindname()):  # Not abstract
                            methods.append(method_ent)

                    if not methods:
                        continue

                    # Pick a random method
                    method = random.choice(methods)
                    method_key = f"{source_class_name}.{method.simplename()}"

                    if method_key in self.selected_methods:
                        continue

                    # Find a suitable target class
                    target_class_ent = self._find_suitable_target_class(db, source_class_ent)
                    if not target_class_ent:
                        continue

                    target_package = ".".join(target_class_ent.longname().split(".")[:-1])
                    target_class_name = target_class_ent.simplename()

                    candidate = {
                        "source_package": source_package,
                        "source_class": source_class_name,
                        "method_name": method.simplename(),
                        "target_package": target_package,
                        "target_class": target_class_name,
                    }

                    candidates.append(candidate)
                    logger.debug(f"Added PMD candidate: {candidate}")

                except Exception as e:
                    logger.debug(f"Error processing PMD row: {str(e)}")
                    continue

        finally:
            db.close()

        return candidates

    def _generate_smart_move_candidates(self):
        """Generate candidates by analyzing actual method usage patterns"""
        candidates = []
        db = und.open(self.udb_path)

        try:
            # Get all classes that aren't selected and aren't test classes
            all_classes = []
            for class_ent in db.ents("Class ~Unknown"):
                class_name = class_ent.simplename()
                if (class_name not in self.selected_classes and
                        not class_name.endswith("Test") and
                        not class_name.startswith("Test") and
                        len(class_name) > 2):  # Avoid very short class names
                    all_classes.append(class_ent)

            # Sort by number of methods (prefer classes with more methods)
            all_classes.sort(key=lambda c: len(list(c.refs("Define", "Method"))), reverse=True)

            # Take top classes for analysis
            sample_classes = all_classes[:min(10, len(all_classes))]

            for source_class in sample_classes:
                try:
                    source_package = ".".join(source_class.longname().split(".")[:-1])
                    source_class_name = source_class.simplename()

                    # Get methods that are good candidates for moving
                    moveable_methods = []
                    for ref in source_class.refs("Define", "Method"):
                        method_ent = ref.ent()
                        method_name = method_ent.simplename()
                        method_key = f"{source_class_name}.{method_name}"

                        # Check if method is suitable for moving
                        if (method_name != source_class_name and  # Not constructor
                                "Static" not in method_ent.kindname() and  # Not static
                                "Abstract" not in method_ent.kindname() and  # Not abstract
                                "Private" not in method_ent.kindname() and  # Not private
                                method_key not in self.selected_methods and  # Not already selected
                                len(method_name) > 2):  # Reasonable name length

                            # Check if method has some external dependencies (good for moving)
                            external_calls = 0
                            for call_ref in method_ent.refs("Call", "Method"):
                                called_method = call_ref.ent()
                                if called_method.parent() and called_method.parent().id() != source_class.id():
                                    external_calls += 1

                            if external_calls > 0:  # Has external dependencies
                                moveable_methods.append((method_ent, external_calls))

                    if not moveable_methods:
                        continue

                    # Sort by external calls (methods with more external calls are better candidates)
                    moveable_methods.sort(key=lambda x: x[1], reverse=True)

                    # Pick the best method
                    method_ent = moveable_methods[0][0]

                    # Find a good target class
                    target_class = self._find_suitable_target_class(db, source_class)
                    if not target_class:
                        continue

                    target_package = ".".join(target_class.longname().split(".")[:-1])

                    candidate = {
                        "source_package": source_package,
                        "source_class": source_class_name,
                        "method_name": method_ent.simplename(),
                        "target_package": target_package,
                        "target_class": target_class.simplename(),
                    }

                    candidates.append(candidate)
                    logger.debug(f"Added smart candidate: {candidate}")

                    # Limit number of candidates
                    if len(candidates) >= 5:
                        break

                except Exception as e:
                    logger.debug(f"Error analyzing class {source_class.simplename()}: {str(e)}")
                    continue

        finally:
            db.close()

        return candidates

    def _find_suitable_target_class(self, db, source_class):
        """Find a suitable target class for method movement"""
        source_class_name = source_class.simplename()

        # Get all available classes
        available_classes = []
        for class_ent in db.ents("Class ~Unknown"):
            class_name = class_ent.simplename()
            if (class_name not in self.selected_classes and
                    class_name != source_class_name and
                    not class_name.endswith("Test") and
                    not class_name.startswith("Test") and
                    len(class_name) > 2):
                available_classes.append(class_ent)

        if not available_classes:
            return None

        # Prefer classes in the same package
        same_package_classes = []
        source_package = ".".join(source_class.longname().split(".")[:-1])

        for class_ent in available_classes:
            class_package = ".".join(class_ent.longname().split(".")[:-1])
            if class_package == source_package:
                same_package_classes.append(class_ent)

        if same_package_classes:
            return random.choice(same_package_classes)
        else:
            return random.choice(available_classes)

    def _generate_simple_fallback_candidates(self):
        """Generate simple fallback candidates when all else fails"""
        candidates = []
        db = und.open(self.udb_path)

        try:
            # Get any two classes that exist and have methods
            all_classes = list(db.ents("Class ~Unknown"))
            suitable_classes = []

            for class_ent in all_classes:
                class_name = class_ent.simplename()
                if (class_name not in self.selected_classes and
                        not class_name.endswith("Test") and
                        not class_name.startswith("Test")):

                    # Check if class has non-constructor methods
                    methods = [ref.ent() for ref in class_ent.refs("Define", "Method")
                               if ref.ent().simplename() != class_name]
                    if methods:
                        suitable_classes.append((class_ent, methods))

            if len(suitable_classes) >= 2:
                # Pick two random classes
                source_class, source_methods = suitable_classes[0]
                target_class, _ = suitable_classes[1]

                # Pick a random method
                method = random.choice(source_methods)

                source_package = ".".join(source_class.longname().split(".")[:-1])
                target_package = ".".join(target_class.longname().split(".")[:-1])

                candidate = {
                    "source_package": source_package,
                    "source_class": source_class.simplename(),
                    "method_name": method.simplename(),
                    "target_package": target_package,
                    "target_class": target_class.simplename(),
                }

                candidates.append(candidate)
                logger.debug(f"Added fallback candidate: {candidate}")

        finally:
            db.close()

        return candidates

    def load_extract_method_candidates(self, project_name=None, version_id=None):
        """Load extract method candidates from code smells or generate fallback candidates, excluding selected files"""
        # Use config values if parameters are not provided
        if not project_name:
            project_name = config["PROJECT"]["NAME"]
        if not version_id:
            version_id = config["PROJECT"]["VERSION"]

        candidates = []

        try:
            # Get code smells CSV using the centralized method
            pmd_results = self.get_code_smells_csv(project_name, version_id)

            # Filter for Long Method or complex method smells
            method_smells = pmd_results[pmd_results['Rule'].isin([
                'CyclomaticComplexity', 'NPathComplexity', 'ExcessiveMethodLength',
                'CognitiveComplexity', 'StdCyclomaticComplexity'
            ])]

            logger.info(f"Found {len(method_smells)} method complexity smells")

            for _, row in method_smells.iterrows():
                file_path = row['File']

                # Skip if this file is already selected
                if file_path in self.selected_files:
                    logger.debug(f"Skipping already selected file: {file_path}")
                    continue

                line_number = row.get('Line', 0)

                # Only get a few consecutive lines within the method
                # This is a simplification - you'd need to analyze the file to get valid statement lines
                if line_number > 0:
                    # Create a mapping of line numbers with a simple value (doesn't need to be preserved)
                    # Extract 3-5 consecutive lines starting from the identified problem line
                    num_lines = random.randint(3, 5)
                    lines = {line_number + i: True for i in range(num_lines)}

                    candidates.append({
                        "file_path": file_path,
                        "lines": lines
                    })
        except Exception as e:
            logger.warning(f"Error loading PMD results for extract method candidates: {str(e)}")

        # If no candidates found, create fallback candidates
        if not candidates:
            logger.warning("No extract method candidates found from PMD, generating fallback candidates")
            # Find some Java files in the project that are not selected
            try:
                _db = und.open(self.udb_path)
                file_ents = _db.ents("file ~unknown ~unresolved")
                java_files = [f.longname() for f in file_ents
                              if f.longname().endswith('.java')
                              and f.longname() not in self.selected_files]

                if java_files:
                    for _ in range(min(5, len(java_files))):
                        file_path = random.choice(java_files)

                        # Pick random line range (this is a simplified approach)
                        start_line = random.randint(20, 50)  # Just some reasonable line numbers
                        num_lines = random.randint(3, 8)
                        lines = {start_line + i: True for i in range(num_lines)}

                        candidates.append({
                            "file_path": file_path,
                            "lines": lines
                        })
                _db.close()
            except Exception as e:
                logger.error(f"Error generating fallback extract method candidates: {str(e)}")

        logger.info(f"Returning {len(candidates)} extract method candidates")
        return candidates

    def load_extract_class_candidates(self, project_name=None, version_id=None):
        """Load extract class candidates from code smells CSV, excluding selected classes."""
        # Use config values if parameters are not provided
        if not project_name:
            project_name = config["PROJECT"]["NAME"]
        if not version_id:
            version_id = config["PROJECT"]["VERSION"]

        try:
            # Get code smells CSV using the centralized method
            pmd_results = self.get_code_smells_csv(project_name, version_id)

            # Filter for God Class issues
            god_classes = pmd_results[pmd_results['Rule'].isin(['GodClass', 'TooManyMethods', 'ExcessivePublicCount'])]
            logger.info(f"Found {len(god_classes)} God Class violations")

            candidates = []
            processed_classes = set()

            for index, row in god_classes.iterrows():
                # Skip if we've already processed this class
                if row['File'] in processed_classes:
                    continue

                processed_classes.add(row['File'])

                # Extract class information
                source_package = row['Package']
                file_path = row['File']
                source_class = os.path.basename(file_path).replace('.java', '')

                # Skip if this class is already selected
                if source_class in self.selected_classes:
                    logger.debug(f"Skipping already selected class: {source_class}")
                    continue

                # We need to open the UDB to get fields and methods
                _db = und.open(self.udb_path)

                try:
                    # Try to find the class in the UDB
                    ent = _db.lookup(f"{source_package}.{source_class}", "class")

                    if not ent:
                        logger.warning(f"Could not find class {source_package}.{source_class} in UDB")
                        continue

                    if len(ent) > 0:
                        ent = ent[0]

                    # Get methods and fields for the class
                    moved_methods = []
                    moved_fields = []

                    # Get a subset of methods (up to 30% of methods)
                    methods = ent.ents("Define", "Method")
                    if methods:
                        num_methods_to_move = max(1, len(methods) // 3)  # Move about 1/3 of methods
                        for i in range(min(num_methods_to_move, len(methods))):
                            method = methods[i]
                            moved_methods.append(method.simplename())

                    # Get a subset of fields (up to 30% of fields)
                    fields = ent.ents("Define", "Variable")
                    if fields:
                        num_fields_to_move = max(1, len(fields) // 3)  # Move about 1/3 of fields
                        for i in range(min(num_fields_to_move, len(fields))):
                            field = fields[i]
                            moved_fields.append(field.simplename())

                    candidates.append({
                        "source_class": source_class,
                        "moved_fields": moved_fields,
                        "moved_methods": moved_methods,
                        "file_path": file_path,
                    })

                except Exception as e:
                    logger.error(f"Error processing class {source_class}: {str(e)}")
                finally:
                    _db.close()

            logger.info(f"Returning {len(candidates)} extract class candidates")
            return candidates

        except Exception as e:
            logger.error(f"Error in load_extract_class_candidates: {str(e)}", exc_info=True)
            return []

    def load_push_down_method_candidates(self, project_name=None, version_id=None):
        """Load push down method candidates based on class hierarchy in UDB, excluding selected classes"""
        # For push-down method, we need class hierarchy information which isn't directly in the PMD results
        # So we'll use the UDB as before but filter based on PMD results if possible

        # First get the code smells to identify problematic classes
        if not project_name:
            project_name = config["PROJECT"]["NAME"]
        if not version_id:
            version_id = config["PROJECT"]["VERSION"]

        # Get code smells CSV using the centralized method
        pmd_results = self.get_code_smells_csv(project_name, version_id)

        problematic_classes = set()
        try:
            # Get classes with high complexity or too many methods
            complex_classes = pmd_results[pmd_results['Rule'].isin(['CyclomaticComplexity', 'TooManyMethods'])]

            for _, row in complex_classes.iterrows():
                class_name = os.path.basename(row['File']).replace('.java', '')
                # Only add if not already selected
                if class_name not in self.selected_classes:
                    problematic_classes.add(class_name)
        except Exception as e:
            logger.warning(f"Error loading PMD results for push down candidates: {str(e)}")

        # Now use the UDB to find hierarchy information
        _db = und.open(self.udb_path)
        candidates = []

        try:
            # Get all public classes
            class_entities = _db.ents("Class ~Unknown ~Anonymous ~TypeVariable ~Private ~Static")

            # Filter out selected classes
            available_classes = [e for e in class_entities if e.simplename() not in self.selected_classes]

            # Prioritize problematic classes
            if problematic_classes:
                prioritized_entities = [e for e in available_classes if e.simplename() in problematic_classes]
                # Add the rest
                prioritized_entities.extend([e for e in available_classes if e.simplename() not in problematic_classes])
                class_entities = prioritized_entities
            else:
                class_entities = available_classes

            for ent in class_entities:
                params = {
                    "source_class": "",
                    "source_package": "",
                    "method_name": "",
                    "target_classes": [],
                }
                method_names = []

                # Get subclasses (excluding selected ones)
                for ref in ent.refs("Extendby ~Implicit", "Public Class"):
                    if ref.ent().simplename() not in self.selected_classes:
                        params["source_class"] = ent.simplename()
                        ln = ent.longname().split(".")
                        params["source_package"] = ln[0] if len(ln) > 1 else ""
                        params["target_classes"].append(ref.ent().simplename())

                # Get methods (excluding selected ones)
                for ref in ent.refs("Define", "Method"):
                    method_key = f"{ent.simplename()}.{ref.ent().simplename()}"
                    if method_key not in self.selected_methods:
                        method_names.append(ref.ent().simplename())

                if method_names:
                    params["method_name"] = random.choice(method_names)
                else:
                    continue

                if params["target_classes"]:
                    params["target_classes"] = [random.choice(params["target_classes"])]
                else:
                    continue

                if params["source_class"] != "":
                    candidates.append(params)

        except Exception as e:
            logger.error(f"Error analyzing class hierarchy: {str(e)}")
        finally:
            _db.close()

        return candidates

    def load_pull_up_method_candidates(self, project_name=None, version_id=None):
        """Load pull up method candidates based on class hierarchy in UDB, excluding selected classes"""
        # For pull-up method, we need class hierarchy information which isn't directly in the PMD results
        # So we'll use the UDB as before but filter based on PMD results if possible

        # First get the code smells to identify problematic classes
        if not project_name:
            project_name = config["PROJECT"]["NAME"]
        if not version_id:
            version_id = config["PROJECT"]["VERSION"]

        # Get code smells CSV using the centralized method
        pmd_results = self.get_code_smells_csv(project_name, version_id)

        problematic_classes = set()
        try:
            # Get classes with duplicate code or similar issues
            duplicate_classes = pmd_results[
                pmd_results['Rule'].isin(['DuplicatedBlocks', 'CyclomaticComplexity'])]

            for _, row in duplicate_classes.iterrows():
                class_name = os.path.basename(row['File']).replace('.java', '')
                # Only add if not already selected
                if class_name not in self.selected_classes:
                    problematic_classes.add(class_name)
        except Exception as e:
            logger.warning(f"Error loading PMD results for pull up candidates: {str(e)}")

        # Now use the UDB to find hierarchy information
        _db = und.open(self.udb_path)
        candidates = []

        try:
            # Get all public classes
            class_entities = _db.ents("Class ~Unknown ~Anonymous ~TypeVariable ~Private ~Static")

            # Filter out selected classes
            available_classes = [e for e in class_entities if e.simplename() not in self.selected_classes]

            # Prioritize problematic classes
            if problematic_classes:
                prioritized_entities = [e for e in available_classes if e.simplename() in problematic_classes]
                # Add the rest
                prioritized_entities.extend([e for e in available_classes if e.simplename() not in problematic_classes])
                class_entities = prioritized_entities
            else:
                class_entities = available_classes

            common_methods = []

            for ent in class_entities:
                children = []
                class_method_dict = {}
                father_methods = []

                # Get methods in parent class
                for met_ref in ent.refs("Define", "Method ~Override"):
                    method = met_ref.ent()
                    father_methods.append(method.simplename())

                # Get child classes and their methods (excluding selected classes)
                for ref in ent.refs("Extendby"):
                    child = ref.ent()
                    if not child.kind().check("public class"):
                        continue
                    child_name = child.simplename()

                    # Skip if child class is already selected
                    if child_name in self.selected_classes:
                        continue

                    children.append(child_name)
                    if child_name not in class_method_dict:
                        class_method_dict[child_name] = []

                    for met_ref in child.refs("Define", "Method"):
                        method = met_ref.ent()
                        method_name = method.simplename()

                        if method.ents("Override"):
                            continue

                        # Skip if method is already selected
                        method_key = f"{child_name}.{method_name}"
                        if method_key in self.selected_methods:
                            continue

                        if method_name not in father_methods:
                            common_methods.append(method_name)
                            class_method_dict[child_name].append(method_name)

                # Find methods that appear in multiple child classes
                counts = Counter(common_methods)
                common_methods = [value for value, count in counts.items() if count > 1]
                if len(common_methods) > 0:
                    random_method = random.choice(common_methods)
                    children = [
                        k for k, v in class_method_dict.items() if random_method in v
                    ]
                    if len(children) > 1:
                        candidates.append(
                            {
                                "method_name": random.choice(common_methods),
                                "children_classes": children,
                            }
                        )
        except Exception as e:
            logger.error(f"Error analyzing class hierarchy for pull-up method: {str(e)}")
        finally:
            _db.close()

        return candidates

    def init_move_method(self):
        """Initialize move method with enhanced validation"""
        try:
            candidates = self.load_move_method_candidates_improved(self.project_name, self.version_id)
            if not candidates:
                logger.warning("No move method candidates available")
                return None, None, None

            # Try multiple candidates to find a valid one
            max_attempts = min(3, len(candidates))
            random.shuffle(candidates)

            for i in range(max_attempts):
                try:
                    params = candidates[i].copy()
                    params["udb_path"] = self.udb_path

                    # Simple validation - check if required parameters exist
                    required_params = ["source_class", "method_name", "source_package", "target_package",
                                       "target_class"]
                    if all(params.get(p) for p in required_params):
                        # Quick UDB check to ensure method exists
                        db = und.open(self.udb_path)
                        try:
                            full_method_name = f"{params['source_package']}.{params['source_class']}.{params['method_name']}"
                            method_lookup = db.lookup(full_method_name, "Method")

                            if len(method_lookup) > 0 and method_lookup[0].simplename() == params['method_name']:
                                db.close()
                                main = move_method.main
                                return main, params, "Move Method"
                            else:
                                logger.debug(f"Method validation failed for candidate {i + 1}: {full_method_name}")
                                db.close()
                                continue
                        except Exception as e:
                            logger.debug(f"Error during method lookup: {str(e)}")
                            db.close()
                            continue
                    else:
                        logger.debug(f"Missing required parameters in candidate {i + 1}")
                        continue

                except Exception as e:
                    logger.warning(f"Error validating candidate {i + 1}: {str(e)}")
                    continue

            logger.warning("All move method candidates failed validation")
            return None, None, None

        except Exception as e:
            logger.error(f"Error in init_move_method: {str(e)}")
            return None, None, None

    def init_extract_class(self):
        """Initialize extract class with enhanced validation"""
        try:
            candidates = self.load_extract_class_candidates(self.project_name, self.version_id)
            if not candidates:
                logger.warning("No extract class candidates available")
                return None, None, None

            # Validate candidate has required fields
            valid_candidates = []
            for candidate in candidates:
                if (candidate.get("source_class") and
                        candidate.get("file_path") and
                        os.path.exists(candidate["file_path"]) and
                        (candidate.get("moved_methods") or candidate.get("moved_fields"))):
                    valid_candidates.append(candidate)

            if not valid_candidates:
                logger.warning("No valid extract class candidates found")
                return None, None, None

            main = extract_class.main
            params = random.choice(valid_candidates)
            params["udb_path"] = self.udb_path
            return main, params, "Extract Class"

        except Exception as e:
            logger.error(f"Error in init_extract_class: {str(e)}")
            return None, None, None

    def init_extract_method(self):
        """Initialize extract method refactoring with appropriate parameters"""
        try:
            candidates = self.load_extract_method_candidates(self.project_name, self.version_id)

            # Check if candidates list is empty
            if not candidates:
                logger.warning("No extract method candidates found, returning None")
                return None, None, None

            # Try up to 3 different candidates in case some fail
            random.shuffle(candidates)

            max_attempts = min(3, len(candidates))
            for i in range(max_attempts):
                try:
                    params = candidates[i]
                    logger.debug(f"Trying extract method candidate {i + 1}/{max_attempts}: {params}")

                    # Validate if the file exists
                    if not os.path.isfile(params["file_path"]):
                        logger.warning(f"File {params['file_path']} does not exist, skipping candidate")
                        continue

                    # Validate line numbers against file length
                    try:
                        with open(params["file_path"], 'r', encoding='utf-8', errors='ignore') as f:
                            file_lines = sum(1 for _ in f)

                        # Check if all line numbers are within file bounds
                        invalid_lines = [line_num for line_num in params["lines"].keys() if line_num > file_lines]
                        if invalid_lines:
                            logger.warning(
                                f"Invalid line numbers {invalid_lines} in {params['file_path']}, skipping candidate")
                            continue

                        # Check if the lines form a continuous block (this is often a requirement)
                        line_nums = sorted(params["lines"].keys())
                        if line_nums[-1] - line_nums[0] + 1 != len(line_nums):
                            logger.warning(f"Lines {line_nums} do not form a continuous block, skipping candidate")
                            continue
                    except Exception as e:
                        logger.warning(f"Error validating file lines: {str(e)}")
                        continue

                    # If all checks pass, proceed with this candidate
                    main = extract_method.main
                    return main, params, "Extract Method"
                except Exception as e:
                    logger.warning(f"Failed to initialize extract method with candidate {i + 1}: {str(e)}")
                    continue

            # If we've tried all candidates and none worked, return None
            logger.warning("All extract method candidates failed, returning None")
            return None, None, None
        except Exception as e:
            logger.error(f"Error in init_extract_method: {str(e)}")
            return None, None, None

    def init_pull_up_method(self):
        candidates = self.load_pull_up_method_candidates(self.project_name, self.version_id)

        # Check if candidates list is empty
        if not candidates:
            logger.warning("No pull up method candidates found, returning None")
            # Return None to indicate no valid candidates
            return None, None, None

        # If we have candidates, proceed as before
        main = pullup_method.main
        params = random.choice(candidates)
        params["udb_path"] = self.udb_path
        return main, params, "Pull Up Method"

    def init_push_down_method(self):
        candidates = self.load_push_down_method_candidates(self.project_name, self.version_id)

        # Check if candidates list is empty
        if not candidates:
            logger.warning("No push down method candidates found, returning None")
            return None, None, None

        main = pushdown_method2.main
        params = random.choice(candidates)
        params["udb_path"] = self.udb_path
        return main, params, "Push Down Method"

    def reset_selections(self):
        """Reset all selections to start fresh"""
        self.selected_classes.clear()
        self.selected_methods.clear()
        self.selected_files.clear()
        logger.info("Reset all selections")