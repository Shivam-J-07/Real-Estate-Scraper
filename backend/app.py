from fastapi import FastAPI

from backend.database import engine, Base
from backend.routers import predict
from backend.routers import analysis


Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(predict.router)
app.include_router(analysis.router)
