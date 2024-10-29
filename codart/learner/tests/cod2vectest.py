import json

from codart.learner.cod2vec.interactive_predictor import InteractivePredictor


ip = InteractivePredictor(database_path=, model=)
predicts = ip.predict()

print(json.dump(predicts, indent=4))