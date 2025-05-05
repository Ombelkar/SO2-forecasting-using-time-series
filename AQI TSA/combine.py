import pandas as pd
import glob
import os

folder_path = "C:/Users/BAPS/Desktop/CSV files" 
all_files = glob.glob(os.path.join(folder_path, "*.csv"))

combined = []

for file in all_files:
    df = pd.read_csv(file)
   
    filename = os.path.basename(file)
    year = filename.split()[0]  
    df["Year"] = int(year)
    combined.append(df[["Year", "State", "SO2"]])  

final_df = pd.concat(combined, ignore_index=True)
final_df.to_csv("combined_SO2_data.csv", index=False)
print("Combined CSV created successfully.")
