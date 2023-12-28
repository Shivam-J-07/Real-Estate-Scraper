from fastapi import APIRouter
import joblib
import numpy
from models import Predict

router = APIRouter(
    prefix="/predict",
    tags=["predict"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
def get_prediction(request: Predict.PredictRequestBody):
    model = joblib.load("random_forest_model.joblib")
    input = numpy.array(
        [
            request.bed,
            request.bath,
            request.sqft,
            request.pets,
            request.lat,
            request.lon,
            request.controlled_access,
            request.fitness_center,
            request.outdoor_space,
            request.residents_lounge,
            request.roof_deck,
            request.storage,
            request.swimming_pool,
            request.air_conditioning,
            request.balcony,
            request.furnished,
            request.hardwood_floor,
            request.high_ceilings,
            request.in_unit_laundry,
        ]
    ).reshape(1, -1)
    prediction = model.predict(input)

    return {"price_prediction": str(prediction[0])}
