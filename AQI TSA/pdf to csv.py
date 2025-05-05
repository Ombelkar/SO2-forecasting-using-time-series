import pandas as pd
import glob
import os

folder_path = "C:/Users/BAPS/Desktop/CSV files"  # e.g., "C:/Users/Om/Desktop/SO2_Files"
all_files = glob.glob(os.path.join(folder_path, "*.csv"))

combined = []

for file in all_files:
    df = pd.read_csv(file)
    # Extract year from filename like "2015 AQI.csv"
    filename = os.path.basename(file)
    year = filename.split()[0]  # Gets '2015' from '2015 AQI.csv'
    df["Year"] = int(year)
    combined.append(df[["Year", "State", "SO2"]])  # Adjust if column names differ

final_df = pd.concat(combined, ignore_index=True)
final_df.to_csv("combined_SO2_data.csv", index=False)
print("Combined CSV created successfully.")
