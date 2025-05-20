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
        self.project_path=kwargs.get('project_path', '')
        self.utils = Utils(
            logger=logger,
            initializers=self.initializers,
            population=self.population,
            project_name=kwargs.get('project_name', ''),
            version_id=kwargs.get('version_id', '')
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
        logger.debug("Generating one random refactoring...")
        available_initializers = []
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

                            # Create a RefactoringOperation based on the type
                            if name == "Move Method":
                                return MoveMethod(
                                    source_class=params.get("source_class", ""),
                                    method_name=params.get("method_name", ""),
                                    udb_path=params.get("udb_path", ""),
                                    source_package=params.get("source_package", ""),
                                    target_package=params.get("target_package", ""),
                                    target_class=params.get("target_class", "")
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

    def get_code_smells_csv(self, project_name: str, version_id: str):
        """
        Centralized method to download code smells CSV from MinIO or Redis URL.
        Uses multiple fallback strategies to ensure the CSV is retrieved.

        Args:
            project_name (str): Name of the project
            version_id (str): Version ID of the project

        Returns:
            pd.DataFrame: DataFrame containing the code smells data, or an empty DataFrame if download fails
        """
        try:
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
            return df

        except Exception as e:
            logger.error(f"Error in get_code_smells_csv: {str(e)}", exc_info=True)
            # Return an empty DataFrame with the expected columns
            return pd.DataFrame(columns=["Rule", "Line", "Package", "File", "Priority", "Description"])

    def load_move_method_candidates(self, project_name: str = "", version_id: str = ""):
        """Load move method candidates from code smells CSV."""
        try:
            # Get code smells CSV using the centralized method
            pmd_results = self.get_code_smells_csv(project_name, version_id)

            # Filter for feature envy issues (Law of Demeter violations)
            feature_envies = pmd_results[pmd_results['Rule'].str.contains('LawOfDemeter', case=False, na=False)]
            logger.info(f"Found {len(feature_envies)} Law of Demeter violations")

            candidates = []

            # Open the UDB to get actual method information
            _db = und.open(self.udb_path)
            try:
                # Get all classes in the project
                classes = {ent.longname(): ent for ent in _db.ents("class ~unknown ~anonymous")}
                logger.debug(f"Found {len(classes)} classes in UDB")

                for index, row in feature_envies.iterrows():
                    try:
                        # Extract source information from the Package and File columns
                        source_package = row['Package']
                        file_path = row['File']
                        source_class_name = os.path.basename(file_path).replace('.java', '')

                        # Find the class in the UDB
                        source_class_longname = f"{source_package}.{source_class_name}"
                        source_class = classes.get(source_class_longname)

                        if not source_class:
                            logger.warning(f"Could not find class {source_class_longname} in UDB")
                            continue

                        # Find the method containing the line number from the description
                        line_number = row.get('Line', 0)

                        # Get all methods in the source class
                        methods = source_class.ents("define", "method")

                        # Find a method that contains the line number
                        method = None
                        for m in methods:
                            if not hasattr(m, 'line') or not m.line():
                                continue

                            # Get start and end line numbers
                            start_line = m.line()
                            end_line = m.line() + m.metric(["CountLineCode"])

                            if start_line <= line_number <= end_line:
                                method = m
                                break

                        if not method:
                            # If we couldn't find a method by line number, just pick one randomly
                            if methods:
                                method = random.choice(methods)
                            else:
                                continue

                        # Extract target class from the Description
                        description = row['Description']
                        target_match = re.search(r"on foreign value `([^`]+)`", description)
                        if target_match:
                            target_class_name = target_match.group(1)

                            # Try to find the target class in the UDB
                            target_class = next((c for c in classes.values() if c.simplename() == target_class_name),
                                                None)

                            if not target_class:
                                # If not found, just pick another class that's not the source class
                                other_classes = [c for c in classes.values() if c.longname() != source_class_longname]
                                if other_classes:
                                    target_class = random.choice(other_classes)
                                else:
                                    continue

                            target_package = ".".join(target_class.longname().split(".")[:-1])
                            target_class_name = target_class.simplename()
                        else:
                            # If we can't extract target class, pick a random one that's not the source
                            other_classes = [c for c in classes.values() if c.longname() != source_class_longname]
                            if not other_classes:
                                continue

                            target_class = random.choice(other_classes)
                            target_package = ".".join(target_class.longname().split(".")[:-1])
                            target_class_name = target_class.simplename()

                        candidates.append({
                            "source_package": source_package,
                            "source_class": source_class_name,
                            "method_name": method.simplename(),
                            "target_package": target_package,
                            "target_class": target_class_name,
                        })
                    except Exception as e:
                        logger.warning(f"Error processing PMD result: {str(e)}")
                        continue
            finally:
                _db.close()

            # If no candidates were found, create some default ones based on class hierarchy
            if not candidates:
                logger.warning("No move method candidates found from PMD, generating fallback candidates")
                candidates = self._generate_fallback_move_method_candidates()

            logger.info(f"Returning {len(candidates)} move method candidates")
            return candidates

        except Exception as e:
            logger.error(f"Error in load_move_method_candidates: {str(e)}", exc_info=True)
            return []

    def _generate_fallback_move_method_candidates(self):
        """Generate some fallback move method candidates if PMD doesn't provide any"""
        candidates = []
        _db = und.open(self.udb_path)

        try:
            classes = list(_db.ents("class ~unknown ~anonymous"))
            # Need at least 2 classes to move a method between them
            if len(classes) < 2:
                return []

            # Pick a few random classes to work with
            sample_size = min(5, len(classes))
            sample_classes = random.sample(classes, sample_size)

            for source_class in sample_classes:
                methods = source_class.ents("define", "method ~constructor")
                if not methods:
                    continue

                method = random.choice(methods)

                # Pick a target class different from the source
                target_classes = [c for c in classes if c.id() != source_class.id()]
                if not target_classes:
                    continue

                target_class = random.choice(target_classes)

                source_package = ".".join(source_class.longname().split(".")[:-1])
                target_package = ".".join(target_class.longname().split(".")[:-1])

                candidates.append({
                    "source_package": source_package,
                    "source_class": source_class.simplename(),
                    "method_name": method.simplename(),
                    "target_package": target_package,
                    "target_class": target_class.simplename(),
                })

        except Exception as e:
            logger.error(f"Error generating fallback move method candidates: {str(e)}")
        finally:
            _db.close()

        return candidates

    def load_extract_method_candidates(self, project_name=None, version_id=None):
        """Load extract method candidates from code smells or generate fallback candidates"""
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
            # Find some Java files in the project
            try:
                _db = und.open(self.udb_path)
                file_ents = _db.ents("file ~unknown ~unresolved")
                java_files = [f.longname() for f in file_ents if f.longname().endswith('.java')]

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
        """Load extract class candidates from code smells CSV."""
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

    # 3. Updated load_push_down_method_candidates function
    def load_push_down_method_candidates(self, project_name=None, version_id=None):
        """Load push down method candidates based on class hierarchy in UDB"""
        # For push-down method, we need class hierarchy information which isn't directly in the PMD results
        # So we'll use the UDB as before but filter based on PMD results if possible

        # First get the code smells to identify problematic classes
        if not project_name:
            project_name = config["PROJECT"]["NAME"]
        if not version_id:
            version_id = config["PROJECT"]["VERSION"]

        # Fetch the code smells URL from Redis
        redis_client = redis.Redis(
            host=os.getenv("REDIS_HOST", "redis"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            db=0,
            decode_responses=True,
        )
        csv_url = redis_client.get(f"project:{project_name}:version:{version_id}:code_smells_url")

        problematic_classes = set()
        if csv_url:
            try:
                # Download CSV from MinIO
                response = requests.get(csv_url)
                if response.status_code == 200:
                    # Parse CSV data
                    csv_data = StringIO(response.text)
                    pmd_results = pd.read_csv(csv_data)

                    # Get classes with high complexity or too many methods
                    complex_classes = pmd_results[pmd_results['Rule'].isin(['CyclomaticComplexity', 'TooManyMethods'])]

                    for _, row in complex_classes.iterrows():
                        class_name = os.path.basename(row['File']).replace('.java', '')
                        problematic_classes.add(class_name)
            except Exception as e:
                logger.warning(f"Error loading PMD results for push down candidates: {str(e)}")

        # Now use the UDB to find hierarchy information
        _db = und.open(self.udb_path)
        candidates = []

        try:
            # Get all public classes
            class_entities = _db.ents("Class ~Unknown ~Anonymous ~TypeVariable ~Private ~Static")

            # Prioritize problematic classes
            if problematic_classes:
                prioritized_entities = [e for e in class_entities if e.simplename() in problematic_classes]
                # Add the rest
                prioritized_entities.extend([e for e in class_entities if e.simplename() not in problematic_classes])
                class_entities = prioritized_entities

            for ent in class_entities:
                params = {
                    "source_class": "",
                    "source_package": "",
                    "method_name": "",
                    "target_classes": [],
                }
                method_names = []

                # Get subclasses
                for ref in ent.refs("Extendby ~Implicit", "Public Class"):
                    params["source_class"] = ent.simplename()
                    ln = ent.longname().split(".")
                    params["source_package"] = ln[0] if len(ln) > 1 else ""
                    params["target_classes"].append(ref.ent().simplename())

                # Get methods
                for ref in ent.refs("Define", "Method"):
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

    # 4. Updated load_pull_up_method_candidates function
    def load_pull_up_method_candidates(self, project_name=None, version_id=None):
        """Load pull up method candidates based on class hierarchy in UDB"""
        # For pull-up method, we need class hierarchy information which isn't directly in the PMD results
        # So we'll use the UDB as before but filter based on PMD results if possible

        # First get the code smells to identify problematic classes
        if not project_name:
            project_name = config["PROJECT"]["NAME"]
        if not version_id:
            version_id = config["PROJECT"]["VERSION"]

        # Fetch the code smells URL from Redis
        redis_client = redis.Redis(
            host=os.getenv("REDIS_HOST", "redis"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            db=0,
            decode_responses=True,
        )
        csv_url = redis_client.get(f"project:{project_name}:version:{version_id}:code_smells_url")

        problematic_classes = set()
        if csv_url:
            try:
                # Download CSV from MinIO
                response = requests.get(csv_url)
                if response.status_code == 200:
                    # Parse CSV data
                    csv_data = StringIO(response.text)
                    pmd_results = pd.read_csv(csv_data)

                    # Get classes with duplicate code or similar issues
                    duplicate_classes = pmd_results[
                        pmd_results['Rule'].isin(['DuplicatedBlocks', 'CyclomaticComplexity'])]

                    for _, row in duplicate_classes.iterrows():
                        class_name = os.path.basename(row['File']).replace('.java', '')
                        problematic_classes.add(class_name)
            except Exception as e:
                logger.warning(f"Error loading PMD results for pull up candidates: {str(e)}")

        # Now use the UDB to find hierarchy information
        _db = und.open(self.udb_path)
        candidates = []

        try:
            # Get all public classes
            class_entities = _db.ents("Class ~Unknown ~Anonymous ~TypeVariable ~Private ~Static")

            # Prioritize problematic classes
            if problematic_classes:
                prioritized_entities = [e for e in class_entities if e.simplename() in problematic_classes]
                # Add the rest
                prioritized_entities.extend([e for e in class_entities if e.simplename() not in problematic_classes])
                class_entities = prioritized_entities

            common_methods = []

            for ent in class_entities:
                children = []
                class_method_dict = {}
                father_methods = []

                # Get methods in parent class
                for met_ref in ent.refs("Define", "Method ~Override"):
                    method = met_ref.ent()
                    father_methods.append(method.simplename())

                # Get child classes and their methods
                for ref in ent.refs("Extendby"):
                    child = ref.ent()
                    if not child.kind().check("public class"):
                        continue
                    child_name = child.simplename()
                    children.append(child_name)
                    if child_name not in class_method_dict:
                        class_method_dict[child_name] = []

                    for met_ref in child.refs("Define", "Method"):
                        method = met_ref.ent()
                        method_name = method.simplename()

                        if method.ents("Override"):
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
        params = random.choice(self.load_move_method_candidates(self.project_name, self.version_id))
        params["udb_path"] = self.udb_path
        main = move_method.main
        return main, params, "Move Method"

    def init_extract_class(self):
        main = extract_class.main
        params = random.choice(self.load_extract_class_candidates(self.project_name, self.version_id))
        params["udb_path"] = self.udb_path
        return main, params, "Extract Class"

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
        return main, params, "PullUp Method"

    def init_push_down_method(self):
        main = pushdown_method2.main
        params = random.choice(self.load_push_down_method_candidates(self.project_name, self.version_id))
        params["udb_path"] = self.udb_path
        return main, params, "PushDown Method"

    def init_extract_method(self):
        """Initialize extract method refactoring with appropriate parameters"""
        main = extract_method.main
        params = random.choice(self.load_extract_method_candidates(self.project_name, self.version_id))
        return main, params, "Extract Method"