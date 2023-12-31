import pandas as pd
from sqlalchemy.orm import Session

from backend.pydantic_schemas.Building import BuildingCreate, Building
from backend.pydantic_schemas.Unit import UnitCreate, Unit
from backend.db_models import Building

from backend.dependencies import get_db
from data.data_cleaner import get_cleaned_df
from constants import TableHeaders, UnitAmenities, BuildingAmenities

def add_unit_to_db(row, building_id: int, db: Session):
    unit = UnitCreate(
        buidling_id=building_id,
        bed=row[TableHeaders.BED.value],
        bath=row[TableHeaders.BATH.value],
        sqft=row[TableHeaders.SQFT.value],
        price=row[TableHeaders.PRICE.value],
        air_conditioning=row[UnitAmenities.AIR_CONDITIONING.value],
        balcony=row[UnitAmenities.BALCONY.value],
        furnished=row[UnitAmenities.FURNISHED.value],
        hardwood_floor=row[UnitAmenities.HARDWOOD_FLOOR.value],
        high_ceilings=row[UnitAmenities.HIGH_CEILINGS.value],
        in_unit_laundry=row[UnitAmenities.IN_UNIT_LAUNDRY.value]
    )
    create_unit(db, unit)


def add_listing_data_to_db(db: Session, df: pd.DataFrame):
    
    # Group listings by building and add individual building followed by associated units
    building_groups = df.groupby(TableHeaders.BUILDING.value)

    for building_name, building_df in building_groups:
        first_row = building_df.iloc[0]
        current_building = BuildingCreate(
            name=building_name,
            address=first_row[TableHeaders.ADDRESS.value],
            city=first_row[TableHeaders.CITY.value],
            lat=first_row[TableHeaders.LAT.value],
            lon=first_row[TableHeaders.LON.value],
            controlled_access=first_row[BuildingAmenities.CONTROLLED_ACCESS.value],
            fitness_center=first_row[BuildingAmenities.FITNESS_CENTER.value],
            outdoor_space=first_row[BuildingAmenities.OUTDOOR_SPACE.value],
            residents_lounge=first_row[BuildingAmenities.RESIDENTS_LOUNGE.value],
            roof_deck=first_row[BuildingAmenities.ROOF_DECK.value],
            storage=first_row[BuildingAmenities.STORAGE.value],
            swimming_pool=first_row[BuildingAmenities.SWIMMING_POOL.value],
            pets=first_row[TableHeaders.PETS.value]
        )

        current_building = create_building(db, current_building)

        for _, row in building_df.iterrows():
            unit = UnitCreate(
                buidling_id=current_building.id,
                bed=row[TableHeaders.BED.value],
                bath=row[TableHeaders.BATH.value],
                sqft=row[TableHeaders.SQFT.value],
                price=row[TableHeaders.PRICE.value],
                air_conditioning=row[UnitAmenities.AIR_CONDITIONING.value],
                balcony=row[UnitAmenities.BALCONY.value],
                furnished=row[UnitAmenities.FURNISHED.value],
                hardwood_floor=row[UnitAmenities.HARDWOOD_FLOOR.value],
                high_ceilings=row[UnitAmenities.HIGH_CEILINGS.value],
                in_unit_laundry=row[UnitAmenities.IN_UNIT_LAUNDRY.value]
            )
            create_unit(db, unit)


def create_building(db: Session, building: BuildingCreate) -> Building:
    db_building = Building(**building.model_dump())
    db.add(db_building)
    db.commit()
    db.refresh(db_building)
    return db_building


def create_unit(db: Session, unit: UnitCreate) -> Unit:
    db_unit = Building(**unit.model_dump())
    db.add(db_unit)
    db.commit()
    db.refresh(db_unit)
    return db_unit


add_listing_data_to_db(get_db(), get_cleaned_df())