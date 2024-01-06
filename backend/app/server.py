from fastapi import FastAPI

from app.routers import predict
from app.routers import analysis

app = FastAPI()

app.include_router(predict.router)
app.include_router(analysis.router)
