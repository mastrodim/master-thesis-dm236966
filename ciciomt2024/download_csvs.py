#!/usr/bin/env python3
"""
download_csvs.py

Downloads CSV files from the CICIoMT2024 WiFi & MQTT attack train/test
directories and places them into folders according to the filename patterns
you specified.

Folder mapping (best-effort, case-insensitive):
  - Benign -> filenames containing "benign"
  - DDoS_ICMP -> filenames containing "dDoS-ICMP" or "tcp_ip-ddos-icmp"
  - DDoS_SYN -> filenames containing "dDoS-SYN" or "tcp_ip-ddos-syn"
  - DDoS_TCP -> filenames containing "dDoS-TCP" or "tcp_ip-ddos-tcp" or "tcp_test"
  - DDoS_UDP -> filenames containing "dDoS-UDP" or "tcp_ip-ddos-udp"
  - DoS_ICMP -> filenames containing "DoS-ICMP"
  - DoS_SYN -> filenames containing "DoS-SYN"
  - DoS_TCP -> filenames containing "DoS-TCP"
  - DoS_UDP -> filenames containing "DoS-UDP"
  - MQTT_DDoS_Flooding -> filenames containing "MQTT-DDoS"
  - MQTT_DoS_Flooding -> filenames containing "MQTT-DoS"
  - MQTT_Malformed_Data -> filenames containing "MQTT-Malformed"
  - Recon_OS_Scan -> filenames containing "Recon-OS_Scan" or "Recon-OS"
  - Recon_Ping_Sweep -> filenames containing "Recon-Ping"
  - Recon_Port_Scan -> filenames containing "Recon-Port"
  - Recon_Vulnerability_Scan -> filenames containing "Recon-VulScan"
  - SPOOFING -> filenames containing "ARP_Spoofing"
  - other -> anything that doesn't match above
"""
import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pathlib import Path

TRAIN_URL = "http://cicresearch.ca/IOTDataset/CICIoMT2024/Dataset/WiFI_and_MQTT/attacks/CSV/train/"
TEST_URL  = "http://cicresearch.ca/IOTDataset/CICIoMT2024/Dataset/WiFI_and_MQTT/attacks/CSV/test/"

# Precompiled regex patterns (case-insensitive)
PATTERNS = [
    (re.compile(r"benign", re.I), "Benign"),
    (re.compile(r"(tcp[_\-]?ip[_\-]?ddos[_\-]?icmp|ddos[_\-]?icmp|ddos_icmp)", re.I), "DDoS_ICMP"),
    (re.compile(r"(tcp[_\-]?ip[_\-]?ddos[_\-]?syn|ddos[_\-]?syn|ddos_syn)", re.I), "DDoS_SYN"),
    (re.compile(r"(tcp[_\-]?ip[_\-]?ddos[_\-]?tcp|ddos[_\-]?tcp|ddos_tcp|tcp[_\-]?test)", re.I), "DDoS_TCP"),
    (re.compile(r"(tcp[_\-]?ip[_\-]?ddos[_\-]?udp|ddos[_\-]?udp|ddos_udp)", re.I), "DDoS_UDP"),
    (re.compile(r"dos[_\-]?icmp|DoS-ICMP", re.I), "DoS_ICMP"),
    (re.compile(r"dos[_\-]?syn|DoS-SYN", re.I), "DoS_SYN"),
    (re.compile(r"dos[_\-]?tcp|DoS-TCP", re.I), "DoS_TCP"),
    (re.compile(r"dos[_\-]?udp|DoS-UDP", re.I), "DoS_UDP"),
    (re.compile(r"mqtt[_\-]?ddos|MQTT-DDoS", re.I), "MQTT_DDoS_Flooding"),
    (re.compile(r"mqtt[_\-]?dos|MQTT-DoS", re.I), "MQTT_DoS_Flooding"),
    (re.compile(r"mqtt[_\-]?malformed|MQTT-Malformed", re.I), "MQTT_Malformed_Data"),
    (re.compile(r"recon[_\-]?os[_\-]?scan|recon[_\-]?os|Recon-OS_Scan", re.I), "Recon_OS_Scan"),
    (re.compile(r"recon[_\-]?ping|Recon-Ping", re.I), "Recon_Ping_Sweep"),
    (re.compile(r"recon[_\-]?port|Recon-Port", re.I), "Recon_Port_Scan"),
    (re.compile(r"recon[_\-]?vulscan|Recon[_\-]?VulScan", re.I), "Recon_Vulnerability_Scan"),
    (re.compile(r"arp[_\-]?spoofing|ARP_Spoofing", re.I), "SPOOFING"),
]

def list_csv_links(base_url: str) -> list[str]:
    """Return list of CSV hrefs from a directory listing page."""
    print(f"Fetching directory listing from {base_url} …")
    r = requests.get(base_url)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    links = soup.find_all("a")
    hrefs = [link.get("href") for link in links if link.get("href") and link.get("href").lower().endswith(".csv")]
    # Remove query fragments or anchors (if any)
    hrefs = [h.split('#')[0].split('?')[0] for h in hrefs]
    return hrefs

def map_to_folder(filename: str) -> str:
    """Return the folder name for a given filename using PATTERNS order."""
    for pat, folder in PATTERNS:
        if pat.search(filename):
            return folder
    return "other"

def safe_download(url: str, dest_path: str) -> None:
    """Download URL to dest_path (skip if exists)."""
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    if os.path.exists(dest_path):
        print(f"  • Skipping {os.path.basename(dest_path)} (exists)")
        return
    print(f"  • Downloading {os.path.basename(dest_path)} …")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(dest_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

def download_split(base_url: str, output_root: str, split_tag: str) -> int:
    """
    Download all CSVs from base_url into output_root/<folder>/ with
    filenames prefixed by split_tag (train_/test_).
    Returns number of files processed.
    """
    hrefs = list_csv_links(base_url)
    if not hrefs:
        print(f"No CSV files found at {base_url}")
        return 0
    print(f"Found {len(hrefs)} CSVs at {base_url} — saving as {split_tag}_<filename>")
    count = 0
    for href in hrefs:
        full_url = urljoin(base_url, href)
        basename = Path(href).name
        folder = map_to_folder(basename)
        local_name = f"{split_tag}_{basename}"
        dest = os.path.join(output_root, folder, local_name)
        safe_download(full_url, dest)
        count += 1
    return count

def download_train_and_test(output_root: str = "cic_iomt2024_grouped"):
    os.makedirs(output_root, exist_ok=True)
    t1 = download_split(TRAIN_URL, output_root, "train")
    t2 = download_split(TEST_URL, output_root, "test")
    print(f"Done. Train: {t1} files, Test: {t2} files. Root folder: {output_root}")

if __name__ == "__main__":
    download_train_and_test("cic_iomt2024_grouped")
