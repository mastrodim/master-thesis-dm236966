#!/usr/bin/env python3
"""
replace_labels.py

Replaces specific values in the Label column of the combined_final.csv file
found in the ./combined_final_csv/ folder, overwriting the same file.
"""

import pandas as pd
import os

# Path to the combined file
combined_path = os.path.join("combined_final_csv", "combined_final.csv")

# Mapping of old labels -> new labels
label_mapping = {
    "SPOOFING": "Spoofing_ARP",
}

def main():
    # Check if file exists
    if not os.path.exists(combined_path):
        raise FileNotFoundError(f"File not found: {combined_path}")

    # Load CSV
    df = pd.read_csv(combined_path)

    if "Label" not in df.columns:
        raise ValueError("No 'Label' column found in the CSV.")

    # Replace labels
    df["Label"] = df["Label"].replace(label_mapping)

    # Overwrite the same file
    df.to_csv(combined_path, index=False)

    print(f"✅ Relabelled and overwritten: {combined_path}")

if __name__ == "__main__":
    main()
