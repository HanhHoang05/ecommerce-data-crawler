import os
import pandas as pd
from pathlib import Path
import re

def clean_phone_data(df: pd.DataFrame) -> pd.DataFrame:

    # input_path = 'data/processed/phone_all.csv'
    output_dir = 'data/processed/clean_phone.csv'

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

    #Quantity Sold
    def convert_sold(text):
        if pd.isna(text): return None

        text = text.lower()
        text = re.sub(r'[^0-9,k,\,\.]', '', text)

        if 'k' in text:
            text = text.replace('k', '').replace(',', '.')
            return int(float(text) * 1000)
        else:
            return int(text)

    #BatteryCapacity
    def cleanse_battery_capacity(capacity_str):
        if pd.isna(capacity_str):
            return None
        try:
            return int(str(capacity_str).replace(' mAh', '').replace('.', ','))
        except ValueError:
            return None

    #RAM
    def cleanse_RAM(value):
        if pd.isna(value):
            return None
        ram_str = str(value).upper().replace(' ', '')

        for unit in ['GB', 'G', 'MB', 'M']:
            ram_str = ram_str.replace(unit, '')

        if ram_str.isdigit():
            return int(ram_str)
        return None

    #Resolution
    def cleanse_resolution(res_str):
        if pd.isna(res_str):
            return None
        numbers = re.findall(r'\d+', str(res_str))

        if len(numbers) >= 2:
            return f"{numbers[0]}x{numbers[1]}"
        return None

    #ROM
    def cleanse_ROM(rom_str):
        if pd.isna(rom_str):
            return None

        rom_str = str(rom_str).upper().replace(" ", "")
        parts = rom_str.split("/")
        first_part = parts[0]

        units = {"TB": 1024, "T": 1024, "GB": 1, "G": 1}
        for unit, multiplier in units.items():
            if unit in first_part:
                num_str = first_part.replace(unit, "")
                if num_str.isdigit():
                    return int(num_str) * multiplier
        if first_part.isdigit():
            return int(first_part)
        return None

    #Screen Size
    def cleanse_ScreenSize(value):
        if pd.isna(value):
            return None
        return float(''.join([c for c in str(value) if c.isdigit() or c == '.']))


    #NumberOfReview
    def extract_number(text):
        if pd.isna(text) or str(text).strip().lower() == 'nan' or str(text).strip() == '':
            return pd.NA
        match = re.search(r'\d+', str(text))
        return int(match.group()) if match else pd.NA

    df['DiscountedPrice'] = df['DiscountedPrice'].apply(cleanse_price)
    df['DiscountPercentage'] = df['DiscountPercentage'].apply(cleanse_discount_percent).astype('Int64')
    df['SoldQuantity'] = df['SoldQuantity'].apply(convert_sold).astype('Int64')
    df['BatteryCapacity']  = (df["BatteryCapacity"].apply(cleanse_battery_capacity)).astype('Int64')
    df['RAM'] = df['RAM'].apply(cleanse_RAM).astype('Int64')
    df['Resolution'] = df['Resolution'].apply(cleanse_resolution).astype('string')
    df['ROM'] = df['ROM'].apply(cleanse_ROM).astype('Int64')
    df['ScreenSize'] = df['ScreenSize'].apply(cleanse_ScreenSize).astype('float64')
    df['NumberOfReview'] = df['NumberOfReview'].apply(extract_number).astype('Int64')

    df.to_csv(output_dir, index=False, encoding='utf-8-sig')
    print(f"Saved cleaned phone data to {output_dir}")

    return df
