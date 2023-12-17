from fake_useragent import UserAgent

from dotenv import load_dotenv
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions

def create_chrome_driver(*, debugging_port):
    # Load environment variables from .env file
    load_dotenv()

    # Generate a random user agent
    user_agent = UserAgent().random

    # Access the WebDriver path from the environment variable
    chrome_driver_path = os.getenv('CHROMEDRIVER_PATH') 

    # Set up Chrome options (optional, for additional configurations)
    chrome_options = ChromeOptions()
    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"--remote-debugging-port={debugging_port}")
    # chrome_options.add_argument("--headless")  # Enable headless mode (does not open browser GUI)

    # First ChromeService instance
    chrome_service = ChromeService(executable_path=chrome_driver_path)

    return webdriver.Chrome(service=chrome_service , options=chrome_options)
