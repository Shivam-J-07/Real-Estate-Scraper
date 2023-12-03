import pandas as pd
from constants import TableHeaders, table_columns, UnitAmenitiesDict, BuildingAmenitiesDict
import collections
import re

MINIMUM_SQFT_THRESHOLD = 200

def get_cleaned_data():
    df = pd.read_excel('rental_listings.xlsx')
    cleaned_list = []
    for index, row in df.iterrows():
        building_value = row[TableHeaders.BUILDING.value] if not pd.isna(row[TableHeaders.BUILDING.value]) else ""
        address_value = row[TableHeaders.ADDRESS.value] if not pd.isna(row[TableHeaders.ADDRESS.value]) else ""
        listing_value = row[TableHeaders.LISTING.value] if not pd.isna(row[TableHeaders.LISTING.value]) else ""
        bed_value = row[TableHeaders.BED.value].lower()
        bath_value = row[TableHeaders.BATH.value]
        sqft_value = row[TableHeaders.SQFT.value]
        price_value = row[TableHeaders.PRICE.value]
        unit_amenities_value = row[TableHeaders.UNIT_AMENITIES.value]
        building_amenities_value = row[TableHeaders.BUILDING_AMENITIES.value]
        pets_value = row[TableHeaders.PETS.value]
        longitude_value = row[TableHeaders.LON.value]
        latitude_value = row[TableHeaders.LAT.value]

        if 'bedroom' in bed_value or ('studio' in bed_value and 'room' not in bed_value):
            try:
                bed_value = int(bed_value.split(' ')[0])
            except ValueError:
                if 'studio' in bed_value :
                    bed_value = 0
                else:
                    continue
            
            if not pd.isna(bath_value) and not '0' in bath_value:
                if ',' in bath_value:
                    [full_bath,  half_bath] = bath_value.split(',')
                    bath_value = int(full_bath.strip().split(' ')[0]) + 0.5 * (int(half_bath.strip().split(' ')[0]))
                else:
                    bath_value = int(bath_value.strip().split(' ')[0])
            else:
                continue

            if not pd.isna(sqft_value) and re.search(r'\d', sqft_value) is not None:
                sqft_value = int(sqft_value.replace(',', '').split(' ')[0])
                if not sqft_value >= MINIMUM_SQFT_THRESHOLD:
                    continue
            else:
                continue
            
            if not pd.isna(price_value):
                price_value = price_value.replace('$', '').replace(',','')
                if '—' in price_value:
                    price_value = price_value.split('—')[-1]
                try:
                    price_value = int(price_value)
                except ValueError:
                    continue
            else:
                continue
            
            unit_amenities_dict = UnitAmenitiesDict.copy() 
            building_amenities_dict = BuildingAmenitiesDict.copy() 

            if not pd.isna(unit_amenities_value):
                unit_amenities_value = unit_amenities_value.strip().split(',')
                for amenity in unit_amenities_value:
                    amenity = amenity.strip()
                    if unit_amenities_dict.get(amenity, None) is not None:
                        unit_amenities_dict[amenity] = 1

            if not pd.isna(building_amenities_value):
                building_amenities_value = building_amenities_value.strip().split(',')
                for amenity in building_amenities_value:
                    amenity = amenity.strip()
                    if building_amenities_dict.get(amenity, None) is not None:
                        building_amenities_dict[amenity] = 1
            
            if not pd.isna(pets_value):
                if 'dog' or 'cat' or 'yes' in pets_value.lower():
                    pets_value = 1
                else:
                    pets_value = 0
            else:
                continue
            
            cleaned_list.append(
                {
                    TableHeaders.BUILDING.value: building_value,
                    TableHeaders.ADDRESS.value: address_value,
                    TableHeaders.LISTING.value: listing_value,
                    TableHeaders.BED.value: bed_value,
                    TableHeaders.BATH.value: bath_value,
                    TableHeaders.SQFT.value: sqft_value,
                    TableHeaders.PRICE.value: price_value,
                    TableHeaders.UNIT_AMENITIES.value: unit_amenities_dict,
                    TableHeaders.BUILDING_AMENITIES.value: building_amenities_dict,
                    TableHeaders.PETS.value: pets_value,
                    TableHeaders.LAT.value: latitude_value,
                    TableHeaders.LON.value: longitude_value
                }
            )

    return cleaned_list

def flatten_data(data: list[dict])->list:
    '''Flattens amenity data from being a single cell to multiple individual cells'''
    flattened_data = []
    for entry in data:
        flattened_entry = entry.copy()  # Create a copy of the entry
        for key, value in entry.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    flattened_entry[sub_key] = sub_value
        # Remove the original nested dictionary keys
        flattened_entry.pop('Unit Amenities', None)
        flattened_entry.pop('Building Amenities', None)
        flattened_data.append(flattened_entry)
    return flattened_data