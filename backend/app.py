from fastapi import FastAPI

from backend import db_models
from backend.database import engine
from backend.routers import predict
from backend.routers import analysis

db_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(predict.router)
app.include_router(analysis.router)
