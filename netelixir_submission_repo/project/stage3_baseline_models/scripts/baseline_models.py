"""
Stage 3: Baseline Deterministic Models (Sanity-Check Layer)
===========================================================

PURPOSE
-------
Before building probabilistic forecasters (Stage 4), fit simple deterministic
baselines per platform and per top campaign-type to confirm the pipeline
produces sane point forecasts.  This is a pipeline-correctness gate, not the
submission model.

MODELS FITTED
-------------
  1. Exponential Smoothing (Holt-Winters, additive trend + weekly seasonality)
     -- statsmodels.tsa.holtwinters.ExponentialSmoothing
  2. Seasonal Naive baseline (last observed value from the same day-of-week)
     -- cheap, interpretable, hard to beat on weekly-seasonal data

WALK-FORWARD VALIDATION
-----------------------
A single expanding-window split is used for speed (train on first N days,
forecast the final 90 days).  The last 90 days of the series are held out;
models are trained on everything before that.  This mirrors the "execute at
next-open" discipline from trading: no future data leaks into the training
set.

OUTPUTS
-------
  outputs/baseline_forecasts.csv        - point forecasts (30/60/90 days) per
                                          platform / channel_grouping
  outputs/validation_metrics.csv        - MAE, RMSE, MAPE on the 90-day holdout
  outputs/diagnostic_plots/*.png        - holdout actuals vs. forecast overlay
  outputs/sanity_check_report.txt       - narrative: which series are
                                          forecastable, which are too sparse,
                                          and whether the numbers pass the
                                          smell test

USAGE
-----
    python baseline_models.py \
        --features-channel features_by_channel.csv \
        --features-campaign-type features_by_campaign_type.csv \
        --outdir ./output
"""

import argparse
import json
import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

warnings.filterwarnings("ignore", category=UserWarning)
pd.options.mode.chained_assignment = None

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------

HOLDOUT_DAYS = 90
FORECAST_HORIZONS = [30, 60, 90]
MIN_NONZERO_DAYS = 60  # need at least this many non-zero days to attempt a model
MIN_TOTAL_DAYS = 120   # need at least this much history overall

# Which grains to model
PLATFORMS = ["Bing Ads", "Google Ads", "Meta Ads", "Organic/Direct"]
TOP_CAMPAIGN_TYPES = [
    "Search", "Pmax", "Direct", "Organic_Search", "Email",
    "Shopping", "Organic_Search_Bing", "Remarketing_DPA",
    "Organic_Social", "Remarketing_Brand",
]


def mape(y_true, y_pred):
    """Mean Absolute Percentage Error (safely handles zeros)."""
    mask = y_true != 0
    if not mask.any():
        return np.nan
    return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100


def seasonal_naive_forecast(series, horizon, period=7):
    """Return the last `period` observed values repeated to cover `horizon`."""
    tail = series[-period:].values
    repeats = int(np.ceil(horizon / period))
    return np.tile(tail, repeats)[:horizon]


# ---------------------------------------------------------------------------
# MODEL FITTING
# ---------------------------------------------------------------------------

def fit_exp_smooth(train_series, seasonal_periods=7):
    """Fit Holt-Winters additive trend + additive seasonal."""
    try:
        model = ExponentialSmoothing(
            train_series,
            trend="add",
            seasonal="add",
            seasonal_periods=seasonal_periods,
            damped_trend=False,
        )
        fitted = model.fit(optimized=True, remove_bias=False)
        return fitted
    except Exception as exc:
        return None


