"""
generate_features.py
=====================
Step (a) of run.sh: build the feature matrix the model needs, straight
from whatever is inside DATA_DIR.

Adapted from project/stage2_eda_feature_engineering/scripts/eda_feature_engineering.py
(decomposition, ROAS-distribution, and plotting code removed — not needed
for prediction, only for the exploratory report).

INPUT DISCOVERY (schema-based, not filename-based)
---------------------------------------------------
DATA_DIR is scanned for every *.csv file. Each file is classified by its
columns, not its name, so the pipeline still works if the test harness
names the files differently:

  - "ad spend" file   : has a `date` column and a `spend` column
                        (expected columns also include platform,
                        channel_grouping)
  - "orders/revenue" file : has an `order_date` column and a `revenue`
                        column (expected columns also include platform,
                        channel_grouping)

If multiple files match a category, they are concatenated. At least one
file of each category is required.

OUTPUT
------
features.parquet — engineered features at both the (date, platform) grain
and the (date, channel_grouping) grain, stacked together with a
`grain_type` column ('platform' or 'campaign_type') so a single file can
feed src/predict.py.

USAGE
-----
    python src/generate_features.py --data-dir ./data --out features.parquet
"""

import argparse
import glob
import os

import numpy as np
import pandas as pd

pd.options.mode.chained_assignment = None


# ---------------------------------------------------------------------------
# 1. INPUT DISCOVERY
# ---------------------------------------------------------------------------

def _load_and_classify(data_dir: str):
    csv_paths = sorted(glob.glob(os.path.join(data_dir, "*.csv")))
    if not csv_paths:
        raise FileNotFoundError(f"No CSV files found in {data_dir}")

    ad_frames, order_frames = [], []
    for path in csv_paths:
        try:
            head = pd.read_csv(path, nrows=5)
        except Exception as e:
            print(f"  [skip] could not read {path}: {e}")
            continue
        cols = set(head.columns)

        if "date" in cols and "spend" in cols:
            df = pd.read_csv(path, parse_dates=["date"])
            ad_frames.append(df)
            print(f"  [ad-spend file]   {path} ({len(df)} rows)")
        elif "order_date" in cols and "revenue" in cols:
            df = pd.read_csv(path, parse_dates=["order_date"])
            order_frames.append(df)
            print(f"  [orders file]     {path} ({len(df)} rows)")
        else:
            print(f"  [unrecognized]    {path} — columns {sorted(cols)}")

    if not ad_frames:
        raise ValueError(
            "No ad-spend file found in data/. Expected a CSV with at least "
            "'date' and 'spend' columns (see README for full schema)."
        )
    if not order_frames:
        raise ValueError(
            "No orders/revenue file found in data/. Expected a CSV with at "
            "least 'order_date' and 'revenue' columns (see README)."
        )

    ad = pd.concat(ad_frames, ignore_index=True)
    orders = pd.concat(order_frames, ignore_index=True)
    return ad, orders


# ---------------------------------------------------------------------------
# 2. DAILY SERIES (per grain)
# ---------------------------------------------------------------------------

def build_daily_series(ad: pd.DataFrame, orders: pd.DataFrame, grain_col: str) -> pd.DataFrame:
    spend = ad.groupby(["date", grain_col])["spend"].sum().reset_index()
    revenue = (
        orders.groupby(["order_date", grain_col])["revenue"].sum().reset_index()
        .rename(columns={"order_date": "date"})
    )

    full_dates = pd.date_range(
        min(ad["date"].min(), orders["order_date"].min()),
        max(ad["date"].max(), orders["order_date"].max()),
        freq="D",
    )
    keys = sorted(set(spend[grain_col]) | set(revenue[grain_col]))
    full_index = pd.MultiIndex.from_product([full_dates, keys], names=["date", grain_col])

    out = (
        pd.DataFrame(index=full_index).reset_index()
        .merge(spend, on=["date", grain_col], how="left")
        .merge(revenue, on=["date", grain_col], how="left")
    )
    out[["spend", "revenue"]] = out[["spend", "revenue"]].fillna(0.0)
    return out.sort_values(["date", grain_col]).reset_index(drop=True)


# ---------------------------------------------------------------------------
# 3. FEATURE ENGINEERING (lags, rolling means, calendar, spend share)
# ---------------------------------------------------------------------------

def engineer_features(df: pd.DataFrame, grain_col: str) -> pd.DataFrame:
    df = df.copy()

    daily_totals = df.groupby("date")["spend"].sum().rename("spend_total_that_day")
    df = df.merge(daily_totals, on="date", how="left")
    df["spend_share_of_total"] = np.where(
        df["spend_total_that_day"] > 0, df["spend"] / df["spend_total_that_day"], 0.0
    )

    df["day_of_week"] = df["date"].dt.day_name()
    df["is_weekend"] = df["date"].dt.dayofweek >= 5

    grouped = df.groupby(grain_col, group_keys=False)
    for lag in (1, 7, 14):
        df[f"spend_lag_{lag}"] = grouped["spend"].shift(lag)
    for window in (7, 14, 30):
        df[f"spend_rolling_mean_{window}d"] = grouped["spend"].transform(
            lambda s: s.shift(1).rolling(window, min_periods=max(2, window // 2)).mean()
        )
        df[f"revenue_rolling_mean_{window}d"] = grouped["revenue"].transform(
            lambda s: s.shift(1).rolling(window, min_periods=max(2, window // 2)).mean()
        )

    return df.drop(columns=["spend_total_that_day"])


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def run(data_dir: str, out_path: str):
    print(f"Reading input from {data_dir} ...")
    ad, orders = _load_and_classify(data_dir)

    daily_by_platform = build_daily_series(ad, orders, "platform")
    daily_by_campaign_type = build_daily_series(ad, orders, "channel_grouping")

    feat_platform = engineer_features(daily_by_platform, "platform")
    feat_platform["grain_type"] = "platform"
    feat_platform = feat_platform.rename(columns={"platform": "grain"})

    feat_campaign = engineer_features(daily_by_campaign_type, "channel_grouping")
    feat_campaign["grain_type"] = "campaign_type"
    feat_campaign = feat_campaign.rename(columns={"channel_grouping": "grain"})

    combined = pd.concat([feat_platform, feat_campaign], ignore_index=True)
    combined.to_parquet(out_path, index=False)
    print(f"Wrote {out_path} ({len(combined)} rows, {combined['grain'].nunique()} grains)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", default="./data")
    parser.add_argument("--out", default="features.parquet")
    args = parser.parse_args()
    run(args.data_dir, args.out)
