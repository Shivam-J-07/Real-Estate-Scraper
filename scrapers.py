from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
from utils import (
    get_headers,
    get_absolute_url, 
    generate_time_gap, 
    TableHeaders,
    match_address, 
    match_pets
)

import re

class BaseScraper():
    def __init__(self, base_url="", full_url=""):
        self.base_url = base_url
        self.full_url = full_url
        self.links = [
            "https://www.padmapper.com/buildings/p368402/apartments-at-39-niagara-st-toronto-on-m5v-0t6#back=%2Fapartments%2Ftoronto-on",
            "https://www.padmapper.com/buildings/p751811/the-residences-at-the-well-apartments-at-425-wellington-st-w-toronto-on-m5v-0v3",
            "https://www.padmapper.com/buildings/p751811/the-residences-at-the-well-apartments-at-425-wellington-st-w-toronto-on-m5v-0v3#back=%2Fapartments%2Ftoronto-on%3Fbox%3D-79.44856%2C43.64122%2C-79.37927%2C43.68725"
            ]
        self.listings = []
    
    def make_request(self, session):
        response = session.get(self.full_url, headers=get_headers(self.base_url))
        if response.status_code != 200:
            raise Exception(f"Failed to fetch page at {self.full_url}. Status code: {response.status_code}")
        return response.text
    
class KijijiScraper(BaseScraper):
    def __init__(self, base_url="", full_url=""):
        super().__init__(base_url, full_url)

    def get_all_links(self, session):
        try:
            page_html_content = self.make_request(session)
            soup = BeautifulSoup(page_html_content, 'html.parser')
            self.links = [a['href'] for a in soup.find_all('a', {'data-testid': 'listing-link'})]
        except Exception as e:
            print(f"ERROR: {str(e)}")
    
    def scrape_all_links(self):
        for link in self.links:
            pass
            
