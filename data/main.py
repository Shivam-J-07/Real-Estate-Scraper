
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

PADMAPPER_BASE_URL = "https://www.padmapper.com"

def extract_raw_data(filepath: str, listing_urls: list[str]) -> pd.DataFrame:
    extracted_listing_data = []

    for listing_url in listing_urls:
        # Initialize WebDriver for retrieving rental listings from landing page
        fetch_rental_listings_driver: WebDriver = create_chrome_driver(debugging_port=9222) 
        padmapper_scraper = PadmapperScraper(PADMAPPER_BASE_URL, [listing_url])
        padmapper_scraper.fetch_rental_listing_urls(fetch_rental_listings_driver)

        # Close the fetch_rental_listing_driver
        fetch_rental_listings_driver.quit()

        # Initialize WebDriver for extracting data from every rental listing
        get_rental_data_driver: WebDriver = create_chrome_driver(debugging_port=9223)

        # Log all extracted listings to a txt file for data permanence
        with open('listings.txt', 'a') as file:
            file.write('\n'.join(padmapper_scraper.urls))
        
        current_100_units = []
        current_city_units = []

        # Scrape page content of collected URLs to get rental listing data 
        for url in padmapper_scraper.urls:
            try:
                # on every 100 listings read, write them to the excel sheet (in case of crash)
                if len(current_100_units) >= 100:
                    current_city_units += current_100_units
                    extracted_listing_data += current_city_units
                    extracted_listing_data_df = pd.DataFrame(extracted_listing_data, columns=table_columns)
                    extracted_listing_data_df.to_excel(filepath, index=False)
                    current_100_units.clear()
                rental_listing_data = padmapper_scraper.get_rental_listing_data(get_rental_data_driver, url)
                if rental_listing_data:
                    current_100_units += rental_listing_data
            except:
                continue

        # Append remaining padmapper listings to all_units
        extracted_listing_data += current_100_units

        extracted_listing_data_df = pd.DataFrame(extracted_listing_data, columns=table_columns)

        extracted_listing_data_df.to_excel(filepath, index=False)

        # Close the get_rental_data_driver
        get_rental_data_driver.quit()

    extracted_listing_data_df[TableHeaders.DATE.value].fillna(datetime.now(), inplace=True)

    extracted_listing_data_df.to_excel(filepath, index=False)

    return extracted_listing_data_df