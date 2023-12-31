import pandas as pd
from sqlalchemy.orm import Session

from backend.pydantic_schemas.Building import Building as BuildingObj
from backend.db_models import Building


def get_building_by_name(db: Session, name: str) -> BuildingObj:
    return db.query(Building).filter_by(name=name).first()
