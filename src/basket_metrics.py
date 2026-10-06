"""Simple audit checks and basket statistics."""

import numpy as np
import pandas as pd
from scipy import stats


def audit_report(df: pd.DataFrame) -> pd.DataFrame:
    """Return missingness, dtype, skew and 1.5-IQR outlier counts by column.

    Skew and outlier counts are unavailable for non-numeric columns.
    An outlier flag does not mean that the observation is an error.
    """
    rows = []

    for column in df.columns:
        values = df[column]
        skew = np.nan
        outliers = np.nan

        if pd.api.types.is_numeric_dtype(values) and not pd.api.types.is_bool_dtype(values):
            clean = values.dropna()
            if len(clean) > 0:
                q1 = clean.quantile(0.25)
                q3 = clean.quantile(0.75)
                iqr = q3 - q1
                lower = q1 - 1.5 * iqr
                upper = q3 + 1.5 * iqr
                outliers = ((clean < lower) | (clean > upper)).sum()
                skew = clean.skew()

        rows.append({
            "column": column,
            "missing_count": values.isna().sum(),
            "missing_pct": values.isna().mean() * 100,
            "dtype": str(values.dtype),
            "skew": skew,
            "outlier_count": outliers
        })

    return pd.DataFrame(rows).set_index("column")


def robust_mean(x: pd.Series | list[float], method: str = "median",
                trim_fraction: float = 0.10,
                exclude_mask: pd.Series | list[bool] | None = None) -> float:
    """Calculate a median, trimmed mean or mean after an explicit exclusion.

    trim_fraction is removed from each tail. For method='rule', provide
    a Boolean mask in the same row order as x; True means exclude.
    Missing values are dropped after the rule. Empty data raises an error.
    """
    values = pd.Series(x, dtype=float).reset_index(drop=True)

    if method == "rule":
        if exclude_mask is None:
            raise ValueError("Provide an exclusion mask for method='rule'.")
        mask = pd.Series(exclude_mask).reset_index(drop=True)
        if len(mask) != len(values) or mask.dtype != bool or mask.isna().any():
            raise ValueError("Use a Boolean mask with one value per observation.")
        values = values[~mask]

    values = values.dropna()
    if len(values) == 0:
        raise ValueError("No observations remain.")
    if np.isinf(values).any():
        raise ValueError("Values must be finite.")

    if method == "median":
        return float(values.median())
    elif method == "trimmed":
        if trim_fraction < 0 or trim_fraction >= 0.5:
            raise ValueError("trim_fraction must be between 0 and 0.5.")
        return float(stats.trim_mean(values, trim_fraction))
    elif method == "rule":
        return float(values.mean())
    else:
        raise ValueError("Choose median, trimmed or rule.")


if __name__ == "__main__":
    example = pd.DataFrame({
        "basket_value": [20., 30., 40., 2000., np.nan],
        "customer_type": ["consumer", "consumer", "consumer", "B2B", "consumer"]
    })
    print(audit_report(example))
    print("Median:", robust_mean(example["basket_value"], "median"))
    print("Trimmed mean:", robust_mean(example["basket_value"], "trimmed", 0.25))
    print("Consumer mean:", robust_mean(
        example["basket_value"], "rule",
        exclude_mask=example["customer_type"] == "B2B"
    ))
