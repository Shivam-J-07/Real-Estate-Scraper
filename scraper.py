import requests
from bs4 import BeautifulSoup
from utils import generate_time_gap, TableHeaders
from scrapers import BaseScraper, KijijiScraper, PadmapperScraper

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

# kijiji_base_url = 'https://www.kijiji.ca'
# kijiji_full_url = f'{kijiji_base_url}/b-for-rent/city-of-toronto/c30349001l1700273'
# kijiji_scraper = KijijiScraper(kijiji_base_url, kijiji_full_url)

padmapper_base_url = 'https://www.padmapper.com'
padmapper_full_url = f'{padmapper_base_url}/apartments/toronto-on?box=-79.4083115,43.6358027,-79.3986192,43.6422432'
padmapper_scraper = PadmapperScraper(padmapper_base_url, padmapper_full_url)

# for link in padmapper_scraper.scrape_page(session):
#     print(link)

urls = [
"https://www.padmapper.com/buildings/p368402/apartments-at-39-niagara-st-toronto-on-m5v-0t6",
"https://www.padmapper.com/buildings/p668941/newton-cityplace-6256-apartments-at-80-queens-wharf-rd-toronto-on-m5v-0j3",
"https://www.padmapper.com/buildings/p470812/the-lakefront-4095-apartments-at-17-bathurst-st-toronto-on-m5v-0n1",
"https://www.padmapper.com/buildings/p751811/the-residences-at-the-well-apartments-at-425-wellington-st-w-toronto-on-m5v-0v3"
]

listings = []

table_columns = [
    TableHeaders.BUILDING.value,
    TableHeaders.ADDRESS.value,
    TableHeaders.LISTING.value,
    TableHeaders.BED.value,
    TableHeaders.BATH.value,
    TableHeaders.SQFT.value,
    TableHeaders.PRICE.value,
    TableHeaders.UNIT_AMENITIES.value,
    TableHeaders.BUILDING_AMENITIES.value,
    TableHeaders.PETS.value
]

df = pd.DataFrame(columns=table_columns)

padmapper_scraper.scrape_all_links(driver)

# Convert the list of new rows to a DataFrame
df_extended = pd.DataFrame(padmapper_scraper.listings, columns=table_columns)

# Append to the DataFrame
df = pd.concat([df, df_extended], ignore_index=True)

# Save DataFrame to Excel
df.to_excel('rental_listings.xlsx', index=False)

# Close the driver
driver.quit()

# all_links = []

# # Number of pages to scrape
# num_pages = 2

# # Loop through the pages and scrape them
# for page_num in range(1, num_pages + 1):
#     page_url = f'{kijiji_base_url}?page={page_num}'
#     links = kijiji_scraper.scrape_page(session)
#     all_links.extend(links)
#     generate_time_gap()

# for link in all_links:
#     print(f'{kijiji_base_url}{link}')