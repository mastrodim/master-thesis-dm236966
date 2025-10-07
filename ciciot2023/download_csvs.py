#!/usr/bin/env python3
"""
download_csvs.py

Downloads all CSV files from a given directory listing URL into a local folder.
"""

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_csvs(base_url, output_dir):
    """
    Download all .csv files linked from the HTML at base_url into output_dir.
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    print(f"Fetching directory listing from {base_url} …")
    resp = requests.get(base_url)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    links = soup.find_all("a")

    csv_links = [link.get("href") for link in links if link.get("href", "").lower().endswith(".csv")]
    if not csv_links:
        print("No CSV files found at that URL.")
        return

    print(f"Found {len(csv_links)} CSV files. Beginning downloads…")
    for href in csv_links:
        file_url = urljoin(base_url, href)
        local_path = os.path.join(output_dir, href)

        # Skip if already downloaded
        if os.path.exists(local_path):
            print(f"  • Skipping {href} (already exists)")
            continue

        print(f"  • Downloading {href} …")
        with requests.get(file_url, stream=True) as r:
            r.raise_for_status()
            with open(local_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
    print("All done!")

if __name__ == "__main__":
    BASE_URL = "http://cicresearch.ca/IOTDataset/CIC_IOT_Dataset2023/Dataset/CSV/MERGED_CSV/"
    OUTPUT_DIR = "ciciot2023_csvs"

    download_csvs(BASE_URL, OUTPUT_DIR)
