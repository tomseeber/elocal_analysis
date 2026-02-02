# Data Cleaning Functions Documentation

## impute_mice
**Description**: 
Applies MICE (Multivariate Imputation by Chained Equations) to fill missing values in specified columns. It uses `sklearn.impute.IterativeImputer`.

**Parameters**:
- `df` (pd.DataFrame): Input dataframe.
- `columns` (list): List of column names to apply imputation on.

**Returns**:
- `pd.DataFrame`: Dataframe with imputed values.

---

## drop_duplicates_data
**Description**: 
Removes duplicate rows from the dataframe.

**Parameters**:
- `df` (pd.DataFrame): Input dataframe.

**Returns**:
- `pd.DataFrame`: Dataframe without duplicates.

---

## drop_na_values
**Description**: 
Drops rows containing missing values (NA). Can be restricted to specific columns.

**Parameters**:
- `df` (pd.DataFrame): Input dataframe.
- `columns` (list, optional): List of columns to check for NA. If None, checks all.

**Returns**:
- `pd.DataFrame`: Dataframe with NAs dropped.

---

## exclude_outliers_iqr
**Description**: 
Excludes outliers from the dataframe based on the Interquartile Range (IQR) method. Rows where the value in `column` is outside `[Q1 - 1.5*IQR, Q3 + 1.5*IQR]` are removed.

**Parameters**:
- `df` (pd.DataFrame): Input dataframe.
- `column` (str): Column name to check for outliers.

**Returns**:
- `pd.DataFrame`: Dataframe with outliers removed.

---

## condense_categories
**Description**: 
Uses fuzzy matching (`thefuzz`) to identify and condense similar categories. If categories are similar above the threshold (default 80%), they are mapped to the first occurring similar value.

**Parameters**:
- `df` (pd.DataFrame): Input dataframe.
- `column` (str): Column with categorical data.
- `threshold` (int): Similarity threshold (0-100). Default is 80.

**Returns**:
- `pd.DataFrame`: Dataframe with condensed categories.
