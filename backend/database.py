import os
import sys

parent_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(parent_dir)

sys.path.append(root_dir)
sys.path.append(parent_dir)

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from model.classes import convert_df_to_classes

SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# class Unit():
#     bed: int
#     bath: int
#     sqft: float
#     pets: bool = False
#     lat: float
#     lon: float
#     controlled_access: bool = False
#     fitness_center: bool = False
#     outdoor_space: bool = False
#     residents_lounge: bool = False
#     roof_deck: bool = False
#     storage: bool = False
#     swimming_pool: bool = False
#     air_conditioning: bool = False
#     balcony: bool = False
#     furnished: bool = False
#     hardwood_floor: bool = False
#     high_ceilings: bool = False
#     in_unit_laundry: bool = False
