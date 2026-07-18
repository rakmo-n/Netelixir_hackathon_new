"""
Stage 4: Probabilistic Forecasting Core
========================================
Train HistGradientBoostingRegressor at multiple quantiles (0.10, 0.50, 0.90)
to predict cumulative revenue and ROAS over 30/60/90-day horizons.

MODEL
-----
  sklearn.ensemble.HistGradientBoostingRegressor
  loss='quantile' + alpha for each target quantile.
  Separate models per grain (platform / campaign_type) and per horizon.

FEATURES
--------
  Historical spend state:
    spend, spend_lag_1/7/14, spend_rolling_mean_7d/14d/30d
    revenue_rolling_mean_7d/14d/30d, spend_share_of_total
  Calendar / trend:
    days_since_start, month_sin/cos, dayofmonth_sin/cos,
    is_weekend, day_of_week (one-hot)
  Planned spend (budget input):
    target_spend_H — cumulative future spend over the horizon.
    During training this is the actual observed spend.
    During inference (budget simulation) it is the user's hypothetical budget.

TARGETS
-------
  target_revenue_H = sum of revenue from t+1 to t+H
  target_roas_H    = target_revenue_H / target_spend_H (derived)

WALK-FORWARD VALIDATION
-----------------------
  Train on all dates before 2026-02-01.
  Test  on 2026-02-01 to 2026-03-01 (30 days).
  This is an expanding-window holdout — no future data leaks into training.

EVALUATION METRICS
------------------
  Pinball loss at p10, p50, p90
  Interval coverage: does the [p10, p90] band contain the true value?
  MAE and RMSE at the median (p50)
  Mean interval width

OUTPUTS
-------
  outputs/probabilistic_forecasts.csv  - every test-date forecast with bands
  outputs/validation_metrics.csv       - per-grain/horizon summary
  outputs/feature_importances.csv      - top features per grain/horizon/q
  outputs/diagnostic_plots/*.png       - fan charts and p50-vs-actual overlays

USAGE
-----
    python probabilistic_forecaster.py \
        --features-channel features_by_channel.csv \
        --features-campaign-type features_by_campaign_type.csv \
        --outdir ./output
"""

import argparse
import os
import warnings
from pathlib import Path

os.environ["LOKY_MAX_CPU_COUNT"] = "1"

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.inspection import permutation_importance

warnings.filterwarnings("ignore")
pd.options.mode.chained_assignment = None

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------

HORIZONS = [30, 60, 90]
QUANTILES = [0.10, 0.50, 0.90]
TRAIN_CUTOFF = "2026-02-01"
TEST_END = "2026-03-01"

PLATFORMS = ["Bing Ads", "Google Ads", "Meta Ads", "Organic/Direct"]
TOP_CAMPAIGN_TYPES = [
    "Search", "Pmax", "Direct", "Organic_Search", "Email",
    "Shopping", "Organic_Search_Bing", "Remarketing_DPA",
    "Organic_Social", "Remarketing_Brand",
]


# ---------------------------------------------------------------------------
# TARGET ENGINEERING
# ---------------------------------------------------------------------------

def create_horizon_targets(df):
    """Add future cumulative revenue and spend targets for each horizon.

    For date t, target_revenue_H = sum of revenue from t+1 to t+H.
    Computed with shift(-1) so the future values are aligned to the
    current feature row.  The last H rows naturally become NaN.
    """
    df = df.sort_values("date").reset_index(drop=True)
    for H in HORIZONS:
        # Shift(-1) moves t+1 to index t, then rolling(H) sums t+1 … t+H
        df[f"target_revenue_{H}d"] = (
            df["revenue"].shift(-1).rolling(H, min_periods=H).sum().shift(H - 1)
        )
        df[f"target_spend_{H}d"] = (
            df["spend"].shift(-1).rolling(H, min_periods=H).sum().shift(H - 1)
        )
    return df


# ---------------------------------------------------------------------------
# FEATURE ENGINEERING
# ---------------------------------------------------------------------------

