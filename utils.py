from fake_useragent import UserAgent
import random
import time

from enum import Enum

def get_headers(base_url):
    user_agent = UserAgent().random
    
    # Get a random user agent for Windows
    while not 'windows' in user_agent.lower():
        user_agent = UserAgent().random
    
    print(user_agent)
    # Set additional headers to mimic realistic behavior
    headers = {
        'User-Agent': user_agent,
        'DNT': '1',  # Do Not Track,
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': f'{base_url}',
        'DNT': '1',
        'Sec-Ch-Ua': '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': 'Windows',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1'
    }
    return headers

def generate_time_gap():
    # Add a delay between requests to avoid overloading the server
    time.sleep(random.uniform(3, 7))

def get_absolute_url(base_url, href):
    return href if href.startswith('http') else f'{base_url}{href}'

def get_address_element(tag):
    return 'h' in tag.name and 'address' in tag.text.lower().strip()

def make_matcher(tag_name, text):
    def match_tag(element):
        return (
            tag_name in element.name and 
            text.lower() in element.get_text().lower().strip()
        )
    return match_tag

match_address = make_matcher('h', 'address')
match_pets = make_matcher('h', 'Dogs')
match_sqft = make_matcher('h', 'feet')

class TableHeaders(Enum):
    BUILDING = 'Building'
    ADDRESS = 'Address'
    LISTING = 'Listing'
    BED = 'Bed'
    BATH = 'Bath'
    SQFT = 'SqFt'
    PRICE = 'Price'
    UNIT_AMENITIES = 'Unit Amenities'
    BUILDING_AMENITIES =  'Building Amenities'
    PETS = 'Pets'
    

