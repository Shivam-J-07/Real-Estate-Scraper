import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from typing import Tuple
from joblib import dump

import os
import joblib

from data.data_cleaner import get_cleaned_df
from constants import TableHeaders

pd.set_option('display.max_columns', None)

def standardize_df(df: pd.DataFrame) -> pd.DataFrame:
    rows_to_drop = []

    city_groups = df.groupby(TableHeaders.CITY.value)
    for city_name, city_df in city_groups:
        unit_groups = city_df.groupby(TableHeaders.BED.value)
        for unit_type, unit_df in unit_groups:
            # Check if the group size is less than 5
            if len(unit_df) < 5:
                rows_to_drop.extend(unit_df.index)

    # Drop the rows outside of the loop
    df = df.drop(rows_to_drop)
    return df

def get_test_train_x_y_arrays(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    city_groups = df.groupby(TableHeaders.CITY.value)
    master_train_df = pd.DataFrame()
    master_test_df = pd.DataFrame()
    for city_name, city_df in city_groups:
        train_df, test_df = train_test_split(city_df, test_size=0.2, random_state=42, stratify=city_df[TableHeaders.BED.value])
        # Concatenate the individual city train and test sets with the master DataFrames
        master_train_df = pd.concat([master_train_df, train_df], ignore_index=True)
        master_test_df = pd.concat([master_test_df, test_df], ignore_index=True)    
    
    dropped_columns = [
        TableHeaders.PRICE.value,
        TableHeaders.BUILDING.value,
        TableHeaders.NEIGHBOURHOOD.value,
        TableHeaders.CITY.value,
        TableHeaders.LISTING.value,
        TableHeaders.ADDRESS.value,
        TableHeaders.DATE.value,
    ]

    updated_train_df = master_train_df.drop(dropped_columns, axis=1)
    updated_test_df = master_test_df.drop(dropped_columns, axis=1)  

    print(updated_train_df.isna().sum())

    X_train = np.array(updated_train_df.values)
    y_train = np.array(master_train_df[TableHeaders.PRICE.value].values)

    X_test = np.array(updated_test_df.values)
    y_test = np.array(master_test_df[TableHeaders.PRICE.value].values)

    return (X_test, y_test, X_train, y_train)

def train_model(df: pd.DataFrame, filepath: str, archive_filepath=""):            
    df = standardize_df(df)

    X_test, y_test, X_train, y_train = get_test_train_x_y_arrays(df)

    # Create the Random Forest classifier
    random_forest = RandomForestRegressor(n_estimators=500, random_state=42)

    # Train the model
    random_forest.fit(X_train, y_train)

    # Predict using the test set
    predictions = random_forest.predict(X_test)

    # Evaluate accuracy
    print(f"Model R^2 score on test set: {random_forest.score(X_test, y_test):.4f}")

    # Save random forest model
    dump(random_forest, filepath)           

    if archive_filepath:
        # Save random forest model to archived models
        dump(random_forest, archive_filepath) 

def get_model(filepath: str):
    model = joblib.load(filepath)
    return model