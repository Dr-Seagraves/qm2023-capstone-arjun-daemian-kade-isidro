"""
Fetch World Governance Indicators (WGI) - World Bank
====================================================

Downloads WGI measures from World Bank for validation and robustness:
1. Control of Corruption (-2.5 to 2.5 scale)
2. Rule of Law (-2.5 to 2.5 scale)  
3. Political Stability & Absence of Violence (-2.5 to 2.5 scale)

These enable:
- Cross-validate CPI findings against alternative corruption measure
- Control for institutional quality (rule of law affects FDI)
- Test if political stability confounds crime-FDI relationship

Install dependency:
  pip install wbgapi pandas

Usage:
  python code/fetch_world_governance_indicators.py
  
Output:
  data/raw/world_governance_indicators.csv
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

def fetch_world_governance_indicators():
    """
    Fetch World Governance Indicators using wbgapi.
    
    Indicators:
    - CC.EST: Control of Corruption (estimate)
    - RL.EST: Rule of Law (estimate)
    - PV.EST: Political Stability & Absence of Violence (estimate)
    
    Scale: -2.5 (weak) to +2.5 (strong)
    """
    try:
        import wbgapi as wb
    except ImportError:
        print("ERROR: wbgapi not installed. Install with: pip install wbgapi")
        sys.exit(1)
    
    print("=" * 80)
    print("Fetching World Governance Indicators (WGI) - 2012-2025")
    print("=" * 80)
    
    # WGI indicators
    indicators = {
        'CC.EST': 'control_of_corruption',
        'RL.EST': 'rule_of_law',
        'PV.EST': 'political_stability'
    }
    
    data_frames = []
    
    for indicator_code, indicator_name in indicators.items():
        print(f"\nFetching {indicator_name} ({indicator_code})...")
        try:
            df = wb.data.get(
                indicator_code,
                time=range(2012, 2026),
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
            print(f"    Range: {df_long[indicator_name].min():.2f} to {df_long[indicator_name].max():.2f}")
            data_frames.append(df_long)
            
        except Exception as e:
            print(f"  ✗ Error fetching {indicator_code}: {e}")
    
    if not data_frames:
        print("\nERROR: No data fetched. Check internet connection and wbgapi installation.")
        sys.exit(1)
    
    # Merge all indicators
    print("\nMerging indicators...")
    merged_df = data_frames[0]
    for df in data_frames[1:]:
        merged_df = merged_df.merge(df, on=['Country', 'Year'], how='outer')
    
    merged_df = merged_df.sort_values(['Country', 'Year']).reset_index(drop=True)
    
    print(f"  ✓ Merged dataset: {merged_df.shape[0]} rows × {merged_df.shape[1]} columns")
    
    # Save raw data
    output_file = RAW_DATA_DIR / "world_governance_indicators.csv"
    merged_df.to_csv(output_file, index=False)
    print(f"\n✓ Saved to: {output_file}")
    
    return merged_df

def clean_and_process(df):
    """Clean governance indicators data."""
    print("\n" + "=" * 80)
    print("Processing World Governance Indicators")
    print("=" * 80)
    
    # Convert to numeric
    for col in ['control_of_corruption', 'rule_of_law', 'political_stability']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    print(f"\n✓ Cleaned dataset: {df.shape[0]} rows × {len(df.columns)} columns")
    print(f"  Countries: {df['Country'].nunique()}")
    print(f"  Years: {df['Year'].min()}-{df['Year'].max()}")
    
    # Save processed data
    output_file = PROCESSED_DATA_DIR / "world_governance_indicators_clean.csv"
    df.to_csv(output_file, index=False)
    print(f"\n✓ Cleaned data saved to: {output_file}")
    
    return df

def main():
    """Main workflow."""
    print("\n")
    
    # Fetch WGI data
    df = fetch_world_governance_indicators()
    
    # Clean and process
    df_clean = clean_and_process(df)
    
    print("\n" + "=" * 80)
    print("Sample of Downloaded Data")
    print("=" * 80)
    print(df_clean.head(10).to_string())
    
    print("\n" + "=" * 80)
    print("Summary Statistics (Scale: -2.5 weak to +2.5 strong)")
    print("=" * 80)
    print(df_clean.describe().round(3))
    
    print("\n✓ World Governance Indicators integration complete!")
    print("\nUsage in M2/M3:")
    print("  - Validate CPI findings: correlate control_of_corruption with cpi_score")
    print("  - Control variable: rule_of_law in regression models")
    print("  - Confounding test: political_stability may explain FDI relationship")

if __name__ == "__main__":
    main()
