"""
Corruption Perceptions Index (CPI) Data Processing and Import Guide

This module provides utilities to work with CPI data from Transparency International.
The CPI is published annually and ranks countries by perceived corruption levels.

Since CPI data requires manual download, this script provides:
1. A standardized template for organizing downloaded data
2. Processing functions to reshape CPI data
3. Validation and cleaning utilities
"""

import pandas as pd
import os
from pathlib import Path


def create_cpi_raw_template():
    """
    Create a raw data template matching Transparency International CPI export format.
    
    Returns:
        pd.DataFrame: Template with expected columns
    """
    template = pd.DataFrame({
        'Rank': [1, 2, 3],
        'Country': ['Denmark', 'Finland', 'New Zealand'],
        'CPI_Score': [90, 89, 88],
        'Region': ['Europe & Central Asia', 'Europe & Central Asia', 'East Asia & Pacific'],
        'Year': [2023, 2023, 2023],
        'Number_of_Sources': [7, 7, 7],
        'Standard_Error': [1.2, 1.1, 1.3]
    })
    return template


def process_cpi_data(input_path, output_path, year_range=(2012, 2024)):
    """
    Process raw CPI data from Transparency International exports.
    
    Args:
        input_path: Path to raw CPI CSV file
        output_path: Path to save processed CPI data
        year_range: Tuple of (start_year, end_year)
    """
    print(f"Processing CPI data from {input_path}...")
    
    # Read CPI data
    cpi = pd.read_csv(input_path)
    
    # Standardize column names
    cpi.columns = cpi.columns.str.lower().str.strip()
    
    # Filter to year range
    if 'year' in cpi.columns:
        cpi = cpi[(cpi['year'] >= year_range[0]) & (cpi['year'] <= year_range[1])]
    
    # Ensure required columns
    required_cols = ['country', 'year', 'cpi_score']
    for col in required_cols:
        if col not in cpi.columns:
            raise ValueError(f"Missing required column: {col}")
    
    # Select and rename key columns
    cpi = cpi[['country', 'year', 'cpi_score']].copy()
    cpi.columns = ['Country', 'Year', 'CPI_Score']
    
    # Clean data
    cpi['Year'] = pd.to_numeric(cpi['Year'], errors='coerce')
    cpi['CPI_Score'] = pd.to_numeric(cpi['CPI_Score'], errors='coerce')
    cpi = cpi.dropna(subset=['Year', 'CPI_Score'])
    cpi = cpi.sort_values(['Country', 'Year']).reset_index(drop=True)
    
    # Save processed data
    cpi.to_csv(output_path, index=False)
    print(f"Processed CPI data saved to {output_path}")
    print(f"Records: {len(cpi)}")
    print(f"Countries: {cpi['Country'].nunique()}")
    print(f"Years: {cpi['Year'].min():.0f}-{cpi['Year'].max():.0f}")
    
    return cpi


def create_cpi_wide_format(input_path, output_path):
    """
    Convert CPI data from long format (years as rows) to wide format (years as columns).
    
    Args:
        input_path: Path to processed CPI CSV (long format)
        output_path: Path to save wide format CSV
    """
    print(f"Converting CPI to wide format...")
    
    cpi = pd.read_csv(input_path)
    
    # Pivot to wide format
    cpi_wide = cpi.pivot(index='Country', columns='Year', values='CPI_Score')
    cpi_wide = cpi_wide.reset_index()
    
    # Save
    cpi_wide.to_csv(output_path, index=False)
    print(f"Wide format CPI saved to {output_path}")
    print(f"Shape: {cpi_wide.shape}")
    
    return cpi_wide


