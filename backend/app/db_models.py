from app.database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


class Unit(Base):
    __tablename__ = "units"
    id = Column(Integer, primary_key=True, index=True,
                autoincrement=True, unique=True)
    building_id = Column(Integer, ForeignKey("buildings.id"))
    bed = Column(Integer, index=True)
    bath = Column(Float)
    sqft = Column(Float)
    price = Column(Float)
    air_conditioning = Column(Boolean, default=False)
    balcony = Column(Boolean, default=False)
    furnished = Column(Boolean, default=False)
    hardwood_floor = Column(Boolean, default=False)
    high_ceilings = Column(Boolean, default=False)
    in_unit_laundry = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.now())

    building = relationship("Building", back_populates="units")


class Building(Base):
    __tablename__ = "buildings"
    id = Column(Integer, primary_key=True, index=True,
                autoincrement=True, unique=True)
    name = Column(String, index=True)
    address = Column(String, index=True)
    neighbourhood = Column(String, index=True)
    city = Column(String, index=True)
    lat = Column(Float, primary_key=True)
    lon = Column(Float, primary_key=True)
    controlled_access = Column(Boolean, default=False)
    fitness_center = Column(Boolean, default=False)
    outdoor_space = Column(Boolean, default=False)
    residents_lounge = Column(Boolean, default=False)
    roof_deck = Column(Boolean, default=False)
    storage = Column(Boolean, default=False)
    swimming_pool = Column(Boolean, default=False)
    pets = Column(Boolean, default=False)

    units = relationship("Unit", back_populates="building")
