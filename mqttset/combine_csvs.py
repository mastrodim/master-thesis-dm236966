#!/usr/bin/env python3
import os
import glob
import pandas as pd

INPUT_DIR = "csv_files"
OUTPUT_DIR = "combine"
OUTPUT_NAME = "combined.csv"

def combine_csvs():
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Find all CSV files in the source folder (non-recursive)
    pattern = os.path.join(INPUT_DIR, "*.csv")
    csv_files = sorted(
        p for p in glob.glob(pattern)
        if os.path.basename(p).lower() != OUTPUT_NAME.lower()  # avoid re-including a previous combined
    )

    if not csv_files:
        print(f"No CSV files found in: {INPUT_DIR}")
        return

    # Read and accumulate
    dfs = []
    for path in csv_files:
        try:
            df = pd.read_csv(path)
            dfs.append(df)
        except Exception as e:
            print(f"Skipping {path} (read error: {e})")

    if not dfs:
        print("No valid CSVs to combine.")
        return

    # Concatenate all into one DataFrame (row-wise)
    combined_df = pd.concat(dfs, ignore_index=True)

    # Save to combine/combined.csv
    out_path = os.path.join(OUTPUT_DIR, OUTPUT_NAME)
    combined_df.to_csv(out_path, index=False)
    print(f"Combined {len(csv_files)} files into {out_path}")

if __name__ == "__main__":
    combine_csvs()
