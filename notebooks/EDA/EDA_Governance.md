# EDA_Governance.ipynb — Function Reference

> **Phase 1: Data Quality Assessment (Governance First)**
> Reusable functions for rapid data quality profiling. All functions accept a pandas `DataFrame` as their first argument and can be run column-by-column or across the entire dataset.

---

## Completeness

### `completeness_summary(df)`

```python
def completeness_summary(df: pd.DataFrame) -> pd.DataFrame
```

**Description**
Returns a summary DataFrame with the missing count, missing percentage, present percentage, and dtype for every column. Results are sorted by missing percentage descending.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| `df` | `pd.DataFrame` | The dataset to assess. |

**Returns**
`pd.DataFrame` with columns: `dtype`, `missing_count`, `missing_pct`, `present_pct`.

---

### `plot_missing(df, threshold)`

```python
def plot_missing(df: pd.DataFrame, threshold: float = 0.0) -> None
```

**Description**
Renders a horizontal Seaborn bar chart of missing-value percentages. Only columns exceeding the given threshold are shown. Each bar is annotated with its percentage.

**Parameters**

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `df` | `pd.DataFrame` | — | The dataset to assess. |
| `threshold` | `float` | `0.0` | Minimum missing percentage to include a column in the chart. |

**Returns**
`None` (displays a matplotlib figure).

---

### `plot_missingness_heatmap(df)`

```python
def plot_missingness_heatmap(df: pd.DataFrame) -> None
```

**Description**
Displays a binary heatmap of nullity across rows and columns. Green cells indicate present values; orange cells indicate missing values. If the dataset exceeds 500 rows, a random sample is used.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| `df` | `pd.DataFrame` | The dataset to assess. |

**Returns**
`None` (displays a matplotlib figure).

---

### `missingness_diagnostic(df)`

```python
def missingness_diagnostic(df: pd.DataFrame) -> pd.DataFrame
```

**Description**
Runs a simplified MCAR / MAR / MNAR diagnostic for every column with missing values. For each such column, it performs Welch's t-test comparing means of all other numeric columns when the column IS vs IS NOT missing. If any tests are significant at p < 0.05, the column is classified as "Likely MAR"; otherwise "Likely MCAR".

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| `df` | `pd.DataFrame` | The dataset to assess. |

**Returns**
`pd.DataFrame` with columns: `column`, `missing_n`, `missing_pct`, `pattern`.

---

## Accuracy

### `iqr_outliers(df, col, factor)`

```python
def iqr_outliers(df: pd.DataFrame, col: str, factor: float = 1.5) -> pd.DataFrame
```

**Description**
Detects outliers in a single numeric column using the IQR method. Prints the quartile bounds, IQR value, fence boundaries, and outlier count. Returns the subset of rows flagged as outliers.

**Parameters**

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `df` | `pd.DataFrame` | — | The dataset. |
| `col` | `str` | — | Name of the numeric column to check. |
| `factor` | `float` | `1.5` | IQR multiplier for the fence (1.5 = standard, 3.0 = extreme). |

**Returns**
`pd.DataFrame` — rows where `col` falls outside [Q1 - factor*IQR, Q3 + factor*IQR].

---

### `iqr_outlier_summary(df, factor)`

```python
def iqr_outlier_summary(df: pd.DataFrame, factor: float = 1.5) -> pd.DataFrame
```

**Description**
Runs IQR outlier detection across all numeric columns and returns a summary table sorted by outlier percentage descending. Includes Q1, Q3, IQR, lower/upper bounds, outlier count, and outlier percentage.

**Parameters**

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `df` | `pd.DataFrame` | — | The dataset. |
| `factor` | `float` | `1.5` | IQR multiplier for the fence. |

**Returns**
`pd.DataFrame` with columns: `column`, `Q1`, `Q3`, `IQR`, `lower_bound`, `upper_bound`, `outlier_count`, `outlier_pct`.

---

### `plot_outlier_boxplots(df)`

