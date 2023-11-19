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
padmapper_full_url = f'{padmapper_base_url}/apartments/toronto-on/?box=-79.398227,43.639738,-79.3885277,43.6461182'
padmapper_scraper = PadmapperScraper(padmapper_base_url, padmapper_full_url)

# Collect rental listing URLs from main page to scrape
padmapper_scraper.fetch_rental_listing_urls(session, driver)
# Scrape page content of collected URLs to get rental listing data 
padmapper_scraper.get_all_rental_listings_data(driver)
# Append data rows to all_listings
all_listings += padmapper_scraper.listings

# ------------------------------------------------------------

# Convert the listings to a DataFrame
all_listings_df = pd.DataFrame(all_listings, columns=table_columns)

# Save DataFrame to Excel
all_listings_df.to_excel('rental_listings.xlsx', index=False)

# Close the driver
driver.quit()

