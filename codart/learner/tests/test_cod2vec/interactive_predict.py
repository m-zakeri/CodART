import os
from common import common
from extractor import Extractor
from codart.learner.sbr_initializer.utils.utility import logger, config
import tensorflow as tf

try:
    import understand as und
except ImportError as e:
    print(e)

tf.compat.v1.disable_eager_execution()

SHOW_TOP_CONTEXTS = config.getint("COD2VEC", "SHOW_TOP_CONTEXTS", fallback=10)
MAX_PATH_LENGTH = config.getint("COD2VEC", "MAX_PATH_LENGTH", fallback=8)
MAX_PATH_WIDTH = config.getint("COD2VEC", "MAX_PATH_WIDTH", fallback=2)
JAR_PATH = config.get(
    "COD2VEC",
    "JAR_PATH",
    fallback=os.path.join(
        "JavaExtractor", "JPredict", "target", "JavaExtractor-0.0.1-SNAPSHOT.jar"
    ),
)


class InteractivePredictor:
    exit_keywords = ["exit", "quit", "q"]

    def __init__(self, model, database_path):
        # model.predict([])
        self.sess = tf.compat.v1.Session()
        self.model = model
        self.config = config
        self.path_extractor = Extractor(
            config,
            jar_path=JAR_PATH,
            max_path_length=MAX_PATH_LENGTH,
            max_path_width=MAX_PATH_WIDTH,
        )
        self.functions_dict = self.extract_functions(database_path)
        self.class_dict = self.extract_classes(database_path)

    def extract_functions(self, database_path):
        """Extract functions from the Understand database."""
        db = und.open(database_path)
        functions_dict = {}

        # Iterate over all functions in the database
        for func in db.ents("function,method,procedure"):
            class_name = func.parent().longname() if func.parent() else "N/A"
            package_name = func.library() if func.library() else "N/A"
            file_path = func.filerefs().longname() if func.filerefs() else "N/A"

            # Get the function's complete content
            function_content = (
                func.contents().strip()
            )  # Use contents() to get the full function body

            # Populate the dictionary with extracted data
            functions_dict[func.longname()] = {
                "class_name": class_name,
                "package_name": package_name,
                "file_path": file_path,
                "function_content": function_content,  # Store the full content
            }

        return functions_dict

    def extract_classes(self, database_path):
        """Extract classes from the Understand database."""
        db = und.open(database_path)
        classes_dict = {}

        # Iterate over all classes in the database
        for cls in db.ents("class"):
            package_name = cls.library() if cls.library() else "N/A"
            file_path = cls.filerefs().longname() if cls.filerefs() else "N/A"

            # Get the class's complete content
            class_content = (
                cls.contents().strip()
            )  # Use contents() to get the full class body

            # Populate the dictionary with extracted data
            classes_dict[cls.longname()] = {
                "package_name": package_name,
                "file_path": file_path,
                "class_content": class_content,  # Store the full content
            }

        return classes_dict

    def predict(self):
        logger.info("Starting interactive prediction...")
        all_predictions = []  # Initialize a list to hold all predictions

        for function_name, data in self.functions_dict.items():
            print(f"\nAnalyzing function: {function_name}")
            print(f"  Package Name: {data['package_name']}")
            print(f"  File Path: {data['file_path']}")
            print(
                f"  Function Content:\n{data['function_content'][:30]}..."
            )  # Display a snippet

            # Predicting with cod2vec using the function content directly
            input_lines = data["function_content"]  # Pass the complete function body

            try:
                # Extract paths for the cod2vec model
                if input_lines == "":
                    print("no content for prediction found")
                    continue

                predict_lines, hash_to_string_dict = self.path_extractor.extract_paths(
                    input_lines
                )
                raw_prediction_results = self.model.predict(predict_lines)
                print("Prediction results:")
                # Check if predictions exist
                if not raw_prediction_results:
                    logger.warning(f"No predictions made for {function_name}")
                    continue  # Skip this function if no predictions

                method_prediction_results = common.parse_prediction_results(
                    raw_prediction_results,
                    hash_to_string_dict,
                    self.model.vocabs.target_vocab.special_words,
                    topk=SHOW_TOP_CONTEXTS,
                )

                # Collect predictions
                function_predictions = {
                    "function_name": function_name,
                    "predictions": [],
                }

                # Iterate through raw predictions and method predictions
                for raw_prediction, method_prediction in zip(
                    raw_prediction_results, method_prediction_results
                ):
                    prediction_info = {
                        "original_name": method_prediction.original_name,
                        "predicted": [
                            {
                                "name": name_prob_pair["name"],
                                "probability": name_prob_pair["probability"],
                            }
                            for name_prob_pair in method_prediction.predictions
                        ],
                        "attention_paths": [
                            {
                                "score": attention_obj["score"],
                                "context": (
                                    attention_obj["token1"],
                                    attention_obj["path"],
                                    attention_obj["token2"],
                                ),
                            }
                            for attention_obj in method_prediction.attention_paths
                        ],
                    }
                    function_predictions["predictions"].append(prediction_info)

                # Append each function's predictions to the all_predictions list
                all_predictions.append(function_predictions)

                if (
                    self.config["COD2VEC"]["EXPORT_CODE_VECTORS"]
                    and raw_prediction is not None
                ):
                    logger.info("Code vector:")
                    logger.info(" ".join(map(str, raw_prediction.code_vector)))

            except ValueError as e:
                print("ERROR 1, ", e)
                logger.error(f"Error processing function {function_name}: {e}")
            except Exception as general_e:
                print("ERROR 2, ", general_e)
                logger.error(f"An unexpected error occurred: {general_e}")

        return all_predictions
