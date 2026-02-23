"""
Fetch Corruption Perceptions Index (CPI) data from World Bank or Transparency International.

The CPI is an annual index published by Transparency International that ranks countries
by their perceived level of public sector corruption.
"""

import pandas as pd
import requests
from io import StringIO
import os


def fetch_corruption_perceptions_index(output_path):
    """
    Fetch Corruption Perceptions Index data from World Development Indicators API.
    
    The indicator code for CPI in World Bank data is: IQ.CPI.TRAN.XQ
    This covers years 2012-present with global coverage.
    
    Args:
        output_path: Path to save the CSV file
    """
    print("Fetching Corruption Perceptions Index data...")
    print("Note: Using World Development Indicators source (similar to FDI data)")
    
    # World Bank API endpoint for CPI data
    # Indicator: IQ.CPI.TRAN.XQ (Internationally comparable CPI from Transparency International)
    indicator = 'IQ.CPI.TRAN.XQ'
    base_url = 'https://api.worldbank.org/v2/country/all/indicator/'
    url = f'{base_url}{indicator}'
    
    params = {
        'format': 'json',
        'per_page': 500,
        'date': '2012:2024'
    }
    
    try:
        print(f"Requesting data from World Bank API...")
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        if len(data) < 2 or data[1] is None:
            print("Warning: No data returned from API. The indicator may not be available.")
            print("Please download CPI data manually from:")
            print("  - World Bank: https://data.worldbank.org/indicator/")
            print("  - Transparency International: https://www.transparency.org/en/cpi/")
            return None
        
        # Parse the JSON response
        records = []
        for record in data[1]:
            records.append({
                'Country': record['countryId'],
                'Country_Name': record.get('country', {}).get('value', ''),
                'Year': record['date'],
                'CPI_Score': record['value']
            })
        
        df = pd.DataFrame(records)
        
        # Filter to 2012-present
        df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
        df = df[df['Year'] >= 2012].dropna(subset=['Year'])
        df = df.sort_values(['Country_Name', 'Year'])
        
        print(f"Retrieved {len(df)} CPI records")
        print(f"Countries: {df['Country_Name'].nunique()}")
        print(f"Year range: {df['Year'].min():.0f}-{df['Year'].max():.0f}")
        
        # Save to CSV
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"Saved to {output_path}")
        
        return df
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching from World Bank API: {e}")
        print("\nAlternative: Manual download instructions")
        print("-" * 70)
        print("CPI data can be downloaded from:")
        print("\n1. Transparency International Official Website:")
        print("   https://www.transparency.org/en/cpi/")
        print("   - Download yearly rankings by country (2012-present)")
        print("   - Usually available as Excel or CSV")
        print("\n2. World Bank Data Portal:")
        print("   https://data.worldbank.org/indicator/")
        print("   - Search for 'Corruption' or use indicator: IQ.CPI.TRAN.XQ")
        print("\n3. Kaggle Datasets:")
        print("   https://www.kaggle.com/datasets/search?q=corruption+perceptions+index")
        print("-" * 70)
        return None


def create_manual_download_template():
    """
    Create a template CSV file for manual CPI data entry.
    This helps if automated download isn't possible.
    """
    template_data = {
        'Country': ['Example', 'Afghanistan', 'Albania', 'Algeria'],
        'Year': [2024, 2012, 2012, 2012],
        'CPI_Score': [50.0, 25.0, 36.0, 34.0],
        'Notes': ['Template example', 'Insert CPI scores', 'Insert CPI scores', 'Insert CPI scores']
    }
    
    df = pd.DataFrame(template_data)
    return df


if __name__ == '__main__':
    # Define output paths
    output_dir = '/workspaces/qm2023-capstone-arjun-daemian-kade-isidro/data/raw'
    output_file = f'{output_dir}/corruption_perceptions_index_2012_present.csv'
    
    # Create directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Try to fetch CPI data
    print("\n" + "=" * 70)
    print("CORRUPTION PERCEPTIONS INDEX (CPI) DATA FETCHER")
    print("=" * 70 + "\n")
    
    result = fetch_corruption_perceptions_index(output_file)
    
    if result is None:
        print("\nCreating template for manual data entry...")
        template = create_manual_download_template()
        template_file = f'{output_dir}/CPI_template.csv'
        template.to_csv(template_file, index=False)
        print(f"Template saved to: {template_file}")
        print("\nNext steps:")
        print("1. Download CPI data from Transparency International or World Bank")
        print("2. Save it to:", output_file)
        print("3. Ensure columns: Country, Year, CPI_Score, (optional: Region, Rank)")
