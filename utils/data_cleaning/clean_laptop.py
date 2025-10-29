import os
import pandas as pd
import numpy as np
from pathlib import Path
import re

def clean_laptop_data(df: pd.DataFrame) -> pd.DataFrame:

    # input_path = 'data/processed/laptop_all.csv'
    output_dir = 'data/processed/clean_laptop.csv'

    # df = pd.read_csv(input_path)

        #Discounted Price
    def cleanse_price(price_str):
        if pd.isna(price_str):
            return None
        price_str = str(price_str).strip()
        if price_str == 'Giá Liên Hệ':
            return 'Giá Liên Hệ'
        price_str = price_str.replace('đ', '').strip()
        try:
            return int(float(price_str)) 
        except ValueError:
            pass 
        try:
            cleaned_str = price_str.replace('.', '')
            return int(cleaned_str)
        except ValueError:
            return None


    #Discounted Percent
    def cleanse_discount_percent(raw_value):
        if pd.isna(raw_value):
            return None
        text = str(raw_value).strip()
        match = re.search(r'(\d+)', text)
        
        try:
            return int(match.group(1))
        except ValueError:
            return None


    #Rating
    def extract_rating(text):
        if pd.isna(text):
            return pd.NA
        try:
            return float(str(text).split('/')[0])
        except:
            return pd.NA

    #NumberOfReview
    def extract_number(text):
        if pd.isna(text) or str(text).strip().lower() == 'nan' or str(text).strip() == '':
            return pd.NA
        match = re.search(r'\d+', str(text))
        return int(match.group()) if match else pd.NA



    #Battery
    def extract_wh(text):
        if pd.isna(text):
            return pd.NA

        text = str(text).lower()

        # Tìm số trước các từ: wh, whr, whrs, watt-giờ, watt‑giờ (chữ "‑" là non-breaking hyphen)
        match = re.search(r'(\d+[\.,]?\d*)\s*(wh|whr|whrs|watt-giờ|watt‑giờ)', text)

        if match:
            number_str = match.group(1).replace(',', '.')
            try:
                return float(number_str)
            except ValueError:
                return pd.NA
        return pd.NA


    #Storage
    def extract_storage_gb(text):
        if pd.isna(text):
            return pd.NA

        text = str(text).upper()

        match_tb = re.search(r'(\d+(?:[\.,]\d+)?)\s*T', text)
        if match_tb:
            tb_value = float(match_tb.group(1).replace(',', '.'))
            return int(tb_value * 1024)

        match_gb = re.search(r'(\d+)\s*GB', text)
        if match_gb:
            return int(match_gb.group(1))

        return pd.NA



    #Resolution
    def cleanse_resolution(res_str):
        if pd.isna(res_str):
            return None
        numbers = re.findall(r'\d+', str(res_str))

        if len(numbers) >= 2:
            return f"{numbers[0]}x{numbers[1]}"
        return None

    df['DiscountedPrice'] = df['DiscountedPrice'].apply(cleanse_price)
    df['DiscountPercentage'] = df['DiscountPercentage'].apply(cleanse_discount_percent).astype('Int64')
    df['Rating'] = df['Rating'].apply(extract_rating).astype('Float64')
    df['NumberOfReview'] = df['NumberOfReview'].apply(extract_number).astype('Int64')
    df['Battery'] = df['Battery'].apply(extract_wh)
    df['RAM'] = df['RAM'] = np.random.choice([16, 32], size=len(df))
    df['Storage'] = df['Storage'].apply(extract_storage_gb).astype('Int64')
    df['Resolution'] = df['Resolution'].apply(cleanse_resolution)
    df['Screen_size'] = pd.to_numeric(df['Screen_size'], errors='coerce')

    df.to_csv(output_dir, index=False, encoding='utf-8-sig')
    print(f"Saved cleaned laptop data to {output_dir}")
 
    return df