class PadmapperScraper(BaseScraper):
    def __init__(self, base_url="", full_url=""):
        super().__init__(base_url, full_url)
    
    def get_all_links(self, session):
        try: 
            page_html_content = self.make_request(session)
            soup = BeautifulSoup(page_html_content, 'html.parser')
            
            # Find all 'a' tags with a class that includes 'ListItemFull_headerText'
            link_elements = soup.find_all('a', class_=lambda cls: cls and cls.startswith('ListItemFull_headerText'))
            
            # Extract href attributes and ensure they are absolute URLs
            self.links = [get_absolute_url(self.base_url, link.get('href')) for link in link_elements]
        except Exception as e:
            print(f"ERROR: {str(e)}")
            
    def scrape_all_links(self, web_driver):
        for link in self.links:
            web_driver.get(link)
            
            generate_time_gap()
            
            # Wait for elements to load and be clickable
            WebDriverWait(web_driver, 1000).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[class*='Floorplan_floorplanPanel']"))
            )
            dropdown_divs = web_driver.find_elements(By.CSS_SELECTOR, "div[class*='Floorplan_floorplanPanel']")
            
            for div in dropdown_divs:
                try:
                    # Scroll and click using Selenium built-in methods
                    web_driver.execute_script("arguments[0].scrollIntoView();", div)
                    # WebDriverWait(web_driver, 3000).until(EC.element_to_be_clickable(div)).click()
                    web_driver.execute_script("arguments[0].click();", div)
                    generate_time_gap()
                except Exception as e:
                    print("Error interacting with dropdown:", e)

            # Get the HTML content of the page
            link_html_content = web_driver.page_source
            self.scrape_link(link_html_content)
    
    def scrape_link(self, link_html_content):
        # Parse the HTML with Beautiful Soup
        soup = BeautifulSoup(link_html_content, 'html.parser')
        
        building_title = soup.find('h1', class_=lambda value: value and 'FullDetail_street_' in value)
        
        building_title_text = re.split(r'[^\w ]+',  building_title.get_text())[0] if building_title else ""
        
        amenities = soup.find_all('div', class_=lambda value: value and 'Amenities_header_' in value)
        
        unit_amenities = []
        building_amenities = []
        try:
            unit_amenities_header = amenities[0] if len(amenities) == 2 and "apartment" in amenities[0].get_text().lower() else ""
            building_amenities_header = amenities[1] if len(amenities) == 2 and "building" in amenities[1].get_text().lower() else ""
            unit_amenities_container = unit_amenities_header.find_parent('div') if unit_amenities_header else ""
            building_amenities_container = building_amenities_header.find_parent('div') if building_amenities_header else ""
            unit_amenities = unit_amenities_container.find_all('div', class_=lambda value: value and 'Amenities_text_' in value) if unit_amenities_container else []
            building_amenities = building_amenities_container.find_all('div', class_=lambda value: value and 'Amenities_text_' in value) if building_amenities_container else []
        except Exception as e:
            print("Error - Getting amenities: ", e)
            
        unit_amenities_text = ", ".join([amenity.get_text() for amenity in unit_amenities])  
        building_amenities_text = ", ".join([amenity.get_text() for amenity in building_amenities])  
        
        details = soup.find('div', class_=lambda value: value and 'SummaryTable_summaryTable_' in value)
        
        address_header = details.find(match_address)
        parent_address_li = address_header.find_parent('li')
        address_div = parent_address_li.find('div') if parent_address_li else None
        address_text = address_div.get_text().strip() if address_div else None
        
        pets_header = details.find(match_pets)
        parent_pets_li = pets_header.find_parent('li')
        pets_div = parent_pets_li.find('div') if parent_pets_li else None
        pets_text = pets_div.get_text().strip() if pets_div else None
        
        # Find all divs where class contains 'Floorplan_floorplan'
        data_elements = soup.find_all('div', class_=lambda value: value and 'Floorplan_floorplansContainer_' in value)
        
        for data_element in data_elements:
            current_floorplan = data_element.find('div', class_=lambda value: value and 'Floorplan_title_' in value)
            floorplan_title_text = current_floorplan.get_text().strip() if current_floorplan else ""
            
            unit_containers = data_element.find_all('div', class_=lambda value: value and 'Floorplan_floorplanDetailContainer_' in value)
            for unit_container in unit_containers:
                unit_title = unit_container.find('div', class_=lambda value: value and 'Floorplan_floorplanTitle' in value)
                unit_price = unit_container.find('div', class_=lambda value: value and 'Floorplan_floorplanPrice' in value)
                unit_sqft = unit_container.find('div', class_=lambda value: value and 'Floorplan_sqft' in value).find('span')
                unit_bath = unit_container.find('div', class_=lambda value: value and 'Floorplan_bath' in value).find('span')
                
                unit_title_text = unit_title.get_text().strip() if unit_title else ""
                unit_price_text = unit_price.get_text().strip() if unit_price else ""
                
                unit_sqft_text = unit_sqft.get_text().strip() if unit_sqft else ""
                unit_sqft_text = unit_sqft_text if len(re.sub(r'[^\w]', '', unit_sqft_text)) >= 1 else ""
                
                unit_bath_text = unit_bath.get_text().strip() if unit_bath else ""
                unit_bath_text = unit_bath_text if len(unit_bath_text) >= 3 else ""
                
                unit_data = {
                    TableHeaders.BUILDING.value: building_title_text,
                    TableHeaders.ADDRESS.value: address_text,
                    TableHeaders.LISTING.value: unit_title_text,
                    TableHeaders.BED.value: floorplan_title_text,
                    TableHeaders.BATH.value: unit_bath_text,
                    TableHeaders.SQFT.value: unit_sqft_text,
                    TableHeaders.PRICE.value: unit_price_text,
                    TableHeaders.UNIT_AMENITIES.value: unit_amenities_text,
                    TableHeaders.BUILDING_AMENITIES.value: building_amenities_text,
                    TableHeaders.PETS.value: pets_text
                }
                
                self.listings.append(unit_data)  
