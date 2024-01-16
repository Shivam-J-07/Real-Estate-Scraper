from pydantic import BaseModel
from datetime import datetime

class AddListing(BaseModel):
    building: str
    neighbourhood: str
    address: str
    city: str
    listing: str
    bed: int
    bath: float
    sqft: float
    price: float
    pets: bool
    latitude: float
    longitude: float
    date: datetime
    controlled_access: bool
    fitness_center: bool
    outdoor_space: bool
    residents_lounge: bool
    roof_deck: bool
    storage: bool
    swimming_pool: bool
    air_conditioning: bool
    balcony: bool
    furnished: bool
    hardwood_floor: bool
    high_ceilings: bool
    in_unit_laundry: bool