def run_baseline_for_series(df, grain_col, grain_value, value_col="revenue"):
    """Run baseline models for one series.  Returns a dict of results."""
    sub = df[df[grain_col] == grain_value].sort_values("date").reset_index(drop=True)
    if len(sub) < MIN_TOTAL_DAYS:
        return {"status": "skipped", "reason": "insufficient_history", "grain": grain_value}

    nonzero = (sub[value_col] > 0).sum()
    if nonzero < MIN_NONZERO_DAYS:
        return {"status": "skipped", "reason": "too_sparse", "grain": grain_value, "nonzero_days": int(nonzero)}

    series = sub[value_col].fillna(0.0)
    train = series.iloc[:-HOLDOUT_DAYS]
    test = series.iloc[-HOLDOUT_DAYS:]

    # --- Holt-Winters ---
    hw_fitted = fit_exp_smooth(train)
    if hw_fitted is None:
        return {"status": "failed", "reason": "hw_fit_failed", "grain": grain_value}

    hw_pred = hw_fitted.forecast(steps=HOLDOUT_DAYS)
    hw_pred = np.maximum(hw_pred, 0)  # revenue can't be negative

    # --- Seasonal Naive ---
    sn_pred = seasonal_naive_forecast(train, HOLDOUT_DAYS)

    # --- Metrics on holdout ---
    metrics = {
        "grain": grain_value,
        "train_days": len(train),
        "test_days": len(test),
        "train_mean": round(train.mean(), 2),
        "test_mean": round(test.mean(), 2),
        "hw_mae": round(np.mean(np.abs(test.values - hw_pred)), 2),
        "hw_rmse": round(np.sqrt(np.mean((test.values - hw_pred) ** 2)), 2),
        "hw_mape": round(mape(test.values, hw_pred), 2),
        "sn_mae": round(np.mean(np.abs(test.values - sn_pred)), 2),
        "sn_rmse": round(np.sqrt(np.mean((test.values - sn_pred) ** 2)), 2),
        "sn_mape": round(mape(test.values, sn_pred), 2),
    }

    # --- Forecasts beyond the holdout (30/60/90) ---
    # We re-fit on the FULL series so the forecast origin is the last observed day.
    hw_full = fit_exp_smooth(series)
    hw_forecasts = {}
    if hw_full is not None:
        for h in FORECAST_HORIZONS:
            f = hw_full.forecast(steps=h)
            hw_forecasts[h] = round(np.maximum(f, 0).sum(), 2)
    else:
        for h in FORECAST_HORIZONS:
            hw_forecasts[h] = np.nan

    # Seasonal naive forecast from full series
    sn_forecasts = {}
    for h in FORECAST_HORIZONS:
        sn_forecasts[h] = round(np.maximum(seasonal_naive_forecast(series, h), 0).sum(), 2)

    return {
        "status": "ok",
        "grain": grain_value,
        "metrics": metrics,
        "hw_forecasts": hw_forecasts,
        "sn_forecasts": sn_forecasts,
        "actual_last_30": round(test.values[:30].sum(), 2),
        "actual_last_60": round(test.values[:60].sum(), 2),
        "actual_last_90": round(test.values[:90].sum(), 2),
        "train_series": train,
        "test_series": test,
        "hw_pred": hw_pred,
        "sn_pred": sn_pred,
    }


# ---------------------------------------------------------------------------
# PLOTTING
# ---------------------------------------------------------------------------

