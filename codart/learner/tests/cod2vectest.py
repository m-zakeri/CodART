import json

from codart.learner.tests.interactive_predict import InteractivePredictor
from codart.learner.tests.tensorflow_model import Code2VecModel
from codart.learner.tests.config import Config

ip = InteractivePredictor(database_path="/home/y/jflex/jflex.und", model=Code2VecModel(config=Config()))
predicts = ip.predict()

print(json.dump(predicts, indent=4))