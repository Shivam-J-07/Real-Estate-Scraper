from fastapi import FastAPI

from backend.database import engine, Base
from backend.routers import predict
from backend.routers import analysis
from backend.db_models import Building, Unit


Base.metadata.drop_all(bind=engine,tables=[Unit.__table__, Building.__table__])
Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(predict.router)
app.include_router(analysis.router)
