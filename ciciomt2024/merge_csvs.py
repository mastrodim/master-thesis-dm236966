#!/usr/bin/env python3
import os
import glob
import pandas as pd

def merge_csvs(folder_path, output_root="merged_csvs"):
    """Merge all CSVs in a single folder and save with a Label column."""
    label = os.path.basename(os.path.normpath(folder_path))
    os.makedirs(output_root, exist_ok=True)

    pattern = os.path.join(folder_path, '*.csv')
    csv_files = glob.glob(pattern)
    if not csv_files:
        print(f"⚠️  No CSV files found in folder: {folder_path}")
        return

    dfs = []
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file)
            df["Label"] = label
            dfs.append(df)
        except Exception as e:
            print(f"❌ Error reading {csv_file}: {e}")

    if not dfs:
        print(f"⚠️  No valid CSVs to merge in {folder_path}")
        return

    merged_df = pd.concat(dfs, ignore_index=True)
    output_filename = f"{label}_merged.csv"
    output_path = os.path.join(output_root, output_filename)
    merged_df.to_csv(output_path, index=False)
    print(f"✅ Merged {len(csv_files)} files into {output_path}")

def main():
    root_dir = "cic_iomt2024_grouped"
    output_root = "merged_csvs"

    # Create the output folder
    os.makedirs(output_root, exist_ok=True)

    # Iterate through all subdirectories of cic_iomt2024_grouped
    subfolders = [
        os.path.join(root_dir, d)
        for d in os.listdir(root_dir)
        if os.path.isdir(os.path.join(root_dir, d))
    ]

    if not subfolders:
        print(f"No subfolders found in {root_dir}")
        return

    print(f"Found {len(subfolders)} folders in {root_dir}. Beginning merge…")

    for folder in subfolders:
        merge_csvs(folder, output_root)

    print("\n🎉 All folders processed. Merged CSVs saved in:", output_root)

if __name__ == "__main__":
    main()
