import pandas as pd
from constants import TableHeaders, table_columns, UnitAmenitiesDict, BuildingAmenitiesDict
import collections
import re

MINIMUM_SQFT_THRESHOLD = 200

df = pd.read_excel('rental_listings.xlsx')

cleaned_list = []

cleaned_df = pd.DataFrame(columns=table_columns)

amentities_count = {}

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
        
        unit_amenities_dict = UnitAmenitiesDict 
        building_amenities_dict = BuildingAmenitiesDict 

        if not pd.isna(unit_amenities_value):
            unit_amenities_value = unit_amenities_value.strip().split(',')
            for amenity in unit_amenities_value:
                amenity = amenity.strip()
                if amenity in unit_amenities_dict.keys():
                    unit_amenities_dict[amenity] = 1

        if not pd.isna(building_amenities_value):
            building_amenities_value = building_amenities_value.strip().split(',')
            for amenity in building_amenities_value:
                amenity = amenity.strip()
                if amenity in building_amenities_dict.keys():
                    building_amenities_dict[amenity] = 1
        
        cleaned_list.append(
            {
                TableHeaders.BUILDING.value: building_value,
                TableHeaders.ADDRESS.value: address_value,
                TableHeaders.LISTING.value: listing_value,
                TableHeaders.BED.value: 1,
                TableHeaders.BATH.value: 1,
                TableHeaders.SQFT.value: 1,
                TableHeaders.PRICE.value: 1,
                TableHeaders.UNIT_AMENITIES.value: 1,
                TableHeaders.BUILDING_AMENITIES.value: 1,
                TableHeaders.PETS.value: 1,
                TableHeaders.LAT.value: 1,
                TableHeaders.LON.value: 1
            }
        )

print(cleaned_list)