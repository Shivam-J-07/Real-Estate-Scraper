from pydantic import BaseModel

class UnitBase(BaseModel):
    building_id: int
    bed: int
    bath: float
    sqft: float
    price: float
    air_conditioning: bool = False
    balcony: bool = False
    furnished: bool = False
    hardwood_floor: bool = False
    high_ceilings: bool = False
    in_unit_laundry: bool = False


class UnitCreate(UnitBase):
    pass


class Unit(UnitBase):
    id: int

    class Config:
        from_attributes = True
