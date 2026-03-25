"""
Script to create derived variables for enhanced panel analysis.
Adds log transformations, lagged variables, standardized scores, and regional classifications.
Output: data/final/analysis_panel_enhanced.csv
"""

import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
FINAL_DIR = DATA_DIR / "final"

# Regional classifications
OECD_COUNTRIES = {
    "Australia", "Canada", "Chile", "France", "Germany", "Greece", 
    "Ireland", "Italy", "Japan", "Mexico", "Spain", "Sweden", 
    "United Kingdom", "United States"
}

BRICS_COUNTRIES = {"Brazil", "Russia", "India", "China"}

DEVELOPED = {
    "Australia", "Canada", "France", "Germany", "Greece", "Ireland", 
    "Italy", "Japan", "Spain", "Sweden", "United Kingdom", "United States"
}

EMERGING = {
    "Brazil", "Chile", "China", "India", "Mexico", "Russia", "Pakistan"
}

ADVANCED = {
    "Australia", "Canada", "France", "Germany", "Ireland", "Italy", 
    "Japan", "Spain", "Sweden", "United Kingdom", "United States"
}

def load_data(filepath: Path) -> pd.DataFrame:
    """Load analysis panel data."""
    if not filepath.exists():
        raise FileNotFoundError(f"Data file not found: {filepath}")
    return pd.read_csv(filepath)

def add_log_fdi(df: pd.DataFrame) -> pd.DataFrame:
    """Add log-transformed FDI (useful for skewed economic variables)."""
    # For negative values, use log(abs(x)) * sign(x) to preserve sign
    df['log_fdi'] = np.where(
        df['foreign_investment'] > 0,
        np.log(df['foreign_investment']),
        np.where(
            df['foreign_investment'] < 0,
            -np.log(np.abs(df['foreign_investment'])),
            np.nan
        )
    )
    # Mark observations with NaN (non-positive FDI values)
    print(f"  Created log_fdi: {df['log_fdi'].notna().sum()} non-missing values")
    return df

def add_standardized_variables(df: pd.DataFrame) -> pd.DataFrame:
    """Add z-score standardized versions of key variables."""
    for col in ['crime_index', 'cpi_score', 'gepu', 'foreign_investment']:
        if col in df.columns:
            mean = df[col].mean()
            std = df[col].std()
            df[f'{col}_std'] = (df[col] - mean) / std if std > 0 else np.nan
    
    print(f"  Created standardized variables: crime_index_std, cpi_score_std, gepu_std, foreign_investment_std")
    return df

def add_lagged_variables(df: pd.DataFrame) -> pd.DataFrame:
    """Add lagged FDI and crime for panel dynamics."""
    df_sorted = df.sort_values(['Country', 'Year']).reset_index(drop=True)
    
    # Lagged FDI (one year back)
    df_sorted['fdi_lag1'] = df_sorted.groupby('Country')['foreign_investment'].shift(1)
    
    # Lagged crime index
    df_sorted['crime_lag1'] = df_sorted.groupby('Country')['crime_index'].shift(1)
    
    # Lagged CPI (corruption perception)
    df_sorted['cpi_lag1'] = df_sorted.groupby('Country')['cpi_score'].shift(1)
    
    print(f"  Created lagged variables: fdi_lag1, crime_lag1, cpi_lag1")
    return df_sorted

def add_change_variables(df: pd.DataFrame) -> pd.DataFrame:
    """Add year-over-year change variables."""
    df_sorted = df.sort_values(['Country', 'Year']).reset_index(drop=True)
    
    # FDI change (year-over-year percentage change where possible)
    df_sorted['fdi_change'] = df_sorted.groupby('Country')['foreign_investment'].pct_change() * 100
    
    # Crime change
    df_sorted['crime_change'] = df_sorted.groupby('Country')['crime_index'].diff()
    
    # CPI change
    df_sorted['cpi_change'] = df_sorted.groupby('Country')['cpi_score'].diff()
    
    print(f"  Created change variables: fdi_change, crime_change, cpi_change")
    return df_sorted

