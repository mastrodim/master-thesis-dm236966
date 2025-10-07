#!/usr/bin/env python3
"""
rename.py

Rename specific CSV files inside the csv_files folder, overwriting targets if they exist.

Usage:
    python rename.py                  # shows planned actions, asks for confirmation
    python rename.py --yes            # proceed without confirmation
    python rename.py --dry-run        # show planned actions but do not perform them
    python rename.py --folder path    # operate on a different folder (default: ./csv_files)
"""

import os
import argparse
import glob

# Mapping from current filename -> desired filename (now that files live in csv_files/)
RENAME_MAP = {
    "bruteforce.csv":          "Bruteforce.csv",
    "capture_1w.csv":          "Legitimate.csv",
    "capture_flood.csv":       "Flooding.csv",
    "capture_malariaDoS.csv":  "DoS Attack.csv",
    "malformed.csv":           "Malformed.csv",
    "slowite.csv":             "slowITe.csv",
}

def find_files_to_rename(folder):
    actions = []
    for src, dst in RENAME_MAP.items():
        src_path = os.path.join(folder, src)
        dst_path = os.path.join(folder, dst)

        if os.path.exists(src_path):
            actions.append((src_path, dst_path))
        else:
            # case-insensitive match to be robust
            matches = [
                p for p in glob.glob(os.path.join(folder, "*"))
                if os.path.isfile(p) and os.path.basename(p).lower() == src.lower()
            ]
            if matches:
                actions.append((matches[0], dst_path))
            else:
                actions.append((None, dst_path))
    return actions

def main(folder="csv_files", yes=False, dry_run=False):
    folder = os.path.abspath(folder)
    os.makedirs(folder, exist_ok=True)

    rename_actions = find_files_to_rename(folder)

    print(f"\nWorking folder: {folder}\n")
    print("Planned rename actions (OVERWRITE if target exists):")
    any_exist = False
    for src, dst in rename_actions:
        if src is None:
            print(f"  - SKIP (source not found) -> target would be: {os.path.basename(dst)}")
        else:
            any_exist = True
            print(f"  - {os.path.basename(src)}  ->  {os.path.basename(dst)}")
    if not any_exist:
        print("  (No source CSV files found among the list.)")

    if dry_run:
        print("\nDry run requested: no changes will be made.")
        return

    if not yes:
        resp = input("\nProceed with the above actions (targets will be overwritten)? [y/N] ").strip().lower()
        if resp not in ("y", "yes"):
            print("Aborted by user. No changes made.")
            return

    # Perform renames (overwrite enabled)
    for src, dst in rename_actions:
        if src is None:
            continue
        try:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            # Atomic overwrite if dst exists
            os.replace(src, dst)
            print(f"Renamed: {os.path.basename(src)} -> {os.path.basename(dst)}")
        except Exception as e:
            print(f"ERROR renaming {src} -> {dst}: {e}")

    print("\nDone.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rename specified CSV files inside csv_files (overwrite targets).")
    parser.add_argument("--folder", "-f", default="csv_files", help="Folder to operate on (default: ./csv_files).")
    parser.add_argument("--yes", "-y", action="store_true", help="Proceed without confirmation.")
    parser.add_argument("--dry-run", action="store_true", help="Only show planned actions; do not perform them.")
    args = parser.parse_args()
    main(folder=args.folder, yes=args.yes, dry_run=args.dry_run)
