from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from bs4 import BeautifulSoup
from constants import TableHeaders
from utils import (
    get_headers,
    get_absolute_url, 
    generate_time_gap, 
    match_address, 
    match_pets
)

import re
import time

class BaseScraper():
    """
    Abstract base class for building web scrapers.

    Attributes:
        base_url (str): Base URL of the site.
        full_url (str): Full URL for making specific requests.
        urls (List[str]): List of URLs to scrape from.
        listings (List[dict]): All rental listings scraped.
    """
    def __init__(self, base_url="", full_url=""):
        self.base_url = base_url
        self.full_url = full_url
        self.urls = []
        self.listings = []
    
    def make_request(self, session: type) -> str:
        """
        Makes an HTTP GET request using the provided session object.
        
        Args:
            session (requests.Session): The session object to make the request.

        Returns:
            str: The response text of the HTTP request.

        Raises:
            Exception: If the response status code is not 200.
        """
        response = session.get(self.full_url, headers=get_headers(self.base_url))
        if response.status_code != 200:
            raise Exception(f"Failed to fetch page at {self.full_url}. Status code: {response.status_code}")
        return response.text

      
class PadmapperScraper(BaseScraper):
    """
    Web scraper specifically designed for the Padmapper website.

    Inherits from BaseScraper and adds methods tailored for scraping Padmapper.
    """
    def __init__(self, base_url="", full_url=""):
        super().__init__(base_url, full_url)
    
    def fetch_rental_listing_urls(self, session, web_driver):
        """
        Retrieves and stores all the listing urls from the main page.

        Args:
            session (requests.Session): The session object to make the request.
            web_driver (webdriver): The Selenium WebDriver to use for scraping.
        """
        try:
            web_driver.get(self.full_url)
            generate_time_gap()
            WebDriverWait(web_driver, 20).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
            self.scroll_to_end_of_page(web_driver)
            self.urls = self.extract_urls(web_driver)
            print(f"Number of URLs: {len(self.urls)}")
        except Exception as e:
            print(f"ERROR: {str(e)}")

    def scroll_to_end_of_page(self, web_driver):
        """
        Scrolls to the end of the page until no more content loads.

        Args:
            web_driver (webdriver): The Selenium WebDriver to use for scraping.
        """
        while True:
            web_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)  # Adjust based on the site's response time
            try:
                no_more_content_divs = web_driver.find_elements(By.XPATH, "//*[contains(@class, 'list_noMoreResult')]")
                if no_more_content_divs:
                    print("Reached the end of the page.")
                    break
            except NoSuchElementException:
                continue

    def extract_urls(self, web_driver):
        """
        Extracts rental listing URLs from the BeautifulSoup-parsed page.

        Args:
            web_driver (webdriver): The Selenium WebDriver to use for scraping.

        Returns:
            List[str]: List of extracted URLs.
        """
        page_html_content = web_driver.page_source
        soup = BeautifulSoup(page_html_content, 'html.parser')
        link_elements = soup.find_all('a', class_=lambda cls: cls and cls.startswith('ListItemFull_headerText'))
        return [get_absolute_url(self.base_url, link.get('href')) for link in link_elements]

            
    def get_page_content_from_urls(self, web_driver):
        """
        Iterates over all collected urls and scrapes data from each link's page.

        Args:
            web_driver (webdriver): The Selenium WebDriver to use for scraping.
        """
        for link in self.urls:
            try:
                web_driver.get(link)
                generate_time_gap()
                WebDriverWait(web_driver, 30).until(
                    lambda d: d.execute_script('return document.readyState') == 'complete'
                )
                try:
                    # Optional wait: proceed if elements are found, skip if not
                    WebDriverWait(web_driver, 10).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[class*='Floorplan_floorplanPanel']"))
                    )
                    dropdown_divs = web_driver.find_elements(By.CSS_SELECTOR, "div[class*='Floorplan_floorplanPanel']")
                    for div in dropdown_divs:
                        web_driver.execute_script("arguments[0].scrollIntoView();", div)
                        web_driver.execute_script("arguments[0].click();", div)
                        generate_time_gap()
                except TimeoutException:
                    print(f"Specific elements not found on {link}. Proceeding with available content.")
                
                link_html_content = web_driver.page_source
                self.get_rental_unit_data(link_html_content)
            
            except Exception as e:
                print(f"Error encountered on page {link}: {e}")
    
    def get_rental_unit_data(self, link_html_content):
        """
        Extracts relevant data from rental unit listing page

        Args:
            link_html_content (str): The HTML content of the page to be scraped.
        """
        
        # Parse the HTML with Beautiful Soup
        soup = BeautifulSoup(link_html_content, 'html.parser')
        
        building_title_text, address_text, pets_text = DataExtractor.extract_building_details(soup)

        unit_amenities_text, building_amenities_text = DataExtractor.extract_amenities(soup)

        all_units_data = DataExtractor.extract_rental_unit_details(soup)

        for unit_data in all_units_data:
            unit_data[TableHeaders.PETS.value] = pets_text
            unit_data[TableHeaders.PETS.value] = pets_text
            unit_data[TableHeaders.UNIT_AMENITIES.value] = unit_amenities_text
            unit_data[TableHeaders.BUILDING_AMENITIES.value] = building_amenities_text
            unit_data[TableHeaders.ADDRESS.value] = address_text
            unit_data[TableHeaders.BUILDING.value] = building_title_text
            self.listings.append(unit_data)
        
