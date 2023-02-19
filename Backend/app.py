from flask import Flask, request
from flask_cors import CORS

import numpy as np
from tensorflow.keras import models

import json
import os


app = Flask(__name__)
CORS(app)

MODEL_PATH = os.path.abspath("./models/model_easy.h5")

model = models.load_model(MODEL_PATH)

@app.route("/move", methods=["POST"])
def bestMove():
    state = np.array(request.json.get("state")).reshape((3, 3))
    player = 0 + (np.sum(state==0) - np.sum(state==1))
    assert player in [0, 1]
    inputs = np.zeros((11,))
    inputs[:9] = state.flatten()
    inputs[9+player] = 1
    
    print(f"Predicting")
    prediction = list(model.predict(np.expand_dims(inputs, 0)).flatten())
    print(f"Prediction: {prediction}")
    prediction = prediction.index(max(prediction))
    return json.dumps((prediction//3, prediction%3))


if __name__ == "__main__":
    app.run(debug=True)
