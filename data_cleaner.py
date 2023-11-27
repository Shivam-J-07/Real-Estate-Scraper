import pandas as pd
from constants import TableHeaders, table_columns
import collections

df = pd.read_excel('rental_listings.xlsx')

cleaned_df = pd.DataFrame(columns=table_columns)

for index, row in df.iterrows():
    # bed_values = df[TableHeaders.BED.value].unique()
    bed_value = row[TableHeaders.BED.value].lower()
    bath_value = row[TableHeaders.BATH.value]
    sqft_value = row[TableHeaders.SQFT.value]
    price_value = row[TableHeaders.PRICE.value]
    unit_amenities_value = row[TableHeaders.UNIT_AMENITIES.value]
    building_amenities_value = row[TableHeaders.BUILDING_AMENITIES.value]

    if not 'room' in bed_value:
        try:
            bed_value = int(bed_value.split(' ')[0])
        except ValueError:
            if 'studio' in bed_value :
                bed_value = 0
            else:
                continue
        
        print(bed_value)
        