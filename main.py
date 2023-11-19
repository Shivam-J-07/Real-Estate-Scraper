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

lat_lon_bounding_box = []

padmapper_base_url = 'https://www.padmapper.com'
padmapper_full_url = f'{padmapper_base_url}/apartments/toronto-on/?box=-79.398227,43.639738,-79.3885277,43.6461182'
padmapper_scraper = PadmapperScraper(padmapper_base_url, padmapper_full_url)

listings = []

df = pd.DataFrame(columns=table_columns)

padmapper_scraper.fetch_rental_listing_urls(session, driver)

padmapper_scraper.get_page_content_from_urls(driver)

# Convert the list of new rows to a DataFrame
df_extended = pd.DataFrame(padmapper_scraper.listings, columns=table_columns)

# Append to the DataFrame
df = pd.concat([df, df_extended], ignore_index=True)

# Save DataFrame to Excel
df.to_excel('rental_listings.xlsx', index=False)

# Close the driver
driver.quit()

