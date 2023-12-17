import requests
from constants import (
    table_columns,
)
from configs import (
    create_chrome_driver
)
from scrapers import PadmapperScraper

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.webdriver import WebDriver

import pandas as pd

import os

# Webdriver --------------------------------------------------

# Initialize WebDriver for retrieving rental listings from landing page
fetch_rental_listings_driver: WebDriver = create_chrome_driver(debugging_port=9222)

# Initialize WebDriver for extracting data from every rental listing
get_rental_data_driver: WebDriver = create_chrome_driver(debugging_port=9223)

current_dir = os.path.dirname(os.path.realpath(__file__))
listings_path = os.path.join(current_dir, "rental_listings.xlsx")

all_listings = []

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

with open('listings.txt', 'w') as file:
    file.write('\n'.join(padmapper_scraper.urls))

all_listings_df = pd.DataFrame(columns=table_columns)
padmapper_listings = []

urls_page = 1
# Scrape page content of collected URLs to get rental listing data 
for url in padmapper_scraper.urls:
    try:
        if len(padmapper_listings) >= 100:
            urls_page += 1
            all_listings += padmapper_listings
            current_df = pd.DataFrame(padmapper_listings, columns=table_columns)
            all_listings_df = pd.concat([all_listings_df, current_df], ignore_index=True)
            # on every 100 listings read, write them to the excel sheet (in case of crash)
            all_listings_df.to_excel(listings_path, index=False)
            padmapper_listings.clear()
        rental_listing_data = padmapper_scraper.get_rental_listing_data(get_rental_data_driver, url)
        if rental_listing_data:
            padmapper_listings += rental_listing_data
    except:
        continue

# Append remaining padmapper listings to all_listings
all_listings += padmapper_listings

# ------------------------------------------------------------

current_df = pd.DataFrame(padmapper_listings, columns=table_columns)
all_listings_df = pd.concat([all_listings_df, current_df], ignore_index=True)

all_listings_df.to_excel(listings_path, index=False)

# Close the fetch_rental_listing_driver
fetch_rental_listings_driver.quit()

# Close the get_rental_data_driver
get_rental_data_driver.quit()

# -------------------------------------------------------------

# List the blobs in the container
# print(f"Listing blobs in the container '{container_name}':")
# try:
#    blob_list = container_client.list_blobs()
#    for blob in blob_list:
#        print(blob.name)
# except Exception as e:
#    print(f"An error occurred while listing blobs: {e}")

 # Create the container if it doesn't exist

# upload_file_to_blob(listings_path, blob_name, container_client)