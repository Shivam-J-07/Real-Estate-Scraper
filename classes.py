import numpy as np
import pandas as pd
from constants import TableHeaders

class BedroomType:
    def __init__(self, bed: int, num_units: int, sqft: pd.Series, prices: pd.Series):
        self.bed = bed
        self.num_units = num_units
        self.sqft: np.array = np.array(sqft)
        self.price: np.array = np.array(prices)

class Building:
    def __init__(self, name, city):
        self.name = name
        self.city = city
        self.bedroom_types: dict[int, BedroomType] = {}
    
    def __str__(self):
        building_info = f"Building: {self.name}\n"
        building_info += f"Total Units: {self.num_units}\n"
        building_info += f"Overall Average SqFt: {np.mean(self.all_sqft_values):.2f}\n"
        building_info += f"Overall Average Price: {np.mean(self.all_prices_values):.2f}\n"
        building_info += f"Overall Price Per SqFt: {(np.mean(self.all_prices_values)/np.mean(self.all_sqft_values)):.2f}\n"
        building_info += "-----------------------------------\n"

        for bed, bedroom_type in self.bedroom_types.items():
            building_info += f"Bedroom Type: {bed} beds\n"
            building_info += f" - Units: {bedroom_type.num_units}\n"
            building_info += f" - Average SqFt: {np.mean(bedroom_type.sqft):.2f}\n"
            building_info += f" - Average Price: {np.mean(bedroom_type.price):.2f}\n"
            building_info += f" - Price per SqFt: {(np.mean(bedroom_type.price)/np.mean(bedroom_type.sqft)):.2f}\n"
            building_info += "-----------------------------------\n"

        return building_info

    def add_bedroom_type(self, bed, bed_df: pd.DataFrame):
        sqft_values: pd.Series = bed_df[TableHeaders.SQFT.value]
        prices_values: pd.Series = bed_df[TableHeaders.PRICE.value]
        num_units: int = len(bed_df)
        self.bedroom_types[bed] = BedroomType(bed, num_units, sqft_values, prices_values)

    @property
    def all_sqft_values(self):
        return np.concatenate([bedroom_type.sqft for bedroom_type in self.bedroom_types.values()])

    @property
    def all_prices_values(self):
        return np.concatenate([bedroom_type.price for bedroom_type in self.bedroom_types.values()])

    @property
    def num_units(self):
        return sum(bedroom_type.num_units for bedroom_type in self.bedroom_types.values())