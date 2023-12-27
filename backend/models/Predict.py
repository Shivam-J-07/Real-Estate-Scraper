from pydantic import BaseModel

class PredictRequestBody(BaseModel):
    bed: int
    bath: int
    sqft: float
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
    air_conditioning: bool = False
    balcony: bool = False
    furnished: bool = False
    hardwood_floor: bool = False
    high_ceilings: bool = False
    in_unit_laundry: bool = False