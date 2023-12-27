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
