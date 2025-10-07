#!/usr/bin/env python3
import os
import pandas as pd

INPUT_DIR = "csv_files"

# Use LOWERCASE keys here (human-friendly values on the right stay as-is)
LABEL_MAP = {
    "legitimate":   "Benign",
    "slowite":      "MQTT_SlowITe",
    "bruteforce":   "MQTT_Bruteforce",
    "malformed":    "MQTT_Malformed_Data",
    "flooding":     "MQTT_DoS_Flooding",
    "dos attack":   "MQTT_DoS_Attack",
}

def normalize_key(s: str) -> str:
    # lower, turn _ and - into spaces, collapse multiple spaces
    s = s.lower().replace("_", " ").replace("-", " ").strip()
    return " ".join(s.split())

# Build normalized map once
NORM_LABEL_MAP = {normalize_key(k): v for k, v in LABEL_MAP.items()}

def main():
    if not os.path.isdir(INPUT_DIR):
        print(f"Error: directory {INPUT_DIR!r} not found.")
        return

    files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".csv")]
    if not files:
        print(f"No CSV files found in {INPUT_DIR!r}.")
        return

    for fname in sorted(files):
        stem_raw = os.path.splitext(fname)[0]
        stem = normalize_key(stem_raw)

        if stem not in NORM_LABEL_MAP:
            print(f"  ↳ no mapping for '{stem_raw}' (normalized '{stem}'), skipping {fname}")
            continue

        label_value = NORM_LABEL_MAP[stem]
        path = os.path.join(INPUT_DIR, fname)

        try:
            df = pd.read_csv(path)
        except Exception as e:
            print(f"  ✖ failed to read {fname}: {e}")
            continue

        df["Label"] = label_value  # overwrite or create

        try:
            df.to_csv(path, index=False)
            print(f"  ✓ {fname}: set Label → '{label_value}' (overwritten)")
        except Exception as e:
            print(f"  ✖ failed to write {fname}: {e}")

if __name__ == "__main__":
    main()
