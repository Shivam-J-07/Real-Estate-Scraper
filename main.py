import os
from datetime import datetime
import pandas as pd

from data.main import extract_raw_data
from data.data_cleaner import get_cleaned_df

from backend.services.create import add_listing_data_to_db
from backend.dependencies import get_db

from model.model import train_model

current_dir = os.path.dirname(os.path.realpath(__file__))

# current_timestamp = datetime.now().strftime("%d-%m-%Y")

current_timestamp = "01-01-2024"

raw_filepath = f"{current_dir}/data/raw_data/{current_timestamp}_rental_listings.xlsx"
cleaned_filepath = f"{current_dir}/data/cleaned_data/{current_timestamp}_cleaned_listings.xlsx"
model_filepath = f"{current_dir}/model/model.joblib"
model_archive_filepath = f"{current_dir}/model/model_archives/{current_timestamp}_model.joblib"

# # Extract raw data to acquire the rental listing data for the current month
# try:
#     extract_raw_data(
#         filepath=raw_filepath,
#         listing_urls=[
#             "https://www.padmapper.com/apartments/vancouver-bc",
#             "https://www.padmapper.com/apartments/winnipeg-mb",
#             "https://www.padmapper.com/apartments/toronto-on",
#             "https://www.padmapper.com/apartments/edmonton-ab",
#             "https://www.padmapper.com/apartments/montreal-qc",
#         ]
#     )

#     cleaned_data_df = get_cleaned_df(
#         raw_filepath=raw_filepath, cleaned_filepath=cleaned_filepath
#     )

# except Exception as e:
#     print("An error occurred while extracting data:", e)
#     if os.path.exists(cleaned_filepath):
#         os.remove(cleaned_filepath)
#     exit()

cleaned_data_df = get_cleaned_df(
    raw_filepath=raw_filepath, cleaned_filepath=cleaned_filepath
)

# Push the acquired data to Neon DB
# try:
#     add_listing_data_to_db(get_db(), cleaned_data_df)
# except Exception as e:
#     print("An error occurred while updated the database:", e)
#     exit()

# Retrain the model and update the joblib object containing the model
train_model(df=cleaned_data_df, filepath=model_filepath, archive_filepath=model_archive_filepath)
