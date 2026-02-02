# EDA_Correlation.ipynb — Function Reference

> **Bivariate & Correlation Analysis**
> Deep-dive correlation notebook for pairwise correlations, heatmaps, scatter matrices, categorical cross-tabs, and target leakage detection. All functions accept a pandas `DataFrame` as their first argument.

---

## Correlation Matrix

### `correlation_matrix(df, method)`

```python
def correlation_matrix(df: pd.DataFrame, method: str = 'pearson') -> pd.DataFrame
```

**Description**
Computes and returns the full pairwise correlation matrix for all numeric columns. Supports Pearson, Spearman, and Kendall methods.

**Parameters**

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `df` | `pd.DataFrame` | — | The dataset. |
| `method` | `str` | `'pearson'` | Correlation method: `'pearson'`, `'spearman'`, or `'kendall'`. |

**Returns**
`pd.DataFrame` — square correlation matrix indexed by column names.

---

### `top_correlations(df, n, method)`

```python
def top_correlations(df: pd.DataFrame, n: int = 20,
                     method: str = 'pearson') -> pd.DataFrame
```

**Description**
Extracts the top-N strongest pairwise correlations by absolute value. Excludes self-pairs and duplicate pairs (upper triangle only).

**Parameters**

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `df` | `pd.DataFrame` | — | The dataset. |
| `n` | `int` | `20` | Number of top pairs to return. |
| `method` | `str` | `'pearson'` | Correlation method. |

**Returns**
`pd.DataFrame` with columns: `feature_1`, `feature_2`, `correlation`.

---

## Correlation Heatmap

### `plot_correlation_heatmap(df, method, figsize)`

```python
def plot_correlation_heatmap(df: pd.DataFrame, method: str = 'pearson',
                              figsize: tuple = (16, 12)) -> None
```

**Description**
Renders a lower-triangle correlation heatmap with annotated coefficients. Uses a coolwarm diverging colormap centered at zero. The colorbar is labeled with the correlation method name.

**Parameters**

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `df` | `pd.DataFrame` | — | The dataset. |
| `method` | `str` | `'pearson'` | Correlation method. |
| `figsize` | `tuple` | `(16, 12)` | Figure dimensions in inches. |

**Returns**
`None` (displays a matplotlib figure).

---

### `plot_clustered_heatmap(df, method)`

```python
def plot_clustered_heatmap(df: pd.DataFrame, method: str = 'pearson') -> None
```

**Description**
Creates a Seaborn clustermap where rows and columns are reordered by hierarchical clustering. This groups correlated features visually, making block structure easier to spot.

**Parameters**

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `df` | `pd.DataFrame` | — | The dataset. |
| `method` | `str` | `'pearson'` | Correlation method. |

**Returns**
`None` (displays a matplotlib figure).

---

## Scatter & Pair Plots

### `plot_scatter(df, x, y, hue)`

```python
def plot_scatter(df: pd.DataFrame, x: str, y: str,
                 hue: str = None) -> None
```

**Description**
Scatter plot of two columns with an OLS regression line overlay. The title displays the Pearson r and p-value. An optional `hue` column adds color grouping using the eLocal brand palette.

**Parameters**

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `df` | `pd.DataFrame` | — | The dataset. |
| `x` | `str` | — | Column for the x-axis. |
| `y` | `str` | — | Column for the y-axis. |
| `hue` | `str` | `None` | Optional categorical column for color grouping. |

**Returns**
`None` (displays a matplotlib figure).

---

### `plot_pairplot(df, cols, hue)`

```python
def plot_pairplot(df: pd.DataFrame, cols: list = None,
                  hue: str = None) -> None
```

**Description**
Generates a Seaborn pair plot (scatter matrix) for a subset of columns. If more than 8 columns are selected, only the first 8 are used to keep the plot readable. Diagonal plots use KDE.

**Parameters**

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `df` | `pd.DataFrame` | — | The dataset. |
| `cols` | `list` | `None` | Column names to include. Defaults to all numeric columns. |
| `hue` | `str` | `None` | Optional categorical column for color grouping. |

