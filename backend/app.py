from fastapi import FastAPI

from backend.database import engine, Base, SessionLocal
from backend.routers import predict
from backend.routers import analysis

# Create a session
session = SessionLocal()

# Clear all data from tables associated with the Base
Base.metadata.drop_all(engine)

# Recreate tables after dropping them (if needed)
Base.metadata.create_all(engine)

# Commit changes and close the session
session.commit()
session.close()

app = FastAPI()

app.include_router(predict.router)
app.include_router(analysis.router)
