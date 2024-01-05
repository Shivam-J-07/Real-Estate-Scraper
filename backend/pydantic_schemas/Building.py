from pydantic import BaseModel
from pydantic_schemas.Unit import Unit


class BuildingBase(BaseModel):
    name: str
    city: str
    address: str
    pets: bool = False
    lat: float
    lon: float
    controlled_access: bool = False
    fitness_center: bool = False
    outdoor_space: bool = False
    residents_lounge: bool = False
    roof_deck: bool = False
    storage: bool = False
    swimming_pool: bool = False


class BuildingCreate(BuildingBase):
    pass


class Building(BuildingBase):
    id: int
    units: list[Unit]

    class Config:
        from_attributes = True
