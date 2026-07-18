"""
model_common.py
================
Shared logic between src/train_model.py (run once, offline, to produce
pickle/model.pkl) and src/predict.py (run by run.sh at test time).

Adapted from project/stage4_probabilistic_forecasting/scripts/probabilistic_forecaster.py.
Keeping this in one place guarantees the feature matrix predict.py builds
is byte-for-byte the same shape the model was trained on.
"""

import numpy as np
import pandas as pd

HORIZONS = [30, 60, 90]
QUANTILES = [0.10, 0.50, 0.90]

PLATFORMS = ["Bing Ads", "Google Ads", "Meta Ads", "Organic/Direct"]
TOP_CAMPAIGN_TYPES = [
    "Search", "Pmax", "Direct", "Organic_Search", "Email",
    "Shopping", "Organic_Search_Bing", "Remarketing_DPA",
    "Organic_Social", "Remarketing_Brand",
]

BASE_FEATURE_COLS = [
    "spend", "spend_lag_1", "spend_lag_7", "spend_lag_14",
    "spend_rolling_mean_7d", "spend_rolling_mean_14d", "spend_rolling_mean_30d",
    "revenue_rolling_mean_7d", "revenue_rolling_mean_14d", "revenue_rolling_mean_30d",
    "spend_share_of_total",
    "days_since_start", "month_sin", "month_cos",
    "dayofmonth_sin", "dayofmonth_cos",
    "is_weekend",
]

DOW_COLUMNS = ["dow_Monday", "dow_Saturday", "dow_Sunday", "dow_Thursday", "dow_Tuesday", "dow_Wednesday"]
# ("Friday" dropped as the reference level, matching drop_first=True on the
#  alphabetically-sorted day names used at training time.)


def add_calendar_features(df: pd.DataFrame) -> pd.DataFrame:
    """Cyclic month / day-of-month + trend index. Same date range in
    training and prediction data will not perfectly align 'days_since_start'
    across runs — this is expected and consistent with the original design
    (the model conditions on absolute trend position, not relative)."""
    df = df.copy()
    df["days_since_start"] = (df["date"] - df["date"].min()).dt.days
    df["month_sin"] = np.sin(2 * np.pi * df["date"].dt.month / 12)
    df["month_cos"] = np.cos(2 * np.pi * df["date"].dt.month / 12)
    df["dayofmonth_sin"] = np.sin(2 * np.pi * df["date"].dt.day / 31)
    df["dayofmonth_cos"] = np.cos(2 * np.pi * df["date"].dt.day / 31)
    return df


def create_horizon_targets(df: pd.DataFrame) -> pd.DataFrame:
    """Forward-looking cumulative revenue/spend targets per horizon."""
    df = df.sort_values("date").reset_index(drop=True)
    for H in HORIZONS:
        df[f"target_revenue_{H}d"] = (
            df["revenue"].shift(-1).rolling(H, min_periods=H).sum().shift(H - 1)
        )
        df[f"target_spend_{H}d"] = (
            df["spend"].shift(-1).rolling(H, min_periods=H).sum().shift(H - 1)
        )
    return df


def build_feature_matrix(df: pd.DataFrame, horizon: int):
    """Return X (aligned to BASE_FEATURE_COLS + fixed dow dummy columns),
    feature name list, and a validity mask. Using a *fixed* dow column list
    (rather than pd.get_dummies on whatever days happen to appear) is the
    key fix vs. the original notebook code — it guarantees train-time and
    predict-time matrices have identical columns even if a test slice
    happens to be missing a particular weekday."""
    base_cols = list(BASE_FEATURE_COLS)
    spend_col = f"target_spend_{horizon}d"
    if spend_col in df.columns:
        base_cols.append(spend_col)

    day_dummies = pd.get_dummies(df["day_of_week"], prefix="dow")
    for col in DOW_COLUMNS:
        if col not in day_dummies.columns:
            day_dummies[col] = False
    day_dummies = day_dummies[DOW_COLUMNS]

    X = pd.concat([df[base_cols].reset_index(drop=True), day_dummies.reset_index(drop=True)], axis=1)
    valid = X.notna().all(axis=1)
    return X, base_cols + DOW_COLUMNS, valid
