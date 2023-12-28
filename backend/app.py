from fastapi import FastAPI

from routers import predict
from routers import analysis

app = FastAPI()

app.include_router(predict.router)
app.include_router(analysis.router)
