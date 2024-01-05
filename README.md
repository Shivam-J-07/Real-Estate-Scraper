# RentRite

## Overview

![](./images/feature_importances.png)

![](./images/price_to_sqft.png)

![](./images/linear_regression.png)

![](./images/random_forest.png)

### Terminology

These terms that appear throughout the project are defined explicitly for the reader’s convenience to clarify precisely what they are referring to.

| Term              | Definition                                                                                          |
|-------------------|-----------------------------------------------------------------------------------------------------|
| Listing           | Contains all the units i.e. floor plans available to rent in a specific building.                   |
| Unit              | Refers to the specific apartment in a building available to rent, synonymous with floor plan.        |
| Amenities         | Refers to premiums included with a unit or a building.                                              |
| Unit amenities    | Balcony, In Unit Laundry, Air Conditioning, High Ceilings, Furnished, Hardwood Floor.               |
| Building amenities| Controlled Access, Fitness Center, Swimming Pool, Roof Deck, Storage, Residents Lounge, Outdoor Space.|


## Setup

This project runs on [Python 3](https://www.python.org/downloads/). Make sure you have a version of Python 3 installed.

### Installing `chromedriver`

In order to run the web scrapers to extract rental listings data, you'll need to install `chromedriver`. Make sure [homebrew](https://brew.sh/) is installed, then run:

```bash
brew install chromedriver 
```

Next get the installation path:

```bash
which chromedriver
```

If you see the error `"Google Chrome for Testing.app is damaged and can’t be opened. You should move it to the Trash."`, run the following:

```bash
xattr -cr 'Google Chrome for Testing.app'
```

### Creating your environment

In the project directory, start by creating and activating a virtual environment:

```bash
python -m venv env # create virtual env named env
source env/bin/activate # activate it
```

Then install all the project requirements:

```bash
pip install -r requirements.txt
```

Now create a `.env` file in the root directory by making a copy of [`.env.schema`](./.env.schema). Replace the `CHROMEDRIVER_PATH` variable in your `.env` file with your `chromedriver` installation path.

### Initialize the database

This project uses a PostgreSQL database to store the extracted rental listing data for each building and its units posted. You can recreate the setup by initializing your own PostgreSQL database (we use [Neon](https://neon.tech/) for a serverless DB) and replacing the `DATABASE_URL` variable in your `.env` file with your database [connection string](https://neon.tech/docs/connect/connect-from-any-app).

### Running the project

Running `main.py` in the root directory will commence the data acquisition and model training process, which executes the following steps:
1. Run the data scraper to acquire the rental listing data for the current month.
2. Push the extracted unit and building details for each listing to your PostgreSQL DB.
3. Re-train the model using the extracted data, then save the updated model as `model.joblib` where it will be utilized by the backend API.

```bash
python -m main
```

To start the backend API from the root directory, run:

```bash
python -m uvicorn backend.app:app --reload
```
