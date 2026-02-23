"""
Script to reverse transpose FDI data.
Converts from Year rows x Country columns to Country rows x Year columns.
"""

import pandas as pd
import os

def reverse_transpose_fdi_data(input_path, output_path):
    """
    Reverse transpose FDI data so that countries are rows and years are columns.
    
    Args:
        input_path: Path to input CSV file (years as rows)
        output_path: Path to output CSV file (countries as rows)
    """
    # Read the transposed data
    df = pd.read_csv(input_path, index_col=0)
    
    # Transpose back to original format (countries as rows, years as columns)
    reversed_df = df.T
    
    # Set the index name
    reversed_df.index.name = 'Country Name'
    
    # Save to CSV
    reversed_df.to_csv(output_path)
    
    print(f"Reverse transposed data saved to {output_path}")
    print(f"\nShape: {reversed_df.shape[0]} countries x {reversed_df.shape[1]} years")
    print(f"First few rows and columns:")
    print(reversed_df.iloc[:5, :5])


if __name__ == '__main__':
    # Define paths
    input_file = '/workspaces/qm2023-capstone-arjun-daemian-kade-isidro/data/processed/fdi_transposed_years_x_countries.csv'
    output_file = '/workspaces/qm2023-capstone-arjun-daemian-kade-isidro/data/processed/fdi_countries_x_years.csv'
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Reverse transpose and save
    reverse_transpose_fdi_data(input_file, output_file)
