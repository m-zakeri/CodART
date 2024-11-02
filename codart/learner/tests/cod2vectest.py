import json
from multiprocessing import Process
from codart.learner.tests.interactive_predict import InteractivePredictor
from codart.learner.tests.tensorflow_model import Code2VecModel
from codart.learner.tests.config import Config
from codart.learner.tests.run_java import run_java_extractor


def start_java_extractor():
    run_java_extractor()


def start_prediction():
    ip = InteractivePredictor(
        database_path="/home/y/jflex/jflex.und", model=Code2VecModel(config=Config())
    )
    # Run the prediction and print results
    predicts = ip.predict()
    print(json.dumps(predicts, indent=4))


# java_process = Process(target=start_java_extractor)
predict_process = Process(target=start_prediction)
# java_process.start()
predict_process.start()
# java_process.join()
predict_process.join()