def add_regional_dummies(df: pd.DataFrame) -> pd.DataFrame:
    """Add categorical variables for regional analysis."""
    df['is_oecd'] = df['Country'].isin(OECD_COUNTRIES).astype(int)
    df['is_brics'] = df['Country'].isin(BRICS_COUNTRIES).astype(int)
    df['development_level'] = df['Country'].apply(lambda x: 
        'Advanced' if x in ADVANCED else 
        'Emerging' if x in EMERGING else 
        'Other'
    )
    
    print(f"  Created regional dummies: is_oecd, is_brics, development_level")
    return df

def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add time-based features."""
    df['time_trend'] = df.groupby('Country').cumcount() + 1  # 1, 2, 3, ... per country
    df['years_since_2012'] = df['Year'] - 2012
    df['is_crisis_year'] = df['Year'].isin([2008, 2009, 2020]).astype(int)  # 2008-09 financial crisis, 2020 COVID
    
    print(f"  Created time features: time_trend, years_since_2012, is_crisis_year")
    return df

def add_interaction_terms(df: pd.DataFrame) -> pd.DataFrame:
    """Add interaction terms for hypothesis testing."""
    # Crime × Corruption interaction
    df['crime_corruption_interaction'] = df['crime_index'] * df['cpi_score']
    
    # GEPU × Corruption interaction
    df['gepu_corruption_interaction'] = df['gepu'] * df['cpi_score']
    
    # Crime × GEPU interaction
    df['crime_gepu_interaction'] = df['crime_index'] * df['gepu']
    
    print(f"  Created interaction terms: crime_corruption_interaction, gepu_corruption_interaction, crime_gepu_interaction")
    return df

def add_ratio_variables(df: pd.DataFrame) -> pd.DataFrame:
    """Add ratio variables for relative measures."""
    # Crime-to-corruption ratio: higher when crime high relative to corruption perception
    df['crime_to_corruption'] = np.where(
        df['cpi_score'] > 0,
        df['crime_index'] / (100 - df['cpi_score']),  # Invert CPI so higher = more corruption
        np.nan
    )
    
    # GEPU-to-corruption ratio
    df['gepu_to_corruption'] = np.where(
        (100 - df['cpi_score']) > 0,
        df['gepu'] / (100 - df['cpi_score']),
        np.nan
    )
    
    print(f"  Created ratio variables: crime_to_corruption, gepu_to_corruption")
    return df

def main():
    """Generate enhanced dataset with derived variables."""
    input_file = FINAL_DIR / "analysis_panel.csv"
    output_file = FINAL_DIR / "analysis_panel_enhanced.csv"
    
    print("=" * 80)
    print("Creating Derived Variables for Panel Analysis")
    print("=" * 80)
    print(f"\nLoading data from: {input_file}")
    
    df = load_data(input_file)
    print(f"Original dataset: {df.shape[0]} rows × {df.shape[1]} columns")
    
    print("\nAdding derived variables...")
    print("-" * 80)
    
    # Apply transformations
    df = add_log_fdi(df)
    df = add_standardized_variables(df)
    df = add_lagged_variables(df)
    df = add_change_variables(df)
    df = add_regional_dummies(df)
    df = add_time_features(df)
    df = add_interaction_terms(df)
    df = add_ratio_variables(df)
    
    print("-" * 80)
    print(f"\nEnhanced dataset: {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"\nNew variables added: {df.shape[1] - 6}")
    print("\nVariable summary:")
    for col in df.columns:
        missing_pct = (df[col].isna().sum() / len(df)) * 100
        print(f"  {col:35} - {df[col].dtype:10} ({missing_pct:5.1f}% missing)")
    
    # Save enhanced dataset
    df.to_csv(output_file, index=False)
    print(f"\n✓ Enhanced dataset saved to: {output_file}")
    
    # Summary statistics
    print("\n" + "=" * 80)
    print("Sample Statistics (Numeric Variables)")
    print("=" * 80)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    print(df[numeric_cols].describe().round(3))

if __name__ == "__main__":
    main()
