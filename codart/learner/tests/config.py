from math import ceil
from typing import Optional
import logging
import sys
import os


class Config:

    def set_defaults(self):
        self.NUM_TRAIN_EPOCHS = 20
        self.SAVE_EVERY_EPOCHS = 1
        self.TRAIN_BATCH_SIZE = 1024
        self.TEST_BATCH_SIZE = self.TRAIN_BATCH_SIZE
        self.TOP_K_WORDS_CONSIDERED_DURING_PREDICTION = 10
        self.NUM_BATCHES_TO_LOG_PROGRESS = 100
        self.NUM_TRAIN_BATCHES_TO_EVALUATE = 1800
        self.READER_NUM_PARALLEL_BATCHES = (
            6  # cpu cores [for tf.contrib.data.map_and_batch() in the reader]
        )
        self.SHUFFLE_BUFFER_SIZE = 10000
        self.CSV_BUFFER_SIZE = 100 * 1024 * 1024  # 100 MB
        self.MAX_TO_KEEP = 10

        # model hyper-params
        self.MAX_CONTEXTS = 200
        self.MAX_TOKEN_VOCAB_SIZE = 1301136
        self.MAX_TARGET_VOCAB_SIZE = 261245
        self.MAX_PATH_VOCAB_SIZE = 911417
        self.DEFAULT_EMBEDDINGS_SIZE = 128
        self.TOKEN_EMBEDDINGS_SIZE = self.DEFAULT_EMBEDDINGS_SIZE
        self.PATH_EMBEDDINGS_SIZE = self.DEFAULT_EMBEDDINGS_SIZE
        self.CODE_VECTOR_SIZE = self.context_vector_size
        self.TARGET_EMBEDDINGS_SIZE = self.CODE_VECTOR_SIZE
        self.DROPOUT_KEEP_RATE = 0.75
        self.SEPARATE_OOV_AND_PAD = False

    def load_from_args(self):
        self.PREDICT = True
        self.MODEL_SAVE_PATH = (
            "/home/y/Downloads/models/java14_model/saved_model_iter8_custom.release"
        )
        self.MODEL_LOAD_PATH = "/home/y/Downloads/models/java14_model/saved_model_iter8.release.data-00000-of-00001"
        self.TRAIN_DATA_PATH_PREFIX = ""
        self.TEST_DATA_PATH = ""
        self.RELEASE = True
        self.EXPORT_CODE_VECTORS = True
        self.SAVE_W2V = True
        self.SAVE_T2V = True
        self.VERBOSE_MODE = True
        self.LOGS_PATH = "/home/y/Downloads/models/java14_model/mylog.log"
        self.DL_FRAMEWORK = "tensorflow"
        self.USE_TENSORBOARD = True

    def __init__(
        self,
        set_defaults: bool = False,
        load_from_args: bool = True,
        verify: bool = False,
    ):
        self.NUM_TRAIN_EPOCHS: int = 0
        self.SAVE_EVERY_EPOCHS: int = 0
        self.TRAIN_BATCH_SIZE: int = 0
        self.TEST_BATCH_SIZE: int = 0
        self.TOP_K_WORDS_CONSIDERED_DURING_PREDICTION: int = 0
        self.NUM_BATCHES_TO_LOG_PROGRESS: int = 0
        self.NUM_TRAIN_BATCHES_TO_EVALUATE: int = 0
        self.READER_NUM_PARALLEL_BATCHES: int = 0
        self.SHUFFLE_BUFFER_SIZE: int = 0
        self.CSV_BUFFER_SIZE: int = 0
        self.MAX_TO_KEEP: int = 0

        # model hyper-params
        self.MAX_CONTEXTS: int = 1000
        self.MAX_TOKEN_VOCAB_SIZE: int = 0
        self.MAX_TARGET_VOCAB_SIZE: int = 0
        self.MAX_PATH_VOCAB_SIZE: int = 0
        self.DEFAULT_EMBEDDINGS_SIZE: int = 0
        self.TOKEN_EMBEDDINGS_SIZE: int = 0
        self.PATH_EMBEDDINGS_SIZE: int = 0
        self.CODE_VECTOR_SIZE: int = 0
        self.TARGET_EMBEDDINGS_SIZE: int = 0
        self.DROPOUT_KEEP_RATE: float = 0
        self.SEPARATE_OOV_AND_PAD: bool = False
        self.PREDICT: bool = False  # TODO: update README;
        self.MODEL_SAVE_PATH: Optional[str] = None
        self.MODEL_LOAD_PATH: Optional[str] = None
        self.TRAIN_DATA_PATH_PREFIX: Optional[str] = None
        self.TEST_DATA_PATH: Optional[str] = ""
        self.RELEASE: bool = False
        self.EXPORT_CODE_VECTORS: bool = False
        self.SAVE_W2V: Optional[str] = None  # TODO: update README;
        self.SAVE_T2V: Optional[str] = None  # TODO: update README;
        self.VERBOSE_MODE: int = 0
        self.LOGS_PATH: Optional[str] = None
        self.DL_FRAMEWORK: str = ""  # in {'keras', 'tensorflow'}
        self.USE_TENSORBOARD: bool = False

        # Automatically filled by `Code2VecModelBase._init_num_of_examples()`.
        self.NUM_TRAIN_EXAMPLES: int = 0
        self.NUM_TEST_EXAMPLES: int = 0

        self.__logger: Optional[logging.Logger] = None

        if set_defaults:
            self.set_defaults()
        if load_from_args:
            self.load_from_args()
        if verify:
            self.verify()

    @property
    def context_vector_size(self) -> int:
        # The context vector is actually a concatenation of the embedded
        # source & target vectors and the embedded path vector.
        return self.PATH_EMBEDDINGS_SIZE + 2 * self.TOKEN_EMBEDDINGS_SIZE

    @property
    def is_training(self) -> bool:
        return bool(self.TRAIN_DATA_PATH_PREFIX)

    @property
    def is_loading(self) -> bool:
        return bool(self.MODEL_LOAD_PATH)

    @property
    def is_saving(self) -> bool:
        return bool(self.MODEL_SAVE_PATH)

    @property
    def is_testing(self) -> bool:
        return bool(self.TEST_DATA_PATH)

    @property
    def train_steps_per_epoch(self) -> int:
        return (
            ceil(self.NUM_TRAIN_EXAMPLES / self.TRAIN_BATCH_SIZE)
            if self.TRAIN_BATCH_SIZE
            else 0
        )

    @property
    def test_steps(self) -> int:
        return (
            ceil(self.NUM_TEST_EXAMPLES / self.TEST_BATCH_SIZE)
            if self.TEST_BATCH_SIZE
            else 0
        )

    def data_path(self, is_evaluating: bool = False):
        return self.TEST_DATA_PATH if is_evaluating else self.train_data_path

    def batch_size(self, is_evaluating: bool = False):
        return (
            self.TEST_BATCH_SIZE if is_evaluating else self.TRAIN_BATCH_SIZE
        )  # take min with NUM_TRAIN_EXAMPLES?

    @property
    def train_data_path(self) -> Optional[str]:
        if not self.is_training:
            return None
        return "{}.train.c2v".format(self.TRAIN_DATA_PATH_PREFIX)

    @property
    def word_freq_dict_path(self) -> Optional[str]:
        if not self.is_training:
            return None
        return "{}.dict.c2v".format(self.TRAIN_DATA_PATH_PREFIX)

    @classmethod
    def get_vocabularies_path_from_model_path(cls, model_file_path: str) -> str:
        vocabularies_save_file_name = "dictionaries.bin"
        return "/".join(model_file_path.split("/")[:-1] + [vocabularies_save_file_name])

    @classmethod
    def get_entire_model_path(cls, model_path: str) -> str:
        return model_path + "__entire-model"

    @classmethod
    def get_model_weights_path(cls, model_path: str) -> str:
        return model_path + "__only-weights"

    @property
    def model_load_dir(self):
        return "/".join(self.MODEL_LOAD_PATH.split("/")[:-1])

    @property
    def entire_model_load_path(self) -> Optional[str]:
        if not self.is_loading:
            return None
        return self.get_entire_model_path(self.MODEL_LOAD_PATH)

    @property
    def model_weights_load_path(self) -> Optional[str]:
        if not self.is_loading:
            return None
        return self.get_model_weights_path(self.MODEL_LOAD_PATH)

    @property
    def entire_model_save_path(self) -> Optional[str]:
        if not self.is_saving:
            return None
        return self.get_entire_model_path(self.MODEL_SAVE_PATH)

    @property
    def model_weights_save_path(self) -> Optional[str]:
        if not self.is_saving:
            return None
        return self.get_model_weights_path(self.MODEL_SAVE_PATH)

    def verify(self):
        if not self.is_training and not self.is_loading:
            raise ValueError("Must train or load a model.")
        if self.is_loading and not os.path.isdir(self.model_load_dir):
            raise ValueError(
                "Model load dir `{model_load_dir}` does not exist.".format(
                    model_load_dir=self.model_load_dir
                )
            )
        if self.DL_FRAMEWORK not in {"tensorflow", "keras"}:
            raise ValueError("config.DL_FRAMEWORK must be in {'tensorflow', 'keras'}.")

    def __iter__(self):
        for attr_name in dir(self):
            if attr_name.startswith("__"):
                continue
            try:
                attr_value = getattr(self, attr_name, None)
            except:
                attr_value = None
            if callable(attr_value):
                continue
            yield attr_name, attr_value

    def get_logger(self) -> logging.Logger:
        if self.__logger is None:
            self.__logger = logging.getLogger("code2vec")
            self.__logger.setLevel(logging.INFO)
            self.__logger.handlers = []
            self.__logger.propagate = 0

            formatter = logging.Formatter("%(asctime)s %(levelname)-8s %(message)s")

            if self.VERBOSE_MODE >= 1:
                ch = logging.StreamHandler(sys.stdout)
                ch.setLevel(logging.INFO)
                ch.setFormatter(formatter)
                self.__logger.addHandler(ch)

            if self.LOGS_PATH:
                fh = logging.FileHandler(self.LOGS_PATH)
                fh.setLevel(logging.INFO)
                fh.setFormatter(formatter)
                self.__logger.addHandler(fh)

        return self.__logger

    def log(self, msg):
        self.get_logger().info(msg)
