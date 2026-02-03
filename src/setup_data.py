import pandas as pd
import numpy as np
import os
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from thefuzz import process, fuzz

# --- Reuse Function Definitions ---
# Ideally these should be in a src module, but for now copying as per previous context

def impute_mice(df, columns):
    df_imputed = df.copy()
    if not columns:
        return df_imputed
    
    missing_cols = [c for c in columns if c not in df.columns]
    if missing_cols:
        return df_imputed

    imputer = IterativeImputer(random_state=0)
    try:
        df_imputed[columns] = imputer.fit_transform(df_imputed[columns])
    except Exception as e:
        print(f"Error during MICE imputation: {e}")
    
    return df_imputed

def drop_duplicates_data(df):
    return df.drop_duplicates()

def drop_na_values(df, columns=None):
    if columns:
        return df.dropna(subset=columns)
    return df.dropna()

def exclude_outliers_iqr(df, column):
    if column not in df.columns:
        return df
    if not pd.api.types.is_numeric_dtype(df[column]):
        return df

    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

def condense_categories(df, column, threshold=80):
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

if __name__ == "__main__":
    raw_path = 'data/raw/raw_test_call_data.csv'
    cleaned_path = 'data/cleaned/cleaned_call_data.csv'
    
    if os.path.exists(raw_path):
        print(f"Reading from {raw_path}")
        df = pd.read_csv(raw_path)
        
        # Apply cleaning steps
        df = drop_duplicates_data(df)
        df = condense_categories(df, 'disposition', threshold=80)
        # Assuming call_duration is the main numeric field for MICE and IQR
        df = impute_mice(df, columns=['call_duration'])
        df = exclude_outliers_iqr(df, 'call_duration')
        df = drop_na_values(df)
        
        os.makedirs(os.path.dirname(cleaned_path), exist_ok=True)
        df.to_csv(cleaned_path, index=False)
        print(f"Cleaned data saved to {cleaned_path}")
    else:
        print(f"Raw data not found at {raw_path}")
