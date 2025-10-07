#!/usr/bin/env python3
"""
replace_labels.py

Reads combined/combined_ciciot2023_filtered.csv, replaces specific values in the
'Label' column according to the provided mapping, writes to
combined/combined_ciciot2023_filtered_relabelled.csv (overwrite if exists),
then deletes the original filtered file.

Input:
  ./combined/combined_ciciot2023_filtered.csv

Output:
  ./combined/combined_ciciot2023_filtered_relabelled.csv
"""

import os
import sys
import pandas as pd

COMBINED_DIR = "combined"
INPUT_NAME   = "combined_ciciot2023_filtered.csv"
BASE, EXT    = os.path.splitext(INPUT_NAME)
OUTPUT_NAME  = f"{BASE}_relabelled{EXT}"

input_path   = os.path.join(COMBINED_DIR, INPUT_NAME)
output_path  = os.path.join(COMBINED_DIR, OUTPUT_NAME)

# Mapping of old labels -> new labels
label_mapping = {
    "DDOS-UDP_FLOOD": "DDoS_UDP",
    "DDOS-ICMP_FLOOD": "DDoS_ICMP",
    "DDOS-TCP_FLOOD": "DDoS_TCP",
    "DDOS-SYN_FLOOD": "DDoS_SYN",
    "DDOS-PSHACK_FLOOD": "DDoS-PSHACK_FLOOD",
    "DDOS-SYNONYMOUSIP_FLOOD": "DDoS-SYNONYMOUSIP_FLOOD",
    "DICTIONARYBRUTEFORCE": "Bruteforce",
    "DDOS-ICMP_FRAGMENTATION": "DDoS-ICMP_FRAGMENTATION",
    "DDOS-UDP_FRAGMENTATION": "DDoS-UDP_FRAGMENTATION",
    "DDOS-ACK_FRAGMENTATION": "DDoS-ACK_FRAGMENTATION",
    "DDOS-RSTFINFLOOD": "DDoS-RSTFINFLOOD",
    "RECON-HOSTDISCOVERY": "Recon-HOSTDISCOVERY ",
    "DOS-HTTP_FLOOD": "DoS-HTTP_FLOOD",
    "DDOS-HTTP_FLOOD": "DDoS-HTTP_FLOOD",
    "DDOS-SLOWLORIS": "DDoS-SLOWLORIS",
    "BENIGN": "Benign",
    "MITM-ARPSPOOFING": "Spoofing_ARP",
    "DNS_SPOOFING": "Spoofing_DNS",
    "DOS-TCP_FLOOD": "DoS_TCP",
    "DOS-SYN_FLOOD": "DoS_SYN",
    "DOS-UDP_FLOOD": "DoS_UDP",
    "COMMANDINJECTION": "Web_Based_COMMANDINJECTION",
    "BACKDOOR_MALWARE": "Web_Based_BACKDOOR_MALWARE",
    "RECON-PINGSWEEP": "Recon_Ping_Sweep",
    "RECON-OSSCAN": "Recon_OS_Scan",
    "VULNERABILITYSCAN": "Recon_Vulnerability_Scan",
    "RECON-PORTSCAN": "Recon_Port_Scan",
}

def main():
    if not os.path.isdir(COMBINED_DIR):
        sys.exit(f"Folder not found: {COMBINED_DIR}")
    if not os.path.isfile(input_path):
        sys.exit(f"Input CSV not found: {input_path}")

    df = pd.read_csv(input_path)

    if "Label" not in df.columns:
        sys.exit("Error: 'Label' column not found in the CSV.")

    # Optional: trim whitespace before replacing
    df["Label"] = df["Label"].astype(str).str.strip()

    # Replace labels
    df["Label"] = df["Label"].replace(label_mapping)

    # Write relabelled file (overwrite if exists)
    df.to_csv(output_path, index=False)

    # Remove the original filtered file so only *_relabelled.csv remains
    try:
        os.remove(input_path)
    except Exception as e:
        print(f"Warning: could not remove original file {input_path}: {e}")

    print(f"Relabelled CSV saved to {output_path}")

if __name__ == "__main__":
    main()