def print_cpi_download_instructions():
    """Print detailed instructions for downloading CPI data."""
    
    instructions = """
    ╔════════════════════════════════════════════════════════════════════════════╗
    ║                 HOW TO DOWNLOAD CPI DATA                                   ║
    ╚════════════════════════════════════════════════════════════════════════════╝
    
    OPTION 1: Official Transparency International Website (RECOMMENDED)
    ─────────────────────────────────────────────────────────────────────
    1. Visit: https://www.transparency.org/en/cpi/
    2. Look for "Data & Findings" or "Download Data" section
    3. Download the CPI rankings for 2012-present as CSV or Excel
    4. Save to: data/raw/corruption_perceptions_index_raw.csv
    
    Expected columns: Country, Year, CPI_Score, Rank, Region, Standard_Error
    
    
    OPTION 2: World Bank Data Bank
    ──────────────────────────────
    1. Visit: https://databank.worldbank.org/
    2. Search for governance or corruption indicators
    3. Select countries and years (2012-2024)
    4. Download as CSV
    5. Save to: data/raw/corruption_perceptions_index_raw.csv
    
    
    OPTION 3: Kaggle Datasets
    ─────────────────────────
    1. Visit: https://www.kaggle.com/datasets
    2. Search: "corruption perceptions index"
    3. Download relevant dataset
    4. Extract and save to: data/raw/corruption_perceptions_index_raw.csv
    
    
    ─────────────────────────────────────────────────────────────────────
    AFTER DOWNLOADING:
    ─────────────────────────────────────────────────────────────────────
    
    1. Place the file in: data/raw/corruption_perceptions_index_raw.csv
    
    2. Process the data using:
       python src/process_cpi_data.py
    
    3. This will create:
       - data/processed/corruption_perceptions_index_processed.csv
       - data/processed/corruption_perceptions_index_wide.csv
    
    
    ─────────────────────────────────────────────────────────────────────
    DATA REQUIREMENTS:
    ─────────────────────────────────────────────────────────────────────
    
    Minimum columns needed:
    • Country (or Country Name)
    • Year
    • CPI_Score (or Corruption Perception Index Score)
    
    Optional columns (will be retained):
    • Rank
    • Region
    • Standard_Error
    • Number_of_Sources
    
    """
    
    print(instructions)


def create_processing_script():
    """Create the main processing script for CPI data."""
    
    script_content = '''#!/usr/bin/env python
"""Main script to process downloaded CPI data."""

import sys
sys.path.insert(0, '/workspaces/qm2023-capstone-arjun-daemian-kade-isidro')

from src.process_cpi_data import (
    process_cpi_data, 
    create_cpi_wide_format,
    print_cpi_download_instructions
)
import os

def main():
    raw_dir = 'data/raw'
    processed_dir = 'data/processed'
    
    # Ensure directories exist
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(processed_dir, exist_ok=True)
    
    raw_file = f'{raw_dir}/corruption_perceptions_index_raw.csv'
    processed_file = f'{processed_dir}/corruption_perceptions_index_processed.csv'
    wide_file = f'{processed_dir}/corruption_perceptions_index_wide.csv'
    
    # Check if raw data exists
    if not os.path.exists(raw_file):
        print(f"Raw CPI file not found: {raw_file}")
        print()
        print_cpi_download_instructions()
        return
    
    # Process data
    print("="*70)
    print("PROCESSING CORRUPTION PERCEPTIONS INDEX DATA")
    print("="*70)
    
    cpi = process_cpi_data(raw_file, processed_file)
    print()
    
    # Create wide format
    cpi_wide = create_cpi_wide_format(processed_file, wide_file)
    
    print()
    print("✓ CPI data processing complete!")
    print(f"  Processed: {processed_file}")
    print(f"  Wide format: {wide_file}")

if __name__ == '__main__':
    main()
'''
    
    return script_content


if __name__ == '__main__':
    print_cpi_download_instructions()
    
    # Create template
    template = create_cpi_raw_template()
    template_path = 'data/raw/CPI_template.csv'
    os.makedirs('data/raw', exist_ok=True)
    template.to_csv(template_path, index=False)
    print(f"✓ Template created: {template_path}")