def engineer_features(df):
    """Add cyclic month, trend, and calendar features."""
    df = df.copy()
    df["days_since_start"] = (df["date"] - df["date"].min()).dt.days
    df["month_sin"] = np.sin(2 * np.pi * df["date"].dt.month / 12)
    df["month_cos"] = np.cos(2 * np.pi * df["date"].dt.month / 12)
    df["dayofmonth_sin"] = np.sin(2 * np.pi * df["date"].dt.day / 31)
    df["dayofmonth_cos"] = np.cos(2 * np.pi * df["date"].dt.day / 31)
    return df


def build_feature_matrix(df, horizon):
    """Return X (features), feature_names, and a validity mask.

    The planned-spend column for the horizon is included so the model can
    condition on a future budget level.  During training this is the actual
    observed spend; during budget simulation it is the user's input.
    """
    base_cols = [
        "spend", "spend_lag_1", "spend_lag_7", "spend_lag_14",
        "spend_rolling_mean_7d", "spend_rolling_mean_14d", "spend_rolling_mean_30d",
        "revenue_rolling_mean_7d", "revenue_rolling_mean_14d", "revenue_rolling_mean_30d",
        "spend_share_of_total",
        "days_since_start", "month_sin", "month_cos",
        "dayofmonth_sin", "dayofmonth_cos",
        "is_weekend",
    ]

    spend_col = f"target_spend_{horizon}d"
    if spend_col in df.columns:
        base_cols.append(spend_col)

    # One-hot day_of_week (drop Monday to avoid collinearity)
    day_dummies = pd.get_dummies(df["day_of_week"], prefix="dow", drop_first=True)

    X = pd.concat([df[base_cols], day_dummies], axis=1)
    valid = X.notna().all(axis=1)
    return X, base_cols + list(day_dummies.columns), valid


# ---------------------------------------------------------------------------
# MODEL FITTING
# ---------------------------------------------------------------------------

def train_quantile_model(X, y, quantile):
    """Fit a single HistGradientBoostingRegressor for the requested quantile."""
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


# ---------------------------------------------------------------------------
# METRICS
# ---------------------------------------------------------------------------

def pinball_loss(y_true, y_pred, quantile):
    diff = y_true - y_pred
    return np.mean(np.where(diff >= 0, quantile * diff, (quantile - 1) * diff))


def coverage_rate(y_true, y_lower, y_upper):
    return np.mean((y_true >= y_lower) & (y_true <= y_upper))


# ---------------------------------------------------------------------------
# PLOTTING
# ---------------------------------------------------------------------------

def plot_fan_chart(grain, label, horizon, dates, actual, preds, outpath):
    """Fan chart: p10–p90 shaded band, p50 line, actual overlay."""
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(dates))

    ax.fill_between(
        x, preds[0.10], preds[0.90],
        alpha=0.25, color="tab:blue", label="10%–90% interval"
    )
    ax.plot(x, preds[0.50], color="tab:blue", linewidth=2, label="p50 forecast")
    ax.plot(x, actual, color="tab:orange", linewidth=1.5, label="actual")

    ax.set_title(f"{label} {grain} — {horizon}-day cumulative revenue forecast")
    ax.set_xlabel("Test date index")
    ax.set_ylabel("Revenue")
    ax.legend()
    fig.tight_layout()
    fig.savefig(outpath, dpi=110)
    plt.close(fig)


def plot_interval_coverage(grain, label, horizon, dates, actual, preds, outpath):
    """Overlay showing which actual points fall inside the forecast band."""
    fig, ax = plt.subplots(figsize=(10, 4))
    x = np.arange(len(dates))

    inside = (actual >= preds[0.10]) & (actual <= preds[0.90])
    colors = np.where(inside, "tab:green", "tab:red")

    ax.fill_between(x, preds[0.10], preds[0.90], alpha=0.20, color="tab:blue")
    ax.scatter(x, actual, c=colors, s=30, zorder=3, label="actual")
    ax.plot(x, preds[0.50], color="tab:blue", linewidth=1.5, label="p50")

    ax.set_title(f"{label} {grain} — {horizon}-day interval coverage "
                 f"({inside.mean()*100:.1f}% inside band)")
    ax.set_xlabel("Test date index")
    ax.set_ylabel("Revenue")
    ax.legend()
    fig.tight_layout()
    fig.savefig(outpath, dpi=110)
    plt.close(fig)


