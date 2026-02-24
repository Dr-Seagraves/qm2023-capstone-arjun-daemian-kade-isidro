"""
Script to download, load and clean the Policy Uncertainty Dataset
---------------------------------------------------------------

This script downloads the All_Country_Data.xlsx file from
https://www.policyuncertainty.com/media/All_Country_Data.xlsx, validates
the download, reads it with pandas, selects only the rows for January 2012,
removes duplicate China columns (keeping the first), and writes a cleaned
CSV to the processed data directory.

Usage: run from the repo root or via the code/ module runner.
"""

import sys
from pathlib import Path
import pandas as pd

from config_paths import RAW_DATA_DIR, PROCESSED_DATA_DIR, ensure_directories

# Ensure directories exist
ensure_directories()

DATA_URL = "https://www.policyuncertainty.com/media/All_Country_Data.xlsx"
RAW_FILE = RAW_DATA_DIR / "All_Country_Data.xlsx"
PROCESSED_FILE = PROCESSED_DATA_DIR / "january_2012_onwards.csv"


def download_file(url: str, target: Path, min_size: int = 1024) -> None:
    """Download file with requests and do a basic size check."""
    try:
        import requests
    except Exception:
        raise SystemExit("Please install 'requests' (pip install requests) to download datasets.")

    print(f"Downloading {url} -> {target}")
    try:
        resp = requests.get(url, stream=True, timeout=30)
        resp.raise_for_status()
        with open(target, "wb") as fh:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    fh.write(chunk)
    except Exception as e:
        raise SystemExit(f"Download failed: {e}")

    size = target.stat().st_size
    if size < min_size:
        target.unlink(missing_ok=True)
        raise SystemExit(f"Downloaded file is too small ({size} bytes). Aborting.")


def ensure_openpyxl():
    try:
        import openpyxl  # noqa: F401
    except Exception:
        raise SystemExit("Missing dependency: install openpyxl (pip install openpyxl)")


def load_excel(path: Path) -> pd.DataFrame:
    ensure_openpyxl()
    try:
        df = pd.read_excel(path)
    except Exception as e:
        raise SystemExit(f"Failed to read Excel file '{path}': {e}")
    return df


def select_from_january_2012(df: pd.DataFrame) -> pd.DataFrame:
    # Prefer explicit Year/Month columns
    if 'Year' in df.columns and 'Month' in df.columns:
        df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
        df['Month'] = pd.to_numeric(df['Month'], errors='coerce')
        sel = df[(df['Year'] > 2012) | ((df['Year'] == 2012) & (df['Month'] >= 1))].copy()
        return sel

    # Try to infer from a Date column
    if 'Date' in df.columns:
        parsed = pd.to_datetime(df['Date'], errors='coerce')
        df['Year'] = parsed.dt.year
        df['Month'] = parsed.dt.month
        return df[(df['Year'] > 2012) | ((df['Year'] == 2012) & (df['Month'] >= 1))].copy()

    raise SystemExit("Unable to find Year/Month/Date columns to select from January 2012 onwards")


def drop_duplicate_china_columns(df: pd.DataFrame) -> pd.DataFrame:
    # find columns with 'china' (case-insensitive)
    china_cols = [c for c in df.columns if 'china' in c.lower()]
    if len(china_cols) <= 1:
        print("No duplicate China columns found or only one China column present.")
        return df

    # keep the first occurrence, drop subsequent ones if present in df
    to_drop = [c for c in china_cols[1:] if c in df.columns]
    if to_drop:
        print(f"Dropping duplicate China columns: {to_drop}")
        df = df.drop(columns=to_drop)
    else:
        print("Duplicate China columns detected but none present in current frame to drop.")
    return df


def main():
    print("POLICY UNCERTAINTY: download -> extract January 2012+ -> clean -> save")

    if not RAW_FILE.exists():
        download_file(DATA_URL, RAW_FILE)
    else:
        print(f"Using existing raw file: {RAW_FILE}")

    df = load_excel(RAW_FILE)
    print(f"Loaded sheet with {len(df)} rows and {len(df.columns)} columns")

    df_jan2012 = select_from_january_2012(df)
    print(f"Selected {len(df_jan2012)} rows from January 2012 onwards")

    df_clean = drop_duplicate_china_columns(df_jan2012)

    PROCESSED_FILE.parent.mkdir(parents=True, exist_ok=True)
    df_clean.to_csv(PROCESSED_FILE, index=False)
    print(f"Saved cleaned file to {PROCESSED_FILE} ({PROCESSED_FILE.stat().st_size} bytes)")


if __name__ == '__main__':
    main()
