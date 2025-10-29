import os
import pandas as pd
from pathlib import Path

def merge_laptop_data(raw_dir="data/raw", output_dir="data/processed/laptop_all.csv"):

    Path(Path(output_path).parent).mkdir(parents=True, exist_ok=True)

    df1 = pd.read_csv(os.path.join(raw_dir, 'laptop_CellphoneS.csv'))
    df2 = pd.read_csv(os.path.join(raw_dir, 'laptop_thegioididong.csv'))

    df_merged = pd.concat(
        [df1, df2],  
        ignore_index=True      
    )

    df_merged.to_csv(output_dir, index=False, encoding='utf-8-sig')
    return df_merged

if __name__ == "__main__":
    merge_laptop_data()


