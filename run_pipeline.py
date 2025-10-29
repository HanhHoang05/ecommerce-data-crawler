import os
import logging
import urllib
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine
from utils.merge_data.merge_phone import merge_phone_data
from utils.merge_data.merge_laptop import merge_laptop_data
from utils.data_cleaning.clean_phone import clean_phone_data
from utils.data_cleaning.clean_laptop import clean_laptop_data


def main():
    try:
        logging.info("STEP 1: Merging raw data...")
        phone_merged = merge_phone_data()
        laptop_merged = merge_laptop_data()
    except Exception:
        logging.exception("Error during merging step")
        raise

    try:
        logging.info("STEP 2: Cleaning merged data...")
        clean_phone_df = clean_phone_data(phone_merged)
        clean_laptop_df = clean_laptop_data(laptop_merged)
    except Exception:
        logging.exception("Error during cleaning step")
        raise

    try:
        logging.info("STEP 3: Loading data into SQL Server...")
        params = urllib.parse.quote_plus(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=HANHHOANG\\SQLEXPRESS;"
            "DATABASE=EcommerceDB;"
            "Trusted_Connection=yes;"
        )

        engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

        clean_phone_df.to_sql("Phones", con=engine, if_exists="replace", index=False)
        clean_laptop_df.to_sql("Laptops", con=engine, if_exists="replace", index=False)

        logging.info("Data loaded successfully into SQL Server!")

    except Exception:
        logging.exception("Error during SQL Server load step")
        raise

    logging.info("Pipeline completed successfully!")


if __name__ == "__main__":
    main()