**Returns**
`None` (displays a matplotlib figure).

---

## Categorical Cross-Tabs

### `crosstab_analysis(df, col_a, col_b, normalize)`

```python
def crosstab_analysis(df: pd.DataFrame, col_a: str, col_b: str,
                      normalize: str = 'index') -> pd.DataFrame
```

**Description**
Computes a cross-tabulation between two categorical columns with optional normalisation. Useful for understanding how category combinations are distributed.

**Parameters**

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `df` | `pd.DataFrame` | — | The dataset. |
| `col_a` | `str` | — | Row variable. |
| `col_b` | `str` | — | Column variable. |
| `normalize` | `str` | `'index'` | Normalise by `'index'` (rows), `'columns'`, `'all'`, or `None` for raw counts. |

**Returns**
`pd.DataFrame` — the cross-tabulation table.

---

### `plot_crosstab_heatmap(df, col_a, col_b)`

```python
def plot_crosstab_heatmap(df: pd.DataFrame, col_a: str, col_b: str) -> None
```

**Description**
Renders a heatmap of raw cross-tab counts between two categorical columns. Uses the eLocal sequential colormap and annotates each cell with the integer count.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| `df` | `pd.DataFrame` | The dataset. |
| `col_a` | `str` | Row variable. |
| `col_b` | `str` | Column variable. |

**Returns**
`None` (displays a matplotlib figure).

---

### `chi_squared_test(df, col_a, col_b)`

```python
def chi_squared_test(df: pd.DataFrame, col_a: str, col_b: str) -> dict
```

**Description**
Runs a chi-squared test of independence on the cross-tabulation of two categorical columns. Prints the test statistic, p-value, degrees of freedom, and significance at alpha = 0.05.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| `df` | `pd.DataFrame` | The dataset. |
| `col_a` | `str` | First categorical column. |
| `col_b` | `str` | Second categorical column. |

**Returns**
`dict` with keys: `chi2`, `p_value`, `dof`, `significant_at_05`.

---

## Target Leakage Detection

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

---

### `plot_target_correlations(df, target_col, top_n)`

```python
def plot_target_correlations(df: pd.DataFrame, target_col: str,
                              top_n: int = 20) -> None
```

**Description**
Horizontal bar chart showing each feature's correlation with the target column, sorted by absolute value. Features at or above 0.95 are highlighted in orange as potential leakage; all others are in blue.

**Parameters**

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `df` | `pd.DataFrame` | — | The dataset. |
| `target_col` | `str` | — | Name of the target / label column. |
| `top_n` | `int` | `20` | Number of top features to display. |

**Returns**
`None` (displays a matplotlib figure).

---

## Numeric vs Categorical Relationships

### `plot_numeric_by_category(df, numeric_col, cat_col, top_n)`

```python
def plot_numeric_by_category(df: pd.DataFrame, numeric_col: str,
                              cat_col: str, top_n: int = 10) -> None
```

**Description**
Box plot showing the distribution of a numeric column grouped by the top-N most frequent categories. Uses the eLocal brand palette and rotates x-axis labels for readability.

**Parameters**

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `df` | `pd.DataFrame` | — | The dataset. |
| `numeric_col` | `str` | — | Numeric column for the y-axis. |
| `cat_col` | `str` | — | Categorical column for grouping. |
| `top_n` | `int` | `10` | Number of top categories to include. |

**Returns**
`None` (displays a matplotlib figure).

---

### `anova_test(df, numeric_col, cat_col)`

```python
def anova_test(df: pd.DataFrame, numeric_col: str,
               cat_col: str) -> dict
```

**Description**
Performs a one-way ANOVA to test whether the mean of `numeric_col` differs significantly across groups defined by `cat_col`. Prints the F-statistic, p-value, and significance at alpha = 0.05.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| `df` | `pd.DataFrame` | The dataset. |
| `numeric_col` | `str` | Numeric column to compare across groups. |
| `cat_col` | `str` | Categorical column defining the groups. |

**Returns**
`dict` with keys: `F_statistic`, `p_value`, `significant_at_05`.
