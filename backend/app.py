from typing import Union
from fastapi import FastAPI
import joblib
import numpy
from models import Predict

app = FastAPI()

@app.post("/predict")
def get_prediction(request: Predict.PredictRequestBody):
    model = joblib.load("random_forest_model.joblib")
    print(request)
    input = numpy.array([
        1.0000,    1.0000,  900.0000,    1.0000,   53.5510, -113.4975,
        1.0000,    0.0000,    0.0000,    0.0000,    0.0000,    1.0000,
        0.0000,    0.0000,    1.0000,    0.0000,    0.0000,    0.0000,
        0.0000
    ])
    input = input.reshape(1,-1)
    prediction = model.predict(input)

    return {
        "prediction": str(prediction[0])
    }
