import requests
from constants import table_columns
from scrapers import PadmapperScraper

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions

import pandas as pd

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Create a session object
session = requests.Session()

# Generate a random user agent
user_agent = UserAgent().random

# Access the WebDriver path from the environment variable
chrome_driver_path = os.getenv('CHROMEDRIVER_PATH')

# Set up Chrome options (optional, for additional configurations)
chrome_options = ChromeOptions()
chrome_options.add_argument(f'user-agent={user_agent}')

# Set up Chrome service
chrome_service = ChromeService(executable_path=chrome_driver_path)

# Initialize Chrome WebDriver with the service
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

all_listings = []
lat_lon_bounding_box = []

# Padmapper --------------------------------------------------

padmapper_base_url = 'https://www.padmapper.com'
padmapper_full_url = f'{padmapper_base_url}/apartments/vancouver-bc/'
padmapper_scraper = PadmapperScraper(padmapper_base_url, padmapper_full_url)

# Collect rental listing URLs from main page to scrape
padmapper_scraper.fetch_rental_listing_urls(session, driver)

padmapper_listings = []
# Scrape page content of collected URLs to get rental listing data 
for url in padmapper_scraper.urls:
    try:
        if len(padmapper_listings) == 100:
            # on every 100 listings read, write them to the excel sheet (in case of crash)
            all_listings += padmapper_listings
            current_df = pd.DataFrame(padmapper_listings, columns=table_columns)
            all_listings_df = pd.concat([all_listings_df, current_df], ignore_index=True)
            all_listings_df.to_excel('rental_listings.xlsx', index=False)
            padmapper_listings.clear()
        padmapper_listings.append(padmapper_scraper.get_rental_listing(url))
    except:
        continue

# Append remaining padmapper listings to all_listings
all_listings += padmapper_listings

# ------------------------------------------------------------

current_df = pd.DataFrame(padmapper_listings, columns=table_columns)
all_listings_df = pd.concat([all_listings_df, current_df], ignore_index=True)
all_listings_df.to_excel('rental_listings.xlsx', index=False)

# Close the driver
driver.quit()

