from datetime import datetime
import pandas as pd
from sqlalchemy.orm import Session

from db_models import Building, Unit


def get_building_by_name(db: Session, name: str):
    return db.query(Building).filter_by(name=name).first()


def get_building_by_lat_lon(db: Session, lat: float, lon: float):
    return db.query(Building).filter_by(lat=lat, lon=lon).first()


def get_building_units_by_timestamp(db: Session, building_id: int, timestamp: datetime):
    return db.query(Unit).filter_by(building_id=building_id, timestamp=timestamp)