# ---------------------------------------------------------------------------
# CORE FORECAST LOOP
# ---------------------------------------------------------------------------

def run_forecast(features_path, grain_col, grains, outdir, label):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    plots_dir = outdir / "diagnostic_plots"
    plots_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(features_path, parse_dates=["date"])
    df = engineer_features(df)

    all_forecasts = []
    all_metrics = []
    all_importances = []

    for grain in grains:
        sub = df[df[grain_col] == grain].copy()
        if len(sub) < 200:
            continue

        sub = create_horizon_targets(sub)

        for H in HORIZONS:
            X, feature_names, valid = build_feature_matrix(sub, H)
            target_col = f"target_revenue_{H}d"

            usable = valid & sub[target_col].notna()
            train_mask = (sub["date"] < pd.Timestamp(TRAIN_CUTOFF)) & usable
            test_mask = (
                (sub["date"] >= pd.Timestamp(TRAIN_CUTOFF))
                & (sub["date"] < pd.Timestamp(TEST_END))
                & usable
            )

            X_train = X[train_mask].values
            y_train = sub.loc[train_mask, target_col].values
            X_test = X[test_mask].values
            y_test = sub.loc[test_mask, target_col].values
            test_dates = sub.loc[test_mask, "date"].values

            if len(X_train) < 50 or len(X_test) < 5:
                continue

            # Train quantile models
            models = {}
            preds = {}
            for q in QUANTILES:
                models[q] = train_quantile_model(X_train, y_train, q)
                preds[q] = np.maximum(models[q].predict(X_test), 0)  # revenue >= 0

            # ---- Store forecasts (with ROAS derived) ----
            for i, date in enumerate(test_dates):
                match = sub[sub["date"] == pd.Timestamp(date)]
                actual_spend = match[f"target_spend_{H}d"].iloc[0] if not match.empty else np.nan
                actual_roas = y_test[i] / actual_spend if actual_spend and actual_spend > 0 else np.nan

                p10_roas = preds[0.10][i] / actual_spend if actual_spend and actual_spend > 0 else np.nan
                p50_roas = preds[0.50][i] / actual_spend if actual_spend and actual_spend > 0 else np.nan
                p90_roas = preds[0.90][i] / actual_spend if actual_spend and actual_spend > 0 else np.nan

                all_forecasts.append({
                    "grain": grain,
                    "level": label,
                    "forecast_origin_date": str(date)[:10],
                    "horizon_days": H,
                    "actual_revenue": round(y_test[i], 2),
                    "p10_revenue": round(preds[0.10][i], 2),
                    "p50_revenue": round(preds[0.50][i], 2),
                    "p90_revenue": round(preds[0.90][i], 2),
                    "actual_spend": round(actual_spend, 2) if not pd.isna(actual_spend) else None,
                    "actual_roas": round(actual_roas, 2) if not pd.isna(actual_roas) else None,
                    "p10_roas": round(p10_roas, 2) if not pd.isna(p10_roas) else None,
                    "p50_roas": round(p50_roas, 2) if not pd.isna(p50_roas) else None,
                    "p90_roas": round(p90_roas, 2) if not pd.isna(p90_roas) else None,
                })

            # ---- Metrics ----
            mae = np.mean(np.abs(y_test - preds[0.50]))
            rmse = np.sqrt(np.mean((y_test - preds[0.50]) ** 2))

            all_metrics.append({
                "grain": grain,
                "level": label,
                "horizon_days": H,
                "n_train": len(X_train),
                "n_test": len(X_test),
                "mae": round(mae, 2),
                "rmse": round(rmse, 2),
                "pinball_p10": round(pinball_loss(y_test, preds[0.10], 0.10), 2),
                "pinball_p50": round(pinball_loss(y_test, preds[0.50], 0.50), 2),
                "pinball_p90": round(pinball_loss(y_test, preds[0.90], 0.90), 2),
                "coverage_p10_p90": round(coverage_rate(y_test, preds[0.10], preds[0.90]), 3),
                "mean_interval_width": round(np.mean(preds[0.90] - preds[0.10]), 2),
                "train_mean_revenue": round(y_train.mean(), 2),
                "test_mean_revenue": round(y_test.mean(), 2),
            })

            # ---- Feature importances (permutation on a small validation subsample) ----
            # HistGradientBoostingRegressor in sklearn 1.9 does not expose
            # native feature_importances_; we use permutation_importance instead.
            for q in QUANTILES:
                # Subsample test set for speed (max 200 rows)
                n_imp = min(len(X_test), 200)
                idx_imp = np.random.RandomState(42).choice(len(X_test), n_imp, replace=False)
                X_imp = X_test[idx_imp]
                y_imp = y_test[idx_imp]
                r = permutation_importance(
                    models[q], X_imp, y_imp,
                    n_repeats=3, random_state=42, n_jobs=1, scoring="neg_mean_absolute_error"
                )
                for name, imp in zip(feature_names, r.importances_mean):
                    all_importances.append({
                        "grain": grain,
                        "level": label,
                        "horizon_days": H,
                        "quantile": q,
                        "feature": name,
                        "importance": round(imp, 4),
                    })

            # ---- Diagnostic plots ----
            safe_grain = grain.replace("/", "-")
            plot_fan_chart(
                grain, label, H, test_dates, y_test, preds,
                plots_dir / f"fan_{label}_{safe_grain}_H{H}.png"
            )
            plot_interval_coverage(
                grain, label, H, test_dates, y_test, preds,
                plots_dir / f"coverage_{label}_{safe_grain}_H{H}.png"
            )

    # ---- Persist ----
    forecasts_df = pd.DataFrame(all_forecasts)
    metrics_df = pd.DataFrame(all_metrics)
    importances_df = pd.DataFrame(all_importances)

    if not forecasts_df.empty:
        forecasts_df.to_csv(outdir / "probabilistic_forecasts.csv", index=False)
    if not metrics_df.empty:
        metrics_df.to_csv(outdir / "validation_metrics.csv", index=False)
    if not importances_df.empty:
        importances_df.to_csv(outdir / "feature_importances.csv", index=False)

    print(f"  [{label}] forecasts={len(forecasts_df)} rows, metrics={len(metrics_df)} rows, "
          f"plots={len(list(plots_dir.glob('*.png')))} PNGs")
    return forecasts_df, metrics_df, importances_df


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def run(features_channel_path, features_campaign_type_path, outdir):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    print("Stage 4 – Probabilistic Forecasting Core")
    print("=" * 45)

    f1, m1, i1 = run_forecast(
        features_channel_path, "platform", PLATFORMS,
        outdir / "platform", "platform"
    )
    f2, m2, i2 = run_forecast(
        features_campaign_type_path, "channel_grouping", TOP_CAMPAIGN_TYPES,
        outdir / "campaign_type", "campaign_type"
    )

    # Combine cross-grain outputs
    for name, frames in [
        ("probabilistic_forecasts.csv", [f1, f2]),
        ("validation_metrics.csv", [m1, m2]),
        ("feature_importances.csv", [i1, i2]),
    ]:
        combined = pd.concat(frames, ignore_index=True)
        if not combined.empty:
            combined.to_csv(outdir / name, index=False)
            print(f"  Combined -> {outdir / name} ({len(combined)} rows)")

    print("\nStage 4 complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--features-channel", default="features_by_channel.csv")
    parser.add_argument("--features-campaign-type", default="features_by_campaign_type.csv")
    parser.add_argument("--outdir", default="./output")
    args = parser.parse_args()
    run(args.features_channel, args.features_campaign_type, args.outdir)
