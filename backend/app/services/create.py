import pandas as pd
from sqlalchemy.orm import Session

from app.constants import TableHeaders, UnitAmenities, BuildingAmenities
from app.db_models import Building, Unit
from app.services.search import get_building_units_by_timestamp, get_building_by_lat_lon
from app.services.delete import delete_units_by_timestamp



def row_to_building(row, db: Session) -> Building:
    building = get_building_by_lat_lon(
        db, lat=row[TableHeaders.LAT.value], lon=row[TableHeaders.LON.value])
    return Building(
        name=row[TableHeaders.BUILDING.value],
        address=row[TableHeaders.ADDRESS.value],
        city=row[TableHeaders.CITY.value],
        lat=row[TableHeaders.LAT.value],
        lon=row[TableHeaders.LON.value],
        controlled_access=row[BuildingAmenities.CONTROLLED_ACCESS.value],
        fitness_center=row[BuildingAmenities.FITNESS_CENTER.value],
        outdoor_space=row[BuildingAmenities.OUTDOOR_SPACE.value],
        residents_lounge=row[BuildingAmenities.RESIDENTS_LOUNGE.value],
        roof_deck=row[BuildingAmenities.ROOF_DECK.value],
        storage=row[BuildingAmenities.STORAGE.value],
        swimming_pool=row[BuildingAmenities.SWIMMING_POOL.value],
        pets=row[TableHeaders.PETS.value]
    ) if building is None else None


def row_to_unit(row, building_id) -> Unit:
    return Unit(
        building_id=building_id,
        bed=row[TableHeaders.BED.value],
        bath=row[TableHeaders.BATH.value],
        sqft=row[TableHeaders.SQFT.value],
        price=row[TableHeaders.PRICE.value],
        air_conditioning=row[UnitAmenities.AIR_CONDITIONING.value],
        balcony=row[UnitAmenities.BALCONY.value],
        furnished=row[UnitAmenities.FURNISHED.value],
        hardwood_floor=row[UnitAmenities.HARDWOOD_FLOOR.value],
        high_ceilings=row[UnitAmenities.HIGH_CEILINGS.value],
        in_unit_laundry=row[UnitAmenities.IN_UNIT_LAUNDRY.value],
        timestamp=row[TableHeaders.DATE.value].to_pydatetime()
    )


def add_listing_data_to_db(db: Session, df: pd.DataFrame):
    try:
        # First add all Building objects by getting all rows with a unique building and converting each to a Building object
        buildings = df.drop_duplicates(
            subset=[TableHeaders.LAT.value, TableHeaders.LON.value], keep='first').apply(row_to_building, args=(db,), axis=1).dropna()
        create_buildings(db, buildings)
        # Now add all Unit objects associated with each building
        building_groups = df.groupby(
            [TableHeaders.LAT.value, TableHeaders.LON.value])
        for (lat, lon), building_df in building_groups:
            building = get_building_by_lat_lon(db, lat=lat, lon=lon)
            timestamp = building_df[TableHeaders.DATE.value].iloc[0]
            existing_units = get_building_units_by_timestamp(
                db, building.id, building_df[TableHeaders.DATE.value].iloc[0]).first()
            if existing_units is not None:
                print(
                    f"Units for building {building.id} for timestamp {timestamp} already exist")
                continue
            units = building_df.apply(row_to_unit, args=(building.id,), axis=1)
            create_units(db, units, building.id)
    except Exception as e:
        print(
            f"An error occurred while adding listing data to the database, rolling back entries")
        # Delete all units for the current date timestamp
        timestamp = df[TableHeaders.DATE.value].iloc[0]
        delete_units_by_timestamp(db=db, timestamp=timestamp)
        raise e


def create_buildings(db: Session, buildings: list[Building]):
    db.bulk_save_objects(buildings)
    db.commit()
    print(f"Created buildings in db")


def create_units(db: Session, units: pd.DataFrame, building_id: int):
    db.bulk_save_objects(units)
    db.commit()
    print(f"Created units in db for building with id {building_id}")