def plot_holdout_overlay(result, grain_label, outpath: Path):
    if result["status"] != "ok":
        return

    fig, ax = plt.subplots(figsize=(10, 5))
    test = result["test_series"]
    hw_pred = result["hw_pred"]
    sn_pred = result["sn_pred"]
    days = np.arange(1, len(test) + 1)

    ax.plot(days, test.values, label="Actual", color="#1f77b4", linewidth=1.5)
    ax.plot(days, hw_pred, label="Holt-Winters", color="#ff7f0e", linewidth=1.5, linestyle="--")
    ax.plot(days, sn_pred, label="Seasonal Naive", color="#2ca02c", linewidth=1.0, linestyle=":")

    ax.axvline(x=30, color="gray", linewidth=0.5, linestyle="-.")
    ax.axvline(x=60, color="gray", linewidth=0.5, linestyle="-.")

    ax.set_title(f"{grain_label} – 90-day holdout vs. baseline forecasts")
    ax.set_xlabel("Day of holdout")
    ax.set_ylabel("Revenue")
    ax.legend()
    fig.tight_layout()
    fig.savefig(outpath, dpi=110)
    plt.close(fig)


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def run(features_channel_path, features_campaign_type_path, outdir):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    plots_dir = outdir / "diagnostic_plots"
    plots_dir.mkdir(parents=True, exist_ok=True)

    features_ch = pd.read_csv(features_channel_path, parse_dates=["date"])
    features_ct = pd.read_csv(features_campaign_type_path, parse_dates=["date"])

    all_results = []
    skipped = []
    failed = []

    # --- Platform-level baselines ---
    for platform in PLATFORMS:
        if platform not in features_ch["platform"].values:
            skipped.append({"grain": platform, "level": "platform", "reason": "not_in_dataset"})
            continue
        res = run_baseline_for_series(features_ch, "platform", platform)
        if res["status"] == "ok":
            all_results.append({"level": "platform", **res})
        elif res["status"] == "skipped":
            skipped.append({"grain": platform, "level": "platform", "reason": res["reason"]})
        else:
            failed.append({"grain": platform, "level": "platform", "reason": res["reason"]})

    # --- Campaign-type-level baselines ---
    for cg in TOP_CAMPAIGN_TYPES:
        if cg not in features_ct["channel_grouping"].values:
            skipped.append({"grain": cg, "level": "campaign_type", "reason": "not_in_dataset"})
            continue
        res = run_baseline_for_series(features_ct, "channel_grouping", cg)
        if res["status"] == "ok":
            all_results.append({"level": "campaign_type", **res})
        elif res["status"] == "skipped":
            skipped.append({"grain": cg, "level": "campaign_type", "reason": res["reason"]})
        else:
            failed.append({"grain": cg, "level": "campaign_type", "reason": res["reason"]})

    # --- Build output tables ---
    forecast_rows = []
    metric_rows = []
    for r in all_results:
        grain = r["grain"]
        level = r["level"]
        for h in FORECAST_HORIZONS:
            forecast_rows.append({
                "level": level,
                "grain": grain,
                "horizon_days": h,
                "model": "Holt-Winters",
                "forecast_total_revenue": r["hw_forecasts"][h],
                "seasonal_naive_total_revenue": r["sn_forecasts"][h],
                "actual_holdout_total_revenue": r[f"actual_last_{h}"],
            })
        metric_rows.append({"level": level, **r["metrics"]})

    forecasts_df = pd.DataFrame(forecast_rows)
    metrics_df = pd.DataFrame(metric_rows)

    if not forecasts_df.empty:
        forecasts_df.to_csv(outdir / "baseline_forecasts.csv", index=False)
    if not metrics_df.empty:
        metrics_df.to_csv(outdir / "validation_metrics.csv", index=False)

    # --- Plots ---
    for r in all_results:
        label = f"{r['level']}_{r['grain']}".replace("/", "-")
        plot_holdout_overlay(r, label, plots_dir / f"holdout_{label}.png")

    # --- Sanity-check report ---
    lines = [
        "STAGE 3 BASELINE DETERMINISTIC MODELS — SANITY CHECK REPORT",
        "=" * 65,
        "",
        f"Holdout period: last {HOLDOUT_DAYS} days of each series",
        f"Forecast horizons: {FORECAST_HORIZONS} days",
        f"Minimum non-zero days required: {MIN_NONZERO_DAYS}",
        f"Minimum total history required: {MIN_TOTAL_DAYS}",
        "",
        f"Series successfully modeled: {len(all_results)}",
        f"Skipped (too sparse / short): {len(skipped)}",
        f"Failed to fit: {len(failed)}",
        "",
        "SKIPPED SERIES",
        "-" * 30,
    ]
    for s in skipped:
        lines.append(f"  [{s['level']}] {s['grain']}: {s['reason']}")

    if failed:
        lines.append("")
        lines.append("FAILED SERIES")
        lines.append("-" * 30)
        for f in failed:
            lines.append(f"  [{f['level']}] {f['grain']}: {f['reason']}")

    if not metrics_df.empty:
        lines.append("")
        lines.append("VALIDATION METRICS (90-day holdout)")
        lines.append("-" * 40)
        for _, row in metrics_df.iterrows():
            lines.append(
                f"  [{row['level']}] {row['grain']}: "
                f"HW MAE={row['hw_mae']}, RMSE={row['hw_rmse']}, MAPE={row['hw_mape']}% | "
                f"SN MAE={row['sn_mae']}, RMSE={row['sn_rmse']}, MAPE={row['sn_mape']}%"
            )

        lines.append("")
        lines.append("SANITY CHECKS")
        lines.append("-" * 30)
        # Check 1: Are test means within ~2x of train means? (massive drift = data issue)
        for _, row in metrics_df.iterrows():
            ratio = row["test_mean"] / row["train_mean"] if row["train_mean"] > 0 else np.nan
            if not np.isnan(ratio) and (ratio > 3.0 or ratio < 0.33):
                lines.append(f"  [WARN] {row['grain']}: test mean is {ratio:.2f}x train mean (drift?)")
            else:
                lines.append(f"  [PASS] {row['grain']}: test/train mean ratio = {ratio:.2f}x")

        # Check 2: Does HW beat or near seasonal naive? (if it's much worse, something is wrong)
        for _, row in metrics_df.iterrows():
            if row["hw_mae"] <= row["sn_mae"] * 1.5:
                lines.append(f"  [PASS] {row['grain']}: HW MAE ({row['hw_mae']}) <= 1.5x SN MAE ({row['sn_mae']})")
            else:
                lines.append(f"  [WARN] {row['grain']}: HW MAE ({row['hw_mae']}) >> SN MAE ({row['sn_mae']}) — model may be overfitting or misspecified")

    report_path = outdir / "sanity_check_report.txt"
    report_path.write_text("\n".join(lines))

    print(f"Baseline forecasts: {outdir / 'baseline_forecasts.csv'} ({len(forecasts_df)} rows)")
    print(f"Validation metrics: {outdir / 'validation_metrics.csv'} ({len(metrics_df)} rows)")
    print(f"Diagnostic plots: {plots_dir}/ ({len(list(plots_dir.glob('*.png')))} PNGs)")
    print(f"Sanity report: {report_path}")
    print(f"OK={len(all_results)}, Skipped={len(skipped)}, Failed={len(failed)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--features-channel", default="features_by_channel.csv")
    parser.add_argument("--features-campaign-type", default="features_by_campaign_type.csv")
    parser.add_argument("--outdir", default="./output")
    args = parser.parse_args()
    run(args.features_channel, args.features_campaign_type, args.outdir)
