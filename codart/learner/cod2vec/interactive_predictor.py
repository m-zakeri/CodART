import os
from common import common
from extractor import Extractor
from codart.learner.sbr_initializer.utils.utility import logger, config

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

    def __init__(self, model):
        model.predict([])
        self.model = model
        self.config = config
        self.path_extractor = Extractor(
            config,
            jar_path=JAR_PATH,
            max_path_length=MAX_PATH_LENGTH,
            max_path_width=MAX_PATH_WIDTH,
        )

    def read_file(self, input_filename):
        with open(input_filename, "r") as file:
            return file.readlines()

    def predict(self):
        input_filename = "Input.java"
        logger.info("Starting interactive prediction...")
        while True:
            logger.info(
                'Modify the file: "%s" and press any key when ready, or "q" / "quit" / "exit" to exit'
                % input_filename
            )
            user_input = input()
            if user_input.lower() in self.exit_keywords:
                logger.info("Exiting...")
                return
            try:
                predict_lines, hash_to_string_dict = self.path_extractor.extract_paths(
                    input_filename
                )
            except ValueError as e:
                logger.error(e)
                continue
            raw_prediction_results = self.model.predict(predict_lines)
            method_prediction_results = common.parse_prediction_results(
                raw_prediction_results,
                hash_to_string_dict,
                self.model.vocabs.target_vocab.special_words,
                topk=SHOW_TOP_CONTEXTS,
            )
            for raw_prediction, method_prediction in zip(
                raw_prediction_results, method_prediction_results
            ):
                logger.info("Original name:\t" + method_prediction.original_name)
                for name_prob_pair in method_prediction.predictions:
                    logger.info(
                        "\t(%f) predicted: %s"
                        % (name_prob_pair["probability"], name_prob_pair["name"])
                    )
                logger.info("Attention:")
                for attention_obj in method_prediction.attention_paths:
                    logger.info(
                        "%f\tcontext: %s,%s,%s"
                        % (
                            attention_obj["score"],
                            attention_obj["token1"],
                            attention_obj["path"],
                            attention_obj["token2"],
                        )
                    )
                if config["COD2VEC"]["EXPORT_CODE_VECTORS"]:
                    logger.info("Code vector:")
                    logger.info(" ".join(map(str, raw_prediction.code_vector)))
