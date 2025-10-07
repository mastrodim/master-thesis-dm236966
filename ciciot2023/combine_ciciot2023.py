#!/usr/bin/env python3
"""
combine_ciciot2023.py

Combines all CSV files found in the ./ciciot2023_csvs/ folder
into a single comprehensive file.

Output:
  ./combined/combined_ciciot2023.csv
"""

import os
import glob
import pandas as pd

def combine_csvs(source_folder="ciciot2023_csvs", output_folder="combined"):
    # Create output folder if not exists
    os.makedirs(output_folder, exist_ok=True)

    # Find all CSV files in the source folder
    pattern = os.path.join(source_folder, "*.csv")
    csv_files = glob.glob(pattern)

    if not csv_files:
        print(f"⚠️  No CSV files found in {source_folder}")
        return

    print(f"Found {len(csv_files)} CSV files in '{source_folder}'. Combining now…\n")

    dfs = []
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file)
            dfs.append(df)
            print(f"  ✅ Loaded {os.path.basename(csv_file)} ({len(df)} rows)")
        except Exception as e:
            print(f"  ❌ Error reading {csv_file}: {e}")

    if not dfs:
        print("⚠️  No valid CSVs to combine.")
        return

    # Combine all CSVs
    combined_df = pd.concat(dfs, ignore_index=True)

    # Save the combined file
    output_path = os.path.join(output_folder, "combined_ciciot2023.csv")
    combined_df.to_csv(output_path, index=False)

    print(f"\n🎉 Combined {len(csv_files)} files into {output_path}")
    print(f"📊 Total rows: {len(combined_df)}")

def main():
    combine_csvs()

if __name__ == "__main__":
    main()
