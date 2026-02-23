"""
Merge Foreign Direct Investment (FDI) and Crime Index data.
Combines datasets by country and year.
"""

import pandas as pd
import numpy as np
import os


def create_country_name_mapping():
    """
    Create a mapping between FDI country names and Crime Index country names.
    This handles differences in naming conventions.
    """
    mapping = {
        # Crime Index name -> FDI name (standardized form)
        'Bahamas': 'Bahamas, The',
        'Bosnia And Herzegovina': 'Bosnia and Herzegovina',
        'Czech Republic': 'Czechia',
        'Ivory Coast': 'Cote d\'Ivoire',
        'Congo, Dem. Rep.': 'Democratic Republic of the Congo',
        'Egypt': 'Egypt, Arab Rep.',
        'Hong Kong (China)': 'Hong Kong SAR, China',
        'Iran': 'Iran, Islamic Rep.',
        'Isle Of Man': 'Isle of Man',
        'Kosovo (Disputed Territory)': 'Kosovo',
        'Macao (China)': 'Macao SAR, China',
        'Korea, Dem. People\'s Rep.': 'North Korea',
        'North Macedonia': 'North Macedonia',
        'Palestine': 'West Bank and Gaza',
        'Puerto Rico': 'Puerto Rico (US)',
        'Russia': 'Russian Federation',
        'South Korea': 'Korea, Rep.',
        'Syria': 'Syrian Arab Republic',
        'Taiwan': 'Taiwan',
        'Trinidad And Tobago': 'Trinidad and Tobago',
        'Turkey': 'Turkiye',
        'Us Virgin Islands': 'Virgin Islands (U.S.)',
        'United Arab Emirates': 'United Arab Emirates',
        'United Kingdom': 'United Kingdom',
        'United States': 'United States',
        'Venezuela': 'Venezuela, RB',
        'Vietnam': 'Viet Nam',
        'Yemen': 'Yemen, Rep.',
    }
    return mapping


def merge_fdi_crime_data(fdi_path, crime_path, output_path):
    """
    Merge FDI and Crime Index datasets.
    
    Args:
        fdi_path: Path to FDI CSV (countries × years format)
        crime_path: Path to Crime Index CSV (years × countries format)
        output_path: Path to save merged CSV (long format)
    """
    # Read datasets
    print("Reading datasets...")
    fdi = pd.read_csv(fdi_path, index_col=0)
    crime = pd.read_csv(crime_path)
    
    # Convert FDI to long format
    print("Converting FDI to long format...")
    fdi_long = fdi.reset_index().melt(
        id_vars=['Country Name'],
        var_name='Year',
        value_name='FDI_NetInflows_USD'
    )
    fdi_long['Year'] = pd.to_numeric(fdi_long['Year'])
    
    # Convert Crime Index to long format
    print("Converting Crime Index to long format...")
    crime_long = crime.melt(
        id_vars=['Year'],
        var_name='Country',
        value_name='Crime_Index'
    )
    crime_long['Crime_Index'] = pd.to_numeric(crime_long['Crime_Index'], errors='coerce')
    
    # Create country name mapping
    mapping = create_country_name_mapping()
    
    # Standardize country names in Crime Index using mapping
    print("Standardizing country names...")
    crime_long['Country_StandardFDI'] = crime_long['Country'].map(mapping).fillna(crime_long['Country'])
    
    # Merge on country and year
    print("Merging datasets...")
    merged = fdi_long.merge(
        crime_long[['Year', 'Country_StandardFDI', 'Crime_Index', 'Country']],
        how='outer',
        left_on=['Country Name', 'Year'],
        right_on=['Country_StandardFDI', 'Year']
    )
    
    # Clean up columns
    merged = merged.drop('Country_StandardFDI', axis=1).rename(columns={'Country': 'Crime_Country'})
    merged = merged[['Country Name', 'Crime_Country', 'Year', 'FDI_NetInflows_USD', 'Crime_Index']]
    
    # Sort by country and year
    merged = merged.sort_values(['Country Name', 'Year']).reset_index(drop=True)
    
    # Save merged dataset
    print(f"Saving merged dataset to {output_path}...")
    merged.to_csv(output_path, index=False)
    
    # Print summary statistics
    print("\n" + "="*70)
    print("MERGE SUMMARY")
    print("="*70)
    print(f"Merged dataset shape: {merged.shape}")
    print(f"Year range: {merged['Year'].min()} - {merged['Year'].max()}")
    print(f"Unique countries: {merged['Country Name'].nunique()}")
    print(f"FDI records with data: {merged['FDI_NetInflows_USD'].notna().sum()}")
    print(f"Crime Index records with data: {merged['Crime_Index'].notna().sum()}")
    print(f"Records with both FDI and Crime data: {merged['FDI_NetInflows_USD'].notna().sum() & merged['Crime_Index'].notna().sum()}")
    
    print("\nMissing data by column:")
    print(f"  FDI_NetInflows_USD: {merged['FDI_NetInflows_USD'].isna().sum()} missing")
    print(f"  Crime_Index: {merged['Crime_Index'].isna().sum()} missing")
    
    print("\nFirst few rows of merged data:")
    print(merged.head(10))
    
    print("\nSample of rows with both FDI and Crime data:")
    both_data = merged[merged['FDI_NetInflows_USD'].notna() & merged['Crime_Index'].notna()]
    if len(both_data) > 0:
        print(both_data.head(10))
    else:
        print("No rows with both FDI and Crime data found")
    
    return merged


if __name__ == '__main__':
    # Define paths
    fdi_file = '/workspaces/qm2023-capstone-arjun-daemian-kade-isidro/data/processed/Foreign Direct Investment Spreadsheet 1960-2024.csv'
    crime_file = '/workspaces/qm2023-capstone-arjun-daemian-kade-isidro/data/processed/Crime Index Spreadsheet.csv'
    output_file = '/workspaces/qm2023-capstone-arjun-daemian-kade-isidro/data/final/fdi_crime_merged.csv'
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Merge datasets
    merged_df = merge_fdi_crime_data(fdi_file, crime_file, output_file)
