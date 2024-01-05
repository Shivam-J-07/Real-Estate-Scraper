import os
import requests
from datetime import datetime
from urllib.parse import urljoin
from dotenv import load_dotenv

from data.main import extract_raw_data
from data.data_cleaner import get_cleaned_df

from model.model import train_model

load_dotenv()

current_dir = os.path.dirname(os.path.realpath(__file__))

current_timestamp = datetime.now().strftime("%d-%m-%Y")

cleaned_data_files = os.listdir(os.path.join('data', 'cleaned_data'))
# Check if there's a cleaned_data excel sheet in the data/cleaned_data dir containing the current year and month
monthly_data_exists = any(datetime.now().strftime("%m-%Y") in filename for filename in cleaned_data_files)

raw_filepath = f"{current_dir}/data/raw_data/{current_timestamp}_rental_listings.xlsx"
cleaned_filepath = f"{current_dir}/data/cleaned_data/{current_timestamp}_cleaned_listings.xlsx"
model_filepath = f"{current_dir}/backend/model.joblib"
model_archive_filepath = f"{current_dir}/model/model_archives/{current_timestamp}_model.joblib"

# Extract raw data to acquire the rental listing data for the current month -----------------
if monthly_data_exists:
    print("Monthly data has already been scraped.")
    exit()

try:
    extract_raw_data(
        filepath=raw_filepath,
        listing_urls=[
            "https://www.padmapper.com/apartments/vancouver-bc",
            "https://www.padmapper.com/apartments/winnipeg-mb",
            "https://www.padmapper.com/apartments/toronto-on",
            "https://www.padmapper.com/apartments/edmonton-ab",
            "https://www.padmapper.com/apartments/montreal-qc",
        ]
    )

    cleaned_data_df = get_cleaned_df(
        raw_filepath=raw_filepath, cleaned_filepath=cleaned_filepath
    )

except Exception as e:
    print("An error occurred while extracting data:", e)
    if os.path.exists(cleaned_filepath):
        os.remove(cleaned_filepath)
    exit()

# Push the acquired data to Neon DB ---------------------------------------------------------

# API endpoint URL
API_URL = urljoin(os.getenv("API_URL"), "analysis")

# Payload (data to be sent in the POST request)
payload = cleaned_data_df.copy()
payload.columns = payload.columns.str.lower().str.replace(' ', '_')
payload = payload.astype(str)
payload = payload.to_dict(orient='records')

# Sending a POST request to the API
response = requests.post(API_URL, json=payload)

# Handling the response
if response.status_code == 201:
    # Accessing the response data
    data = response.json()
    print(data)
else:
    print("Request failed with status code:", response.status_code)
    exit()

# Retrain the model and update the joblib object containing the model -----------------------
train_model(df=cleaned_data_df, filepath=model_filepath,
            archive_filepath=model_archive_filepath)
