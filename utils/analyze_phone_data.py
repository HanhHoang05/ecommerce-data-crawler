import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import os

EXPORT_DIR = 'data/exports'

def analyze_phone_data():
    if not os.path.exists(EXPORT_DIR):
        os.makedirs(EXPORT_DIR)

    phones = pd.read_csv('data/processed/clean_phone.csv')
    print(phones.columns)

    #1. Basic Probability (Data Overview)
    print("------------- Data Overview-------------")
    print(phones.info())
    print("------------- Descriptive Statistics -------------")
    print(phones.describe())


    #2. Price Distribution Plot
    phones["DiscountedPrice"] = pd.to_numeric(phones["DiscountedPrice"], errors='coerce')
    plt.figure(figsize=(8, 5))
    sns.histplot(phones["DiscountedPrice"], bins=30, kde=True)
    plt.title("PRICE DISTRIBUTION", fontsize=16, fontweight='bold')
    plt.xlabel("Price (VND)")
    plt.ticklabel_format(style='plain', axis='x')
    formatter = ticker.FuncFormatter(lambda x, p: format(int(x), ','))
    plt.gca().xaxis.set_major_formatter(formatter)
    plt.ylabel("Number of Products")
    plt.savefig(os.path.join(EXPORT_DIR, '01_price_distribution.png'))
    plt.show()


    #3. Top 10 Brands 
    filtered_phones = phones[phones["Brand"] != 'Tin đồn - Mới ra']
    filtered_phones["Rating"] = pd.to_numeric(filtered_phones["Rating"], errors='coerce')
    avg_rating = filtered_phones.groupby("Brand")["Rating"].mean()
    avg_rating_top10 = avg_rating.dropna().sort_values(ascending=False).head(10)

    plt.figure(figsize=(8, 5))
    plt.scatter(avg_rating_top10.values, 
                avg_rating_top10.index, 
                s=100, 
                color='teal') 

    plt.title("TOP 10 BRANDS BY RATING", fontsize=16, fontweight='bold')
    plt.xlabel("Average Rating Score")
    plt.ylabel("Brand")
    plt.grid(axis='x', linestyle='--', alpha=0.7) 

    plt.savefig(os.path.join(EXPORT_DIR, '02_top_brands.png')) 
    plt.show()

    #4. Average Price by Brand
    phones["DiscountedPrice"] = pd.to_numeric(phones["DiscountedPrice"], errors='coerce')
    avg_price = filtered_phones.groupby("Brand")["DiscountedPrice"].mean()
    avg_price_million = avg_price / 1_000_000
    avg_price_top10 = avg_price_million.sort_values(ascending=False).head(10)

    plt.figure(figsize=(8, 5))
    sns.barplot(x=avg_price_top10.values, y=avg_price_top10.index)
    plt.title("AVERAGE PRICE BY BRAND", fontsize=16, fontweight='bold')
    plt.xlabel("Average price (million VND)")
    plt.ticklabel_format(style='plain', axis='x')
    plt.ticklabel_format(style='plain', axis='x')
    formatter = ticker.FuncFormatter(lambda x, p: format(int(x), ','))
    plt.ylabel("Brand")
    plt.savefig(os.path.join(EXPORT_DIR, '03_avg_price_by_brand.png'))
    plt.show()


if __name__ == "__main__":
    analyze_phone_data()