from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import predict
from app.routers import analysis

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://rent-rite-hpcb.vercel.app/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict.router)
app.include_router(analysis.router)
