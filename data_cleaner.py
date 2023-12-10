import pandas as pd
import re
from constants import TableHeaders, UnitAmenitiesDict, BuildingAmenitiesDict

MINIMUM_SQFT_THRESHOLD = 200

################## Parsing and validation functions #################
def parse_city_value(address_value):
    if pd.isna(address_value):
        return None
    cities = ["toronto", "edmonton"]
    return next((city for city in cities if city in address_value.lower()), None)

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
    price_value = price_value.replace('$', '').replace(',','')
    if '—' in price_value:
        price_value = price_value.split('—')[-1]
    try:
        return int(price_value)
    except ValueError:
        return None

def parse_amenities(amenities_value, amenities_dict):
    parsed_amenities = amenities_dict.copy()
    if not pd.isna(amenities_value):
        amenities_value = amenities_value.strip().split(',')
        for amenity in amenities_value:
            amenity = amenity.strip()
            if amenity in parsed_amenities:
                parsed_amenities[amenity] = 1
    return parsed_amenities

def parse_pets_value(pets_value):
    if pd.isna(pets_value):
        return 0
    pets_value = pets_value.lower()
    return 1 if any(pet in pets_value for pet in ['dog', 'cat', 'yes']) else 0

# Main function to process the data
def get_cleaned_data():
    df = pd.read_excel('rental_listings.xlsx')
    cleaned_list = []

    for _, row in df.iterrows():
        bed_value = parse_bed_value(row[TableHeaders.BED.value])
        bath_value = parse_bath_value(row[TableHeaders.BATH.value])
        sqft_value = parse_sqft_value(row[TableHeaders.SQFT.value])
        price_value = parse_price_value(row[TableHeaders.PRICE.value])
        unit_amenities = parse_amenities(row[TableHeaders.UNIT_AMENITIES.value], UnitAmenitiesDict)
        building_amenities = parse_amenities(row[TableHeaders.BUILDING_AMENITIES.value], BuildingAmenitiesDict)
        pets_value = parse_pets_value(row[TableHeaders.PETS.value])
        city_value = parse_city_value(row[TableHeaders.ADDRESS.value])

        if None in [bed_value, bath_value, sqft_value, price_value, city_value]:
            continue

        cleaned_list.append({
            TableHeaders.BUILDING.value: row[TableHeaders.BUILDING.value],
            TableHeaders.ADDRESS.value: row[TableHeaders.ADDRESS.value],
            TableHeaders.CITY.value: city_value,
            TableHeaders.LISTING.value: row[TableHeaders.LISTING.value],
            TableHeaders.BED.value: bed_value,
            TableHeaders.BATH.value: bath_value,
            TableHeaders.SQFT.value: sqft_value,
            TableHeaders.PRICE.value: price_value,
            TableHeaders.UNIT_AMENITIES.value: unit_amenities,
            TableHeaders.BUILDING_AMENITIES.value: building_amenities,
            TableHeaders.PETS.value: pets_value,
            TableHeaders.LAT.value: row[TableHeaders.LAT.value],
            TableHeaders.LON.value: row[TableHeaders.LON.value]
        })
    return cleaned_list

# Function to flatten data
def flatten_data(data):
    flattened_data = []
    for entry in data:
        flattened_entry = entry.copy()
        for key, value in entry.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    flattened_entry[sub_key] = sub_value
        flattened_entry.pop(TableHeaders.UNIT_AMENITIES.value, None)
        flattened_entry.pop(TableHeaders.BUILDING_AMENITIES.value, None)
        flattened_data.append(flattened_entry)
    return flattened_data