class DataExtractor():
    @staticmethod
    def extract_building_details(soup: BeautifulSoup) -> tuple:
        """
        Extracts text of unit and building amenities.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object to extract data from.

        Returns:
            Tuple[str, str]: A tuple containing text of unit amenities and building amenities.
        """
        building_title = soup.find('h1', class_=lambda cls: cls and 'FullDetail_street_' in cls)
        building_title_text = re.split(r'[^\w ]+',  building_title.get_text())[0] if building_title else ""

        details = soup.find('div', class_=lambda cls: cls and 'SummaryTable_summaryTable_' in cls)

        address_header = details.find(match_address)
        parent_address_li = address_header.find_parent('li')
        address_div = parent_address_li.find('div') if parent_address_li else None
        address_text = address_div.get_text().strip() if address_div else ""
        
        pets_header = details.find(match_pets)
        parent_pets_li = pets_header.find_parent('li')
        pets_div = parent_pets_li.find('div') if parent_pets_li else None
        pets_text = pets_div.get_text().strip() if pets_div else ""

        return (building_title_text, address_text, pets_text)

    @staticmethod
    def extract_amenities(soup: BeautifulSoup) -> tuple:
        """
        Extracts text of unit and building amenities.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object to extract data from.

        Returns:
            Tuple[str, str]: A tuple containing text of unit amenities and building amenities.
        """
        amenities = soup.find_all('div', class_=lambda value: value and 'Amenities_header_' in value)
        unit_amenities, building_amenities = [], []
        try:
            unit_amenities_header = amenities[0] if len(amenities) == 2 and "apartment" in amenities[0].get_text().lower() else ""
            building_amenities_header = amenities[1] if len(amenities) == 2 and "building" in amenities[1].get_text().lower() else ""
            unit_amenities_container = unit_amenities_header.find_parent('div') if unit_amenities_header else ""
            building_amenities_container = building_amenities_header.find_parent('div') if building_amenities_header else ""
            unit_amenities = unit_amenities_container.find_all('div', class_=lambda cls: cls and 'Amenities_text_' in cls) if unit_amenities_container else []
            building_amenities = building_amenities_container.find_all('div', class_=lambda cls: cls and 'Amenities_text_' in cls) if building_amenities_container else []
        except Exception as e:
            print("Error - Getting amenities: ", e)
            
        unit_amenities_text = ", ".join([amenity.get_text() for amenity in unit_amenities])  
        building_amenities_text = ", ".join([amenity.get_text() for amenity in building_amenities])  

        return(unit_amenities_text, building_amenities_text)

    @staticmethod
    def extract_rental_unit_details(soup: BeautifulSoup) -> list:
        """
        Extracts rental unit details from listing.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object to extract data from.

        Returns:
            List[dict]: A list of dictionaries, each containing data for a rental unit.
        """
        all_units_data = []

        # Find all divs where class contains 'Floorplan_floorplan'
        floorplans = soup.find_all('div', class_=lambda cls: cls and 'Floorplan_floorplansContainer_' in cls)
        
        for floorplan in floorplans:
            current_floorplan = floorplan.find('div', class_=lambda cls: cls and 'Floorplan_title_' in cls)
            floorplan_title_text = current_floorplan.get_text().strip() if current_floorplan else ""
            
            unit_containers = floorplan.find_all('div', class_=lambda cls: cls and 'Floorplan_floorplanDetailContainer_' in cls)
            for unit_container in unit_containers:
                unit_title = unit_container.find('div', class_=lambda cls: cls and 'Floorplan_floorplanTitle' in cls)
                unit_price = unit_container.find('div', class_=lambda cls: cls and 'Floorplan_floorplanPrice' in cls)
                unit_sqft = unit_container.find('div', class_=lambda cls: cls and 'Floorplan_sqft' in cls).find('span')
                unit_bath = unit_container.find('div', class_=lambda cls: cls and 'Floorplan_bath' in cls).find('span')
                
                unit_title_text = unit_title.get_text().strip() if unit_title else ""
                unit_price_text = unit_price.get_text().strip() if unit_price else ""
                
                unit_sqft_text = unit_sqft.get_text().strip() if unit_sqft else ""
                unit_sqft_text = unit_sqft_text if len(re.sub(r'[^\w]', '', unit_sqft_text)) >= 1 else ""
                
                unit_bath_text = unit_bath.get_text().strip() if unit_bath else ""
                unit_bath_text = unit_bath_text if len(unit_bath_text) >= 3 else ""
                
                unit_data = {
                    TableHeaders.LISTING.value: unit_title_text,
                    TableHeaders.BED.value: floorplan_title_text,
                    TableHeaders.BATH.value: unit_bath_text,
                    TableHeaders.SQFT.value: unit_sqft_text,
                    TableHeaders.PRICE.value: unit_price_text,
                }

                all_units_data.append(unit_data)
        
        return all_units_data
