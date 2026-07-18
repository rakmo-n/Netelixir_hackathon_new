"""
predict.py
==========
Step (b) of run.sh: load the pre-trained, pickled model and produce
predictions from the features generate_features.py just built.
Does NOT fit or retrain anything.

USAGE
-----
    python src/predict.py --features features.parquet --model pickle/model.pkl --output output/predictions.csv
"""

import argparse
import pickle

import numpy as np
import pandas as pd

from model_common import add_calendar_features, create_horizon_targets, build_feature_matrix


def predict_for_grain_type(df, grain_col, grain_models, grain_type_label):
    df = add_calendar_features(df)
    rows = []

    for grain, horizons in grain_models.items():
        sub = df[df[grain_col] == grain].copy()
        if sub.empty:
            continue
        sub = create_horizon_targets(sub)

        for H, quantile_models in horizons.items():
            X, _, valid = build_feature_matrix(sub, H)
            spend_col = f"target_spend_{H}d"
            usable = valid.values & sub[spend_col].notna().values
            if usable.sum() == 0:
                continue

            X_pred = X[usable].values
            dates = sub.loc[usable, "date"].values
            planned_spend = sub.loc[usable, spend_col].values
            actual_revenue = sub.loc[usable, f"target_revenue_{H}d"].values

            preds = {}
            for q, model in quantile_models.items():
                preds[q] = np.maximum(model.predict(X_pred), 0.0)

            q_sorted = sorted(preds.keys())
            for i in range(len(dates)):
                row = {
                    "grain_type": grain_type_label,
                    "grain": grain,
                    "forecast_origin_date": str(dates[i])[:10],
                    "horizon_days": H,
                    "planned_spend": round(float(planned_spend[i]), 2),
                }
                for q in q_sorted:
                    label = f"p{int(q * 100)}_revenue"
                    row[label] = round(float(preds[q][i]), 2)
                    if planned_spend[i] and planned_spend[i] > 0:
                        row[f"p{int(q * 100)}_roas"] = round(float(preds[q][i] / planned_spend[i]), 2)
                    else:
                        row[f"p{int(q * 100)}_roas"] = None
                # actual_revenue is only non-null when the horizon window is
                # fully contained in the data provided (useful for scoring /
                # sanity checks); it is NOT used as a model input.
                row["actual_revenue"] = (
                    round(float(actual_revenue[i]), 2) if not np.isnan(actual_revenue[i]) else None
                )
                rows.append(row)

    return rows


def run(features_path: str, model_path: str, output_path: str):
    with open(model_path, "rb") as f:
        bundle = pickle.load(f)

    df = pd.read_parquet(features_path)
    df["date"] = pd.to_datetime(df["date"])

    platform_df = df[df["grain_type"] == "platform"].rename(columns={"grain": "platform"})
    campaign_df = df[df["grain_type"] == "campaign_type"].rename(columns={"grain": "channel_grouping"})

    print("Predicting platform-level forecasts...")
    platform_rows = predict_for_grain_type(
        platform_df, "platform", bundle["platform_models"], "platform"
    )
    print("Predicting campaign-type-level forecasts...")
    campaign_rows = predict_for_grain_type(
        campaign_df, "channel_grouping", bundle["campaign_type_models"], "campaign_type"
    )

    all_rows = platform_rows + campaign_rows
    if not all_rows:
        raise RuntimeError(
            "No predictions were generated. This usually means the provided "
            "data/ does not contain enough history for any grain (need at "
            "least ~120 days of daily data covering a known platform / "
            "campaign type). See README for the expected schema."
        )

    out_df = pd.DataFrame(all_rows)
    out_df.to_csv(output_path, index=False)
    print(f"Wrote {len(out_df)} prediction rows to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--features", default="features.parquet")
    parser.add_argument("--model", default="pickle/model.pkl")
    parser.add_argument("--output", default="output/predictions.csv")
    args = parser.parse_args()
    run(args.features, args.model, args.output)
