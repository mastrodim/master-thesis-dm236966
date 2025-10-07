#!/usr/bin/env python3
"""
add_label_inplace.py

Add a 'Label' column to all CSVs in a folder, overwriting the files in place.
Label value is derived from the filename (stem by default, or full name with --include-ext).
"""

import os
import glob
import argparse
import pandas as pd
import tempfile

def add_label_inplace(file_path: str, include_extension: bool = False) -> None:
    # Read the CSV
    df = pd.read_csv(file_path)

    # Determine label from filename
    basename = os.path.basename(file_path)
    label = basename if include_extension else os.path.splitext(basename)[0]

    # Add or overwrite the 'Label' column
    df["Label"] = label

    # Write to a temp file in the same directory, then atomically replace
    dirpath = os.path.dirname(file_path)
    fd, tmp_path = tempfile.mkstemp(prefix=".label_tmp_", suffix=".csv", dir=dirpath)
    os.close(fd)
    try:
        df.to_csv(tmp_path, index=False)
        os.replace(tmp_path, file_path)  # atomic overwrite on most OSes
        print(f"✔ Updated (in-place): {file_path}  [Label='{label}']")
    except Exception as e:
        # Clean up temp file on failure
        try:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        finally:
            raise e

def main():
    parser = argparse.ArgumentParser(
        description="Add a 'Label' column to all CSVs in a directory (overwrite in place)."
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default="csv_files",
        help="Directory containing CSV files (default: ./csv_files)"
    )
    parser.add_argument(
        "--include-ext",
        action="store_true",
        help="Use the full filename (including .csv) as the label value"
    )
    args = parser.parse_args()

    pattern = os.path.join(args.directory, "*.csv")
    csv_files = sorted(glob.glob(pattern))
    if not csv_files:
        print(f"No CSV files found in {args.directory!r}.")
        return

    for file_path in csv_files:
        try:
            add_label_inplace(file_path, include_extension=args.include_ext)
        except Exception as e:
            print(f"✖ Failed to process {file_path}: {e}")

if __name__ == "__main__":
    main()
