"""
Script to transpose World Foreign Direct Investment data.
Converts from Country rows x Year columns to Year rows x Country columns.
"""

import pandas as pd
import os

def transpose_fdi_data(input_path, output_path):
    """
    Transpose FDI data so that years are rows and countries are columns.
    
    Args:
        input_path: Path to input CSV file
        output_path: Path to output CSV file
    """
    # Read the raw data with proper encoding
    df = pd.read_csv(input_path, skiprows=4, encoding='utf-8-sig')
    
    # The data has Country Name, Country Code, Indicator Name, Indicator Code
    # followed by year columns (1960-2024)
    
    # Set the index to Country Name for clarity
    df.set_index('Country Name', inplace=True)
    
    # Drop non-numeric metadata columns and unnamed columns
    cols_to_drop = ['Country Code', 'Indicator Name', 'Indicator Code']
    cols_to_drop += [col for col in df.columns if col.startswith('Unnamed')]
    df = df.drop(cols_to_drop, axis=1)
    
    # Convert all columns to numeric (handle empty strings as NaN)
    df = df.apply(pd.to_numeric, errors='coerce')
    
    # Transpose the dataframe
    transposed_df = df.T
    
    # The index is now years, let's rename it for clarity
    transposed_df.index.name = 'Year'
    
    # Convert year index to integer (clean up any whitespace first)
    transposed_df.index = transposed_df.index.str.strip().astype(int)
    
    # Sort by year
    transposed_df = transposed_df.sort_index()
    
    # Save to CSV
    transposed_df.to_csv(output_path)
    
    print(f"Transposed data saved to {output_path}")
    print(f"\nShape: {transposed_df.shape[0]} years x {transposed_df.shape[1]} countries")
    print(f"Years range: {transposed_df.index.min()} to {transposed_df.index.max()}")
    print(f"\nFirst few rows and columns:")
    print(transposed_df.iloc[:5, :5])


if __name__ == '__main__':
    # Define paths
    input_file = '/workspaces/qm2023-capstone-arjun-daemian-kade-isidro/data/raw/WorldForeignDirectInvestmentInflow'
    output_file = '/workspaces/qm2023-capstone-arjun-daemian-kade-isidro/data/processed/fdi_transposed_years_x_countries.csv'
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Transpose and save
    transpose_fdi_data(input_file, output_file)
