from fastapi import APIRouter, Depends, HTTPException
import pandas as pd
from sqlalchemy.orm import Session
from services.create import add_listing_data_to_db
from dependencies import get_db
from pydantic_schemas.Analysis import AddListing

router = APIRouter(
    prefix="/analysis",
    tags=["analysis"],
    responses={404: {"description": "Not found"}},
)


@router.get("")
def get_analysis():
    return {"data": {}}


@router.post("", status_code=201)
def add_listings(request: list[AddListing], db: Session = Depends(get_db)):
    df = pd.DataFrame([obj.dict() for obj in request])
    df.columns = df.columns.str.replace('_', ' ').str.title()
    df = df.rename(columns={'Sqft': 'SqFt'})
    try:
        add_listing_data_to_db(db, df)
        return {"message": "Database updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error occurred")
