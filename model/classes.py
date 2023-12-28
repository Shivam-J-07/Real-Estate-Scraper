import numpy as np
import pandas as pd
from constants import TableHeaders

class UnitType:
    def __init__(self, unit_type: int, num_units: int, sqft: pd.Series, prices: pd.Series):
        self.unit_type = unit_type
        self.num_units = num_units
        self.sqft: np.array = np.array(sqft)
        self.price: np.array = np.array(prices)

class Building:
    def __init__(self, name, city):
        self.name = name
        self.city = city
        self.unit_types: dict[int, UnitType] = {}
    
    def __str__(self):
        building_info = f"Building: {self.name}\n"
        building_info += f"Total Units: {self.num_units}\n"
        building_info += f"Overall Average SqFt: {np.mean(self.all_sqft_values):.2f}\n"
        building_info += f"Overall Average Price: {np.mean(self.all_prices_values):.2f}\n"
        building_info += f"Overall Price Per SqFt: {(np.mean(self.all_prices_values)/np.mean(self.all_sqft_values)):.2f}\n"
        building_info += "-----------------------------------\n"

        for bed, unit_type in self.unit_types.items():
            building_info += f"Bedroom Type: {bed} beds\n"
            building_info += f" - Units: {unit_type.num_units}\n"
            building_info += f" - Average SqFt: {np.mean(unit_type.sqft):.2f}\n"
            building_info += f" - Average Price: {np.mean(unit_type.price):.2f}\n"
            building_info += f" - Price per SqFt: {(np.mean(unit_type.price)/np.mean(unit_type.sqft)):.2f}\n"
            building_info += "-----------------------------------\n"

        return building_info

    def add_unit_type(self, unit_type, unit_type_df: pd.DataFrame):
        sqft_values: pd.Series = unit_type_df[TableHeaders.SQFT.value]
        prices_values: pd.Series = unit_type_df[TableHeaders.PRICE.value]
        num_units: int = len(unit_type_df)
        self.unit_types[unit_type] = UnitType(unit_type, num_units, sqft_values, prices_values)

    @property
    def all_sqft_values(self):
        return np.concatenate([unit_type.sqft for unit_type in self.unit_types.values()])

    @property
    def all_prices_values(self):
        return np.concatenate([unit_type.price for unit_type in self.unit_types.values()])

    @property
    def num_units(self):
        return sum(unit_type.num_units for unit_type in self.unit_types.values())

class City():
    def __init__(self, name: str):
        self.name = name
        self.buildings: list[Building] = []
    
    def add_building(self, building: Building):
        self.buildings.append(building)


def convert_df_to_classes(df: pd.DataFrame) -> list[City]:
    cities: list[City] = []

    # Group data by city to extract city specific insights
    city_groups = df.groupby(TableHeaders.CITY.value)

    for city_name, city_df in city_groups:
        current_city = City(city_name)
        # Group city data by building name to extract building specific insights
        building_groups = city_df.groupby(TableHeaders.BUILDING.value)

        # Create an intermediary tuple to record number of available units and sort buildings accordingly
        # When displaying overarching insights for an area, buildings with more units will be more informational
        buildings_tuples = [(building, building_df, len(building_df)) for building, building_df in building_groups]
        buildings_tuples.sort(key = lambda x: x[2], reverse=True)

        for building_name, building_df, num_units in buildings_tuples:

            current_building: Building = Building(building_name, city_name)
            # Group by bed type within this building
            bed_groups = building_df.groupby(TableHeaders.BED.value)
            for unit_type, unit_type_df in bed_groups:
                current_building.add_unit_type(unit_type=unit_type, unit_type_df=unit_type_df)

            current_city.add_building(current_building) 

        cities.append(current_city)

    return cities
