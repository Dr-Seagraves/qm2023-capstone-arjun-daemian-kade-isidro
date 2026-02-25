"""
Script to load and clean the CPI2025_Results.csv Dataset
--------------------------------------------------------

This script reads the raw CPI2025_Results.csv file (Corruption Perceptions
Index 2025 with historical data back to 2012), removes unnecessary header
rows, cleans the data, and writes a cleaned CSV to the processed data directory.

The raw file has:
- Row 1: Title row with comma separation artifacts
- Row 2: EMBARGOED notice
- Row 3: Empty row
- Row 4: Actual column headers
- Row 5+: Data

Usage: run from the repo root or via the code/ module runner.
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

from config_paths import RAW_DATA_DIR, PROCESSED_DATA_DIR, ensure_directories

# Ensure directories exist
ensure_directories()

RAW_FILE = RAW_DATA_DIR / "CPI2025_Results.csv"
PROCESSED_FILE = PROCESSED_DATA_DIR / "CPI2025_Results_clean.csv"


def load_raw_cpi_data(filepath: Path) -> pd.DataFrame:
    """
    Load the raw CPI2025_Results.csv file.
    
    The file has 3 header/metadata rows before the actual column names.
    We skip these and use row 3 (zero-indexed) as the header.
    
    Parameters
    ----------
    filepath : Path
        Path to the raw CPI CSV file
        
    Returns
    -------
    pd.DataFrame
        Raw dataframe with proper column headers
    """
    if not filepath.exists():
        raise FileNotFoundError(
            f"Raw CPI file not found at {filepath}\n"
            f"Please ensure CPI2025_Results.csv exists in {RAW_DATA_DIR}"
        )
    
    print(f"Loading raw CPI data from {filepath}")
    
    # Skip first 3 rows (title, embargo notice, blank line)
    # Row 4 (index 3) contains the actual column headers
    df = pd.read_csv(filepath, skiprows=3)
    
    print(f"  Loaded {len(df)} rows and {len(df.columns)} columns")
    
    return df


def clean_cpi_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the CPI dataframe.
    
    Cleaning steps:
    1. Strip whitespace from column names
    2. Remove completely empty rows
    3. Remove completely empty columns
    4. Convert numeric columns to appropriate types
    5. Handle missing values appropriately
    
    Parameters
    ----------
    df : pd.DataFrame
        Raw CPI dataframe
        
    Returns
    -------
    pd.DataFrame
        Cleaned dataframe
    """
    print("Cleaning CPI data...")
    
    # 1. Strip whitespace from column names
    df.columns = df.columns.str.strip()
    
    # 2. Remove completely empty rows
    rows_before = len(df)
    df = df.dropna(how='all')
    rows_removed = rows_before - len(df)
    if rows_removed > 0:
        print(f"  Removed {rows_removed} completely empty rows")
    
    # 3. Remove completely empty columns
    cols_before = len(df.columns)
    df = df.dropna(axis=1, how='all')
    cols_removed = cols_before - len(df.columns)
    if cols_removed > 0:
        print(f"  Removed {cols_removed} completely empty columns")
    
    # 4. Convert numeric columns (scores, ranks, sources, standard errors) to numeric
    # Identify numeric columns by pattern matching
    numeric_patterns = ['score', 'rank', 'sources', 'standard error', 'Score', 'Rank', 'Sources', 'Standard error']
    
    for col in df.columns:
        if any(pattern in col for pattern in numeric_patterns):
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # 5. Sort by country name for consistency
    if 'Country / Territory' in df.columns:
        df = df.sort_values('Country / Territory').reset_index(drop=True)
        print(f"  Sorted by country/territory")
    
    print(f"  Final shape: {len(df)} rows × {len(df.columns)} columns")
    
    return df


def save_cleaned_data(df: pd.DataFrame, filepath: Path) -> None:
    """
    Save the cleaned dataframe to CSV.
    
    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataframe
    filepath : Path
        Output filepath
    """
    print(f"Saving cleaned data to {filepath}")
    df.to_csv(filepath, index=False)
    print(f"  ✓ Saved {len(df)} rows to {filepath.name}")


def main():
    """Main execution function."""
    print("="*70)
    print("CPI 2025 Data Cleaning Pipeline")
    print("="*70)
    
    # 1. Load raw data
    df_raw = load_raw_cpi_data(RAW_FILE)
    
    # 2. Clean data
    df_clean = clean_cpi_data(df_raw)
    
    # 3. Save cleaned data
    save_cleaned_data(df_clean, PROCESSED_FILE)
    
    print("\n" + "="*70)
    print("✓ CPI data cleaning complete!")
    print("="*70)
    
    # 4. Display summary info
    print("\nSummary:")
    print(f"  Countries/Territories: {len(df_clean)}")
    if 'Country / Territory' in df_clean.columns:
        print(f"  First country: {df_clean['Country / Territory'].iloc[0]}")
        print(f"  Last country: {df_clean['Country / Territory'].iloc[-1]}")
    if 'CPI score 2025' in df_clean.columns:
        print(f"  2025 CPI scores available: {df_clean['CPI score 2025'].notna().sum()}")
    
    return df_clean


if __name__ == "__main__":
    df = main()
