import pandas as pd
import numpy as np
import os
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from thefuzz import process, fuzz

# --- Function Definitions ---

def impute_mice(df, columns):
    """
    Applies MICE (Multivariate Imputation by Chained Equations) to fill missing values.
    """
    # MICE requires numeric data.
    df_imputed = df.copy()
    if not columns:
        return df_imputed
    
    # Check if columns exist
    missing_cols = [c for c in columns if c not in df.columns]
    if missing_cols:
        print(f"Warning: Columns not found: {missing_cols}")
        return df_imputed

    imputer = IterativeImputer(random_state=0)
    try:
        df_imputed[columns] = imputer.fit_transform(df_imputed[columns])
    except Exception as e:
        print(f"Error during MICE imputation: {e}")
    
    return df_imputed

def drop_duplicates_data(df):
    """
    Drops duplicate rows from the dataframe.
    """
    return df.drop_duplicates()

def drop_na_values(df, columns=None):
    """
    Drops rows with NA values.
    """
    if columns:
        return df.dropna(subset=columns)
    return df.dropna()

def exclude_outliers_iqr(df, column):
    """
    Excludes outliers based on IQR formula.
    """
    if column not in df.columns:
        return df
        
    # Ensure column is numeric
    if not pd.api.types.is_numeric_dtype(df[column]):
        print(f"Column {column} is not numeric. Skipping outlier removal.")
        return df

    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

def condense_categories(df, column, threshold=80):
    """
    Condenses similar categories using fuzzy matching.
    """
    if column not in df.columns:
        return df
        
    df_out = df.copy()
    unique_values = df_out[column].dropna().unique().tolist()
    replacements = {}
    unique_values.sort()
    processed = set()
    
    for val in unique_values:
        if val in processed:
            continue
            
        matches = process.extract(val, unique_values, limit=None, scorer=fuzz.token_sort_ratio)
        similar_values = [match[0] for match in matches if match[1] >= threshold]
        
        for similar in similar_values:
            if similar not in processed:
                replacements[similar] = val
                processed.add(similar)
                
    df_out[column] = df_out[column].replace(replacements)
    return df_out

# --- Main Test Script ---

if __name__ == "__main__":
    # Define data path relative to this script
    # Assuming script is in notebooks/Data Cleaning/
    raw_data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/raw/raw_test_call_data.csv'))
    
    print(f"Loading data from: {raw_data_path}")
    
    if os.path.exists(raw_data_path):
        df = pd.read_csv(raw_data_path)
        print("Original Data Shape:", df.shape)
        
        # 1. Drop Duplicates
        print("\n--- Testing Drop Duplicates ---")
        df = drop_duplicates_data(df)
        print("Shape after dropping duplicates:", df.shape)
        
        # 2. Fuzzy Matching
        print("\n--- Testing Fuzzy Matching on 'disposition' ---")
        # Check unique values before
        print("Unique dispositions before:", df['disposition'].unique())
        df = condense_categories(df, 'disposition', threshold=80)
        print("Unique dispositions after:", df['disposition'].unique())
        
        # 3. MICE Imputation
        # We need to handle non-numeric data before MICE if we were passing the whole DF, 
        # but the function takes specific columns.
        print("\n--- Testing MICE Imputation on 'call_duration' ---")
        # Introduce some NAs for testing if none exist (though file had some issues)
        # raw data had empty call_start_time, call_duration seemed full but let's check.
        print("Missing values in call_duration before:", df['call_duration'].isnull().sum())
        
        # MICE fills missing values. If there are none, it does nothing.
        # Let's ensure there are some NAs or we test on a column that has them.
        # 'billable_status' has a missing value in the file preview line 6 (index 5) but it's boolean/string.
        # 'call_duration' is numeric.
        
        # For demonstration, let's force a nan if needed, or just run it.
        df = impute_mice(df, columns=['call_duration'])
        print("Missing values in call_duration after:", df['call_duration'].isnull().sum())
        
        # 4. Outlier Removal
        print("\n--- Testing IQR Outlier Removal on 'call_duration' ---")
        print("Shape before outlier removal:", df.shape)
        df = exclude_outliers_iqr(df, 'call_duration')
        print("Shape after outlier removal:", df.shape)
        
        # 5. Drop NA
        print("\n--- Testing Drop NA ---")
        print("Shape before drop NA:", df.shape)
        df = drop_na_values(df)
        print("Shape after drop NA:", df.shape)
        
        print("\nData Cleaning Test Complete.")
        
    else:
        print("Error: Data file not found.")
