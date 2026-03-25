"""
Fetch World Bank Development Indicators (WDI) for Panel Analysis
================================================================

Downloads key indicators from World Bank for 2012-2025:
1. GDP (constant 2015 US$) - NY.GDP.MKTP.KD
2. GDP per capita (current US$) - NY.GDP.PCAP.CD
3. Population - SP.POP.TOTL

These enable:
- FDI normalization (FDI per GDP, FDI per capita)
- Cross-country comparison on development level
- Better controls for economic size effects

Install dependency:
  pip install wbgapi pandas

Usage:
  python code/fetch_world_bank_data.py
  
Output:
  data/raw/world_bank_indicators.csv
"""

import pandas as pd
from pathlib import Path
import sys

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Ensure directories exist
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

def fetch_world_bank_data():
    """
    Fetch World Bank indicators using wbgapi.
    
    Indicators:
    - NY.GDP.MKTP.KD: GDP (constant 2015 US$)
    - NY.GDP.PCAP.CD: GDP per capita (current US$)
    - SP.POP.TOTL: Population
    """
    try:
        import wbgapi as wb
    except ImportError:
        print("ERROR: wbgapi not installed. Install with: pip install wbgapi")
        sys.exit(1)
    
    print("=" * 80)
    print("Fetching World Bank Development Indicators (2012-2025)")
    print("=" * 80)
    
    # Indicators to fetch
    indicators = {
        'NY.GDP.MKTP.KD': 'gdp_constant_2015_usd',
        'NY.GDP.PCAP.CD': 'gdp_per_capita_current_usd',
        'SP.POP.TOTL': 'population'
    }
    
    data_frames = []
    
    for indicator_code, indicator_name in indicators.items():
        print(f"\nFetching {indicator_name} ({indicator_code})...")
        try:
            df = wb.data.get(
                indicator_code,
                time=range(2012, 2026),  # 2012-2025
                numericTimeKeys=True
            )
            df = df.reset_index()
            df = df.rename(columns={'index': 'Country'})
            
            # Reshape from wide to long
            df_long = df.melt(
                id_vars=['Country'],
                var_name='Year',
                value_name=indicator_name
            )
            df_long['Year'] = df_long['Year'].astype(int)
            
            # Remove rows with missing values
            df_long = df_long.dropna(subset=[indicator_name])
            
            print(f"  ✓ Downloaded {len(df_long)} observations")
            data_frames.append(df_long)
            
        except Exception as e:
            print(f"  ✗ Error fetching {indicator_code}: {e}")
    
    if not data_frames:
        print("\nERROR: No data fetched. Check internet connection and wbgapi installation.")
        sys.exit(1)
    
    # Merge all indicators on Country and Year
    print("\nMerging indicators...")
    merged_df = data_frames[0]
    for df in data_frames[1:]:
        merged_df = merged_df.merge(df, on=['Country', 'Year'], how='outer')
    
    # Sort by country and year
    merged_df = merged_df.sort_values(['Country', 'Year']).reset_index(drop=True)
    
    print(f"  ✓ Merged dataset: {merged_df.shape[0]} rows × {merged_df.shape[1]} columns")
    
    # Save raw data
    output_file = RAW_DATA_DIR / "world_bank_indicators.csv"
    merged_df.to_csv(output_file, index=False)
    print(f"\n✓ Saved to: {output_file}")
    
    return merged_df

def clean_and_process(df):
    """
    Clean and create normalized variables.
    
    Creates:
    - fdi_as_pct_gdp: Foreign investment as % of GDP
    - fdi_per_capita: FDI per capita
    """
    print("\n" + "=" * 80)
    print("Processing World Bank Data")
    print("=" * 80)
    
    # Convert numeric columns
    for col in ['gdp_constant_2015_usd', 'gdp_per_capita_current_usd', 'population']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Remove rows with missing gdp or population
    df = df.dropna(subset=['gdp_constant_2015_usd', 'population'])
    
    print(f"\n✓ Cleaned dataset: {df.shape[0]} rows × {len(df.columns)} columns")
    print(f"  Countries: {df['Country'].nunique()}")
    print(f"  Years: {df['Year'].min()}-{df['Year'].max()}")
    
    # Save processed data
    output_file = PROCESSED_DATA_DIR / "world_bank_indicators_clean.csv"
    df.to_csv(output_file, index=False)
    print(f"\n✓ Cleaned data saved to: {output_file}")
    
    return df

def main():
    """Main workflow."""
    print("\n")
    
    # Fetch World Bank data
    df = fetch_world_bank_data()
    
    # Clean and process
    df_clean = clean_and_process(df)
    
    print("\n" + "=" * 80)
    print("Sample of Downloaded Data")
    print("=" * 80)
    print(df_clean.head(10).to_string())
    
    print("\n" + "=" * 80)
    print("Summary Statistics")
    print("=" * 80)
    print(df_clean.describe().round(2))
    
    print("\n✓ World Bank data integration complete!")
    print("\nNext steps:")
    print("  1. Merge this data into analysis_panel.csv using merge_final_panel.py")
    print("  2. Create derived variables: fdi_as_pct_gdp, fdi_per_capita")
    print("  3. Use for M2 robustness checks and subsample analysis")

if __name__ == "__main__":
    main()
