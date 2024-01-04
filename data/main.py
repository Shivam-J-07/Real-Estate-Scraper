
import os

from constants import (
    table_columns, TableHeaders
)

from data.configs import (
    create_chrome_driver
)

from data.scrapers import PadmapperScraper

from selenium.webdriver.chrome.webdriver import WebDriver

import pandas as pd

from datetime import datetime

# Webdriver --------------------------------------------------

# Initialize WebDriver for retrieving rental listings from landing page
fetch_rental_listings_driver: WebDriver = create_chrome_driver(debugging_port=9222)

current_dir = os.path.dirname(os.path.realpath(__file__))
listings_path = os.path.join(current_dir, "rental_listings.xlsx")

# Padmapper --------------------------------------------------

padmapper_base_url = 'https://www.padmapper.com'
padmapper_complete_urls = [
    f'{padmapper_base_url}/apartments/toronto-on',
    f'{padmapper_base_url}/apartments/vancouver-bc',
    f'{padmapper_base_url}/apartments/winnipeg-mb',
    f'{padmapper_base_url}/apartments/edmonton-ab',
    f'{padmapper_base_url}/apartments/montreal-qc',
]
padmapper_scraper = PadmapperScraper(padmapper_base_url, padmapper_complete_urls)

# Collect rental listing URLs from main page to scrape

padmapper_scraper.fetch_rental_listing_urls(fetch_rental_listings_driver)

# Close the fetch_rental_listing_driver
fetch_rental_listings_driver.quit()

# Initialize WebDriver for extracting data from every rental listing
get_rental_data_driver: WebDriver = create_chrome_driver(debugging_port=9223)

# Log all extracted listings to a txt file for data permanence
with open('listings.txt', 'w') as file:
    file.write('\n'.join(padmapper_scraper.urls))

all_units_df = pd.DataFrame(columns=table_columns)
current_units = []
all_units = []

# Scrape page content of collected URLs to get rental listing data 
for url in padmapper_scraper.urls:
    try:
        # on every 100 listings read, write them to the excel sheet (in case of crash)
        if len(current_units) >= 100:
            all_units += current_units
            # current_df = pd.DataFrame(current_units, columns=table_columns)
            # all_units_df = pd.concat([all_units_df, current_df], ignore_index=True)
            all_units_df = pd.DataFrame(all_units, columns=table_columns)
            all_units_df.to_excel(listings_path, index=False)
            current_units.clear()
        rental_listing_data = padmapper_scraper.get_rental_listing_data(get_rental_data_driver, url)
        # print(rental_listing_data[0][TableHeaders.CITY.value])
        # print(table_columns)
        if rental_listing_data:
            current_units += rental_listing_data
    except:
        continue

# Append remaining padmapper listings to all_units
all_units += current_units

# ------------------------------------------------------------

all_units_df: pd.DataFrame = pd.DataFrame(all_units, columns=table_columns)

all_units_df[TableHeaders.DATE.value] = all_units_df[TableHeaders.DATE.value].fillna(datetime.now())

all_units_df.to_excel(listings_path, index=False)

# Close the get_rental_data_driver
get_rental_data_driver.quit()

# -------------------------------------------------------------