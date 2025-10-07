#!/usr/bin/env python3
import os
import glob
import pandas as pd

def combine_merged_csvs(source_folder="merged_csvs", output_folder="combined_final_csv"):
    """Combine all merged CSVs into a single final dataset."""
    os.makedirs(output_folder, exist_ok=True)

    pattern = os.path.join(source_folder, "*.csv")
    csv_files = glob.glob(pattern)

    if not csv_files:
        print(f"⚠️  No CSV files found in {source_folder}")
        return

    dfs = []
    print(f"Found {len(csv_files)} merged CSVs in '{source_folder}'. Combining now…\n")

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

    combined_df = pd.concat(dfs, ignore_index=True)
    output_path = os.path.join(output_folder, "combined_final.csv")
    combined_df.to_csv(output_path, index=False)

    print(f"\n🎉 Combined {len(csv_files)} files into {output_path}")
    print(f"📊 Total rows: {len(combined_df)}")

def main():
    combine_merged_csvs()

if __name__ == "__main__":
    main()