```python
def plot_outlier_boxplots(df: pd.DataFrame) -> None
```

**Description**
Creates a grid of Seaborn box plots — one per numeric column — to visually identify outliers. Uses eLocal brand blue for the box color.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| `df` | `pd.DataFrame` | The dataset. |

**Returns**
`None` (displays a matplotlib figure).

---

### `impossible_value_check(df)`

```python
def impossible_value_check(df: pd.DataFrame) -> pd.DataFrame
```

**Description**
Scans every column for potential data quality issues:
- **Numeric columns**: flags negative values and zeros.
- **Object columns**: samples up to 1,000 non-null values and flags mixed-type columns where some entries look numeric and others do not.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| `df` | `pd.DataFrame` | The dataset. |

**Returns**
`pd.DataFrame` with columns: `column`, `dtype`, `issues`.

---

## Consistency

### `duplicate_summary(df)`

```python
def duplicate_summary(df: pd.DataFrame) -> dict
```

**Description**
Counts exact duplicate rows and prints a one-line summary. Returns a dict with total rows, duplicate count, duplicate percentage, and unique row count.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| `df` | `pd.DataFrame` | The dataset. |

**Returns**
`dict` with keys: `total_rows`, `duplicate_rows`, `duplicate_pct`, `unique_rows`.

---

### `duplicate_on_keys(df, key_cols)`

```python
def duplicate_on_keys(df: pd.DataFrame, key_cols: list) -> pd.DataFrame
```

**Description**
Finds rows that are duplicated on a specified subset of key columns (keeps all copies). Returns the duplicated rows sorted by the key columns.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| `df` | `pd.DataFrame` | The dataset. |
| `key_cols` | `list` | Column names to use as the composite key. |

**Returns**
`pd.DataFrame` — all rows where the key combination appears more than once.

---

### `conflicting_entries(df, key_cols, value_col)`

```python
def conflicting_entries(df: pd.DataFrame, key_cols: list, value_col: str) -> pd.DataFrame
```

**Description**
Identifies groups that share identical key columns but have multiple distinct values in `value_col`. This flags data conflicts where the same entity has inconsistent records.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| `df` | `pd.DataFrame` | The dataset. |
| `key_cols` | `list` | Column names forming the group key. |
| `value_col` | `str` | Column to check for conflicting values within each group. |

**Returns**
`pd.DataFrame` with the key columns plus `n_unique` (count of distinct values per group), filtered to groups with `n_unique > 1`.

---

### `referential_integrity(df, fk_col, ref_df, ref_col)`

```python
def referential_integrity(df: pd.DataFrame, fk_col: str,
                          ref_df: pd.DataFrame, ref_col: str) -> pd.DataFrame
```

**Description**
Checks that every non-null value in `fk_col` of the primary DataFrame exists in `ref_col` of a reference DataFrame. Returns "orphan" rows — foreign key violations.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| `df` | `pd.DataFrame` | The primary dataset containing the foreign key. |
| `fk_col` | `str` | Foreign key column name in `df`. |
| `ref_df` | `pd.DataFrame` | Reference dataset. |
| `ref_col` | `str` | Primary key column name in `ref_df`. |

**Returns**
`pd.DataFrame` — rows from `df` where `fk_col` value is not found in `ref_df[ref_col]`.

---

## Cardinality

### `cardinality_summary(df)`

```python
def cardinality_summary(df: pd.DataFrame) -> pd.DataFrame
```

**Description**
Returns the number of unique values and cardinality ratio (unique/total as %) for every column. Sorted by unique count descending. Useful for identifying high-cardinality columns that may need binning or encoding.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| `df` | `pd.DataFrame` | The dataset. |

**Returns**
`pd.DataFrame` with columns: `column`, `dtype`, `n_unique`, `cardinality_ratio`.

---

### `value_counts_pct(df, col, top_n)`

```python
def value_counts_pct(df: pd.DataFrame, col: str, top_n: int = 20) -> pd.DataFrame
```

