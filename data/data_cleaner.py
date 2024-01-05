import pandas as pd
import re
import os
from constants import TableHeaders, UnitAmenitiesDict, BuildingAmenitiesDict

MINIMUM_SQFT_THRESHOLD = 200

################## Parsing and validation functions #################

def parse_bed_value(bed_value):
    if pd.isna(bed_value):
        return None
    bed_value = bed_value.lower()
    if 'bedroom' in bed_value or ('studio' in bed_value and 'room' not in bed_value):
        try:
            return 0 if 'studio' in bed_value else int(bed_value.split(' ')[0])
        except (ValueError, IndexError):
            return None
    return None


def parse_bath_value(bath_value):
    if pd.isna(bath_value) or '0' in bath_value:
        return None
    try:
        if ',' in bath_value:
            full_bath, half_bath = bath_value.split(',')
            return int(full_bath.strip().split(' ')[0]) + 0.5 * int(half_bath.strip().split(' ')[0])
        return int(bath_value.strip().split(' ')[0])
    except (ValueError, IndexError):
        return None


def parse_sqft_value(sqft_value):
    if pd.isna(sqft_value) or re.search(r'\d', sqft_value) is None:
        return None
    sqft_value = int(sqft_value.replace(',', '').split(' ')[0])
    return sqft_value if sqft_value >= MINIMUM_SQFT_THRESHOLD else None


def parse_price_value(price_value):
    if pd.isna(price_value):
        return None
    price_value = price_value.replace('$', '').replace(',', '')
    if '—' in price_value:
        price_value = price_value.split('—')[-1]
    try:
        return int(price_value)
    except ValueError:
        return None


def parse_building_amenities(amenities_value):
    if not pd.isna(amenities_value):
        return [amenity.strip() for amenity in amenities_value.split(',') if amenity.strip() in BuildingAmenitiesDict]
    return None


def parse_unit_amenities(amenities_value):
    if not pd.isna(amenities_value):
        return [amenity.strip() for amenity in amenities_value.split(',') if amenity.strip() in UnitAmenitiesDict]
    return None


def parse_pets_value(pets_value):
    if pd.isna(pets_value):
        return 0
    pets_value = pets_value.lower()
    return 1 if any(pet in pets_value for pet in ['dog', 'cat', 'yes']) else 0

def get_raw_df(raw_filepath: str) -> pd.DataFrame:
    return pd.read_excel(raw_filepath)

def get_cleaned_df(raw_filepath: str, cleaned_filepath: str) -> pd.DataFrame:
    cleaned_df = get_cleaned_data(get_raw_df(raw_filepath))
    cleaned_df.to_excel(cleaned_filepath, index=False)
    return cleaned_df

# Main function to process the data
def get_cleaned_data(df):
    df[TableHeaders.BED.value] = df[TableHeaders.BED.value].apply(parse_bed_value)
    df[TableHeaders.BATH.value] = df[TableHeaders.BATH.value].apply(parse_bath_value)
    df[TableHeaders.SQFT.value] = df[TableHeaders.SQFT.value].apply(parse_sqft_value)
    df[TableHeaders.PRICE.value] = df[TableHeaders.PRICE.value].apply(parse_price_value)
    df[TableHeaders.PETS.value] = df[TableHeaders.PETS.value].apply(parse_pets_value)
    df[TableHeaders.BUILDING_AMENITIES.value] = df[TableHeaders.BUILDING_AMENITIES.value].apply(parse_building_amenities)
    df[TableHeaders.UNIT_AMENITIES.value] = df[TableHeaders.UNIT_AMENITIES.value].apply(parse_unit_amenities)
    # Flatten out the building amenities into one-hot encoded columns
    df_exploded = df.explode(TableHeaders.BUILDING_AMENITIES.value)
    dummies = pd.get_dummies(df_exploded, columns=[TableHeaders.BUILDING_AMENITIES.value], prefix='', prefix_sep='', dtype=int)
    df = dummies.groupby(dummies.index).max()

    # Flatten out the unit amenities into one-hot encoded columns
    df_exploded = df.explode(TableHeaders.UNIT_AMENITIES.value)
    dummies = pd.get_dummies(df_exploded, columns=[TableHeaders.UNIT_AMENITIES.value], prefix='', prefix_sep='', dtype=int)
    df = dummies.groupby(dummies.index).max()

    # List of columns to check for NaN values
    na_columns_to_drop = [TableHeaders.BUILDING.value, TableHeaders.CITY.value, TableHeaders.BED.value, TableHeaders.BATH.value, TableHeaders.SQFT.value, TableHeaders.PRICE.value]  # replace with your actual column names

    # Remove nulls
    df.dropna(subset=na_columns_to_drop, inplace=True)

    # Filter out listings with prices greater than $5K - these extreme values are outliers
    df = df[df[TableHeaders.PRICE.value] < 5000]

    return df