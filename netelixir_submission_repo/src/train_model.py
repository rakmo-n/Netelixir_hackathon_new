"""
train_model.py
===============
OFFLINE TRAINING SCRIPT — run this yourself, once, before submitting.
run.sh does NOT call this file. The contract for the hackathon pipeline
is: features are generated from the test data, then a model that was
already trained and committed is loaded and used to predict. This script
is what produces that committed pickle/model.pkl in the first place.

Trains a HistGradientBoostingRegressor at each quantile in
model_common.QUANTILES, for each grain in PLATFORMS + TOP_CAMPAIGN_TYPES,
for each horizon in model_common.HORIZONS — using ALL available history
in the given features file (no held-out split, since this is the final
artifact to ship, not a validation run; validation/backtesting already
happened in project/stage4_probabilistic_forecasting).

USAGE
-----
    python src/train_model.py --features features.parquet --out pickle/model.pkl
"""

import argparse
import pickle
import sys
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import HistGradientBoostingRegressor

from model_common import (
    HORIZONS, QUANTILES, PLATFORMS, TOP_CAMPAIGN_TYPES,
    add_calendar_features, create_horizon_targets, build_feature_matrix,
)

MIN_ROWS_PER_GRAIN = 200
MIN_TRAIN_ROWS = 50


def train_quantile_model(X, y, quantile):
    model = HistGradientBoostingRegressor(
        loss="quantile",
        quantile=quantile,
        max_iter=300,
        early_stopping=True,
        validation_fraction=0.10,
        n_iter_no_change=20,
        random_state=42,
    )
    model.fit(X, y)
    return model


def train_for_grain_type(df, grain_col, grains, grain_type_label):
    df = add_calendar_features(df)
    models = {}  # grain -> horizon -> quantile -> fitted model

    for grain in grains:
        sub = df[df[grain_col] == grain].copy()
        if len(sub) < MIN_ROWS_PER_GRAIN:
            print(f"  [skip] {grain_type_label}='{grain}': only {len(sub)} rows (< {MIN_ROWS_PER_GRAIN})")
            continue

        sub = create_horizon_targets(sub)
        models[grain] = {}

        for H in HORIZONS:
            X, feature_names, valid = build_feature_matrix(sub, H)
            target_col = f"target_revenue_{H}d"
            usable = valid & sub[target_col].notna()

            X_train = X[usable].values
            y_train = sub.loc[usable, target_col].values

            if len(X_train) < MIN_TRAIN_ROWS:
                print(f"  [skip] {grain_type_label}='{grain}' H={H}: only {len(X_train)} usable rows")
                continue

            models[grain][H] = {}
            for q in QUANTILES:
                models[grain][H][q] = train_quantile_model(X_train, y_train, q)
            print(f"  [trained] {grain_type_label}='{grain}' H={H} on {len(X_train)} rows")

    return models


def run(features_path: str, out_path: str):
    df = pd.read_parquet(features_path)
    df["date"] = pd.to_datetime(df["date"])

    platform_df = df[df["grain_type"] == "platform"].rename(columns={"grain": "platform"})
    campaign_df = df[df["grain_type"] == "campaign_type"].rename(columns={"grain": "channel_grouping"})

    print("Training platform-level models...")
    platform_models = train_for_grain_type(platform_df, "platform", PLATFORMS, "platform")

    print("Training campaign-type-level models...")
    campaign_models = train_for_grain_type(campaign_df, "channel_grouping", TOP_CAMPAIGN_TYPES, "campaign_type")

    bundle = {
        "platform_models": platform_models,
        "campaign_type_models": campaign_models,
        "horizons": HORIZONS,
        "quantiles": QUANTILES,
        "sklearn_version": sklearn.__version__,
        "trained_at_utc": datetime.now(timezone.utc).isoformat(),
        "trained_on_features_file": features_path,
        "trained_on_n_rows": int(len(df)),
    }

    with open(out_path, "wb") as f:
        pickle.dump(bundle, f)

    n_models = sum(
        len(qs) for grains in (platform_models, campaign_models)
        for horizons in grains.values() for qs in horizons.values()
    )
    print(f"\nSaved {n_models} quantile models to {out_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--features", default="features.parquet")
    parser.add_argument("--out", default="pickle/model.pkl")
    args = parser.parse_args()
    run(args.features, args.out)
