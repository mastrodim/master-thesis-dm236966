#!/usr/bin/env python3
"""
remove_unused_attacks.py

Reads combined/combined_ciciot2023.csv, removes rows whose Label is in:
  - SQLINJECTION
  - UPLOADING_ATTACK
  - XSS
  - BROWSERHIJACKING

Writes to combined/combined_ciciot2023_filtered.csv (overwrites if exists),
then deletes the original combined_ciciot2023.csv.
"""

import os
import sys
import pandas as pd

COMBINED_DIR = "combined"
INPUT_NAME   = "combined_ciciot2023.csv"
BASE, EXT    = os.path.splitext(INPUT_NAME)
OUTPUT_NAME  = f"{BASE}_filtered{EXT}"

UNWANTED = {"SQLINJECTION", "UPLOADING_ATTACK", "XSS", "BROWSERHIJACKING"}

def main():
    in_path  = os.path.join(COMBINED_DIR, INPUT_NAME)
    out_path = os.path.join(COMBINED_DIR, OUTPUT_NAME)

    if not os.path.isdir(COMBINED_DIR):
        sys.exit(f"Folder not found: {COMBINED_DIR}")
    if not os.path.isfile(in_path):
        sys.exit(f"Input CSV not found: {in_path}")

    df = pd.read_csv(in_path)
    if "Label" not in df.columns:
        sys.exit("Error: 'Label' column not found in the CSV.")

    total_before = len(df)

    # Normalize for comparison (trim + upper) but keep original values in output
    norm = df["Label"].astype(str).str.strip().str.upper()
    filtered_df = df[~norm.isin(UNWANTED)].copy()

    # Write filtered file (overwrite if exists)
    filtered_df.to_csv(out_path, index=False)

    # Remove original file so only the *_filtered.csv remains
    try:
        os.remove(in_path)
    except Exception as e:
        print(f"Warning: could not remove original file {in_path}: {e}")

    print(f"Filtered CSV saved to: {out_path}")
    print(f"Original rows: {total_before}")
    print(f"Filtered rows: {len(filtered_df)}")
    print(f"Dropped rows:  {total_before - len(filtered_df)}")

if __name__ == "__main__":
    main()