**Description**
Returns the top-N value counts for a single column including both raw count and percentage of total. `NaN` values are included in the count.

**Parameters**

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `df` | `pd.DataFrame` | — | The dataset. |
| `col` | `str` | — | Column name. |
| `top_n` | `int` | `20` | Number of top values to return. |

**Returns**
`pd.DataFrame` with columns: `value`, `count`, `pct`.

---

### `plot_value_counts(df, col, top_n)`

```python
def plot_value_counts(df: pd.DataFrame, col: str, top_n: int = 20) -> None
```

**Description**
Renders a horizontal bar chart of the top-N most frequent values in a column. Uses eLocal brand orange. Each bar is annotated with its count.

**Parameters**

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `df` | `pd.DataFrame` | — | The dataset. |
| `col` | `str` | — | Column name. |
| `top_n` | `int` | `20` | Number of top values to display. |

**Returns**
`None` (displays a matplotlib figure).

---

## Univariate Analysis

### `univariate_stats(df)`

```python
def univariate_stats(df: pd.DataFrame) -> pd.DataFrame
```

**Description**
Extends `DataFrame.describe()` with additional statistical measures for all numeric columns: skewness, kurtosis, IQR, and coefficient of variation (CV = std/mean).

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| `df` | `pd.DataFrame` | The dataset. |

**Returns**
`pd.DataFrame` — transposed describe output with extra columns: `skew`, `kurtosis`, `iqr`, `cv`.

---

### `plot_distributions(df)`

```python
def plot_distributions(df: pd.DataFrame) -> None
```

**Description**
Generates a grid of histograms with KDE overlays for every numeric column. Each subplot title includes the skewness value. Uses eLocal brand blue.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| `df` | `pd.DataFrame` | The dataset. |

**Returns**
`None` (displays a matplotlib figure).

---

### `plot_single_distribution(df, col)`

```python
def plot_single_distribution(df: pd.DataFrame, col: str) -> None
```

**Description**
Detailed distribution plot for a single column. Overlays a KDE curve plus vertical lines for mean (orange dashed) and median (green solid). Title includes skewness and kurtosis.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| `df` | `pd.DataFrame` | The dataset. |
| `col` | `str` | Numeric column name. |

**Returns**
`None` (displays a matplotlib figure).

---

## Bivariate Analysis

### `top_correlations(df, n)`

```python
def top_correlations(df: pd.DataFrame, n: int = 15) -> pd.DataFrame
```

**Description**
Computes Pearson correlations for all numeric column pairs and returns the top-N by absolute value. Self-pairs and duplicate pairs are excluded.

**Parameters**

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `df` | `pd.DataFrame` | — | The dataset. |
| `n` | `int` | `15` | Number of top pairs to return. |

**Returns**
`pd.DataFrame` with columns: `feature_1`, `feature_2`, `correlation`.

---

### `plot_correlation_heatmap(df)`

```python
def plot_correlation_heatmap(df: pd.DataFrame) -> None
```

**Description**
Renders a lower-triangle Pearson correlation heatmap with annotated coefficients. Uses a coolwarm diverging colormap centered at zero.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| `df` | `pd.DataFrame` | The dataset. |

**Returns**
`None` (displays a matplotlib figure).

---

### `target_leakage_check(df, target_col, threshold)`

```python
def target_leakage_check(df: pd.DataFrame, target_col: str,
                          threshold: float = 0.95) -> pd.DataFrame
```

**Description**
Flags numeric features whose absolute Pearson correlation with the target column meets or exceeds the threshold. High correlation may indicate data leakage — a feature that would not be available at prediction time.

**Parameters**

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `df` | `pd.DataFrame` | — | The dataset. |
| `target_col` | `str` | — | Name of the target / label column. |
| `threshold` | `float` | `0.95` | Absolute correlation cutoff. |

**Returns**
`pd.DataFrame` with columns: `feature`, `abs_corr`.
