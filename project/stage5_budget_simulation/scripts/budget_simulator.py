"""
Stage 5: Budget Simulation / Response-Curve Engine
====================================================

PURPOSE
-------
Fit saturation-style response curves per grain and build a budget simulator
that takes hypothetical future spend per channel and outputs a forecasted
revenue / ROAS range.

SATURATION CURVES FITTED
------------------------
  1. Log-saturation:      revenue = a * ln(1 + b * spend)
  2. Power-law (diminishing):  revenue = a * spend^b   (b < 1)
  Both are fitted on historical daily (spend, revenue) pairs per grain.

BUDGET SIMULATION
-----------------
  The simulator uses the Stage 4 quantile models, but overrides the
  planned-spend feature (target_spend_H) with the user's hypothetical budget.
  Forecast origin = the last training date (2026-01-31), so the model
  conditions on the most recent historical state (lags, rolling averages,
  calendar position) and the new budget level.

  Budget levels tested: 50%, 75%, 100%, 125%, 150%, 200% of historical
  mean daily spend per grain.  These are cumulative over the horizon.

OUTPUTS
-------
  outputs/response_curve_params.csv    - fitted parameters per grain
  outputs/budget_simulation.csv       - p10/p50/p90 revenue and ROAS for
                                         every grain x horizon x budget level
  outputs/diagnostic_plots/*.png      - response curves + simulation overlay

USAGE
-----
    python budget_simulator.py \
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
from scipy.optimize import curve_fit
from sklearn.ensemble import HistGradientBoostingRegressor

warnings.filterwarnings("ignore")
pd.options.mode.chained_assignment = None

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------

HORIZONS = [30, 60, 90]
QUANTILES = [0.10, 0.50, 0.90]
TRAIN_CUTOFF = "2026-02-01"
FORECAST_ORIGIN = "2026-01-31"

BUDGET_MULTIPLIERS = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0]

PLATFORMS = ["Bing Ads", "Google Ads", "Meta Ads", "Organic/Direct"]
TOP_CAMPAIGN_TYPES = [
    "Search", "Pmax", "Direct", "Organic_Search", "Email",
    "Shopping", "Organic_Search_Bing", "Remarketing_DPA",
    "Organic_Social", "Remarketing_Brand",
]


# ---------------------------------------------------------------------------
# SATURATION CURVES
# ---------------------------------------------------------------------------

def log_saturation(spend, a, b):
    """Log-saturation: revenue = a * ln(1 + b * spend)."""
    return a * np.log1p(b * spend)


def power_law(spend, a, b):
    """Power-law with diminishing returns: revenue = a * spend^b."""
    return a * np.power(spend, b)


def hill_function(spend, Vmax, K, n):
    """Hill saturation: revenue = Vmax * spend^n / (K^n + spend^n)."""
    return Vmax * np.power(spend, n) / (np.power(K, n) + np.power(spend, n))


def fit_curves(df, grain_col, grain_value):
    """Fit saturation curves for one grain.  Returns dict of params."""
    sub = df[df[grain_col] == grain_value].copy()
    sub = sub[(sub["spend"] > 0) & (sub["revenue"] >= 0)]
    if len(sub) < 10:
        return None

    x = sub["spend"].values
    y = sub["revenue"].values

    results = {}

    # --- Log saturation ---
    try:
        popt, _ = curve_fit(log_saturation, x, y, p0=[y.max(), 1.0], maxfev=5000)
        results["log_a"] = popt[0]
        results["log_b"] = popt[1]
        pred = log_saturation(x, *popt)
        results["log_r2"] = 1 - np.sum((y - pred) ** 2) / np.sum((y - y.mean()) ** 2)
    except Exception:
        results["log_a"] = np.nan
        results["log_b"] = np.nan
        results["log_r2"] = np.nan

    # --- Power law ---
    try:
        popt, _ = curve_fit(power_law, x, y, p0=[y.max() / x.max(), 0.8], maxfev=5000)
        results["power_a"] = popt[0]
        results["power_b"] = popt[1]
        pred = power_law(x, *popt)
        results["power_r2"] = 1 - np.sum((y - pred) ** 2) / np.sum((y - y.mean()) ** 2)
    except Exception:
        results["power_a"] = np.nan
        results["power_b"] = np.nan
        results["power_r2"] = np.nan

    # --- Hill function ---
    try:
        popt, _ = curve_fit(
            hill_function, x, y,
            p0=[y.max(), x.mean(), 1.0],
            bounds=([0, 0, 0.1], [np.inf, np.inf, 5.0]),
            maxfev=5000
        )
        results["hill_Vmax"] = popt[0]
        results["hill_K"] = popt[1]
        results["hill_n"] = popt[2]
        pred = hill_function(x, *popt)
        results["hill_r2"] = 1 - np.sum((y - pred) ** 2) / np.sum((y - y.mean()) ** 2)
    except Exception:
        results["hill_Vmax"] = np.nan
        results["hill_K"] = np.nan
        results["hill_n"] = np.nan
        results["hill_r2"] = np.nan

    return results


# ---------------------------------------------------------------------------
# FEATURE ENGINEERING (reused from Stage 4)
# ---------------------------------------------------------------------------

def engineer_features(df):
    df = df.copy()
    df["days_since_start"] = (df["date"] - df["date"].min()).dt.days
    df["month_sin"] = np.sin(2 * np.pi * df["date"].dt.month / 12)
    df["month_cos"] = np.cos(2 * np.pi * df["date"].dt.month / 12)
    df["dayofmonth_sin"] = np.sin(2 * np.pi * df["date"].dt.day / 31)
    df["dayofmonth_cos"] = np.cos(2 * np.pi * df["date"].dt.day / 31)
    return df


def create_horizon_targets(df):
    df = df.sort_values("date").reset_index(drop=True)
    for H in HORIZONS:
        df[f"target_revenue_{H}d"] = (
            df["revenue"].shift(-1).rolling(H, min_periods=H).sum().shift(H - 1)
        )
        df[f"target_spend_{H}d"] = (
            df["spend"].shift(-1).rolling(H, min_periods=H).sum().shift(H - 1)
        )
    return df


def build_feature_matrix(df, horizon):
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
    day_dummies = pd.get_dummies(df["day_of_week"], prefix="dow", drop_first=True)
    X = pd.concat([df[base_cols], day_dummies], axis=1)
    valid = X.notna().all(axis=1)
    return X, base_cols + list(day_dummies.columns), valid


# ---------------------------------------------------------------------------
# MODEL TRAINING (Stage 4 re-train, kept lightweight)
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# BUDGET SIMULATION
# ---------------------------------------------------------------------------

def simulate_budget(features_path, grain_col, grains, outdir, label):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    plots_dir = outdir / "diagnostic_plots"
    plots_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(features_path, parse_dates=["date"])
    df = engineer_features(df)

    curve_params = []
    sim_rows = []

    for grain in grains:
        sub = df[df[grain_col] == grain].copy()
        if len(sub) < 200:
            continue

        # --- Fit saturation curves on daily spend-revenue ---
        curves = fit_curves(sub, grain_col, grain)
        if curves is not None:
            curve_params.append({"grain": grain, "level": label, **curves})

        # --- Prepare for model training ---
        sub = create_horizon_targets(sub)

        # Historical mean daily spend (for scaling budget levels)
        hist_mean_daily_spend = sub["spend"].mean()
        hist_mean_daily_revenue = sub["revenue"].mean()

        for H in HORIZONS:
            X, feature_names, valid = build_feature_matrix(sub, H)
            target_col = f"target_revenue_{H}d"
            usable = valid & sub[target_col].notna()
            train_mask = (sub["date"] < pd.Timestamp(TRAIN_CUTOFF)) & usable

            X_train = X[train_mask].values
            y_train = sub.loc[train_mask, target_col].values

            if len(X_train) < 50:
                continue

            # Train quantile models
            models = {}
            for q in QUANTILES:
                models[q] = train_quantile_model(X_train, y_train, q)

            # Find the forecast origin row
            origin_mask = sub["date"] == pd.Timestamp(FORECAST_ORIGIN)
            if not origin_mask.any():
                # Fallback: last training date
                origin_mask = sub["date"] == sub[sub["date"] < pd.Timestamp(TRAIN_CUTOFF)]["date"].max()
            if not origin_mask.any():
                continue

            origin_idx = sub[origin_mask].index[0]
            origin_row = X.loc[origin_idx].values.reshape(1, -1)
            spend_col_idx = feature_names.index(f"target_spend_{H}d") if f"target_spend_{H}d" in feature_names else None

            # --- Simulate across budget levels ---
            for mult in BUDGET_MULTIPLIERS:
                hypothetical_daily_spend = hist_mean_daily_spend * mult
                hypothetical_cumulative_spend = hypothetical_daily_spend * H

                # Override the spend feature in the origin row
                sim_row = origin_row.copy()
                if spend_col_idx is not None:
                    sim_row[0, spend_col_idx] = hypothetical_cumulative_spend

                # Predict
                preds = {q: max(models[q].predict(sim_row)[0], 0) for q in QUANTILES}

                # Saturation curve estimate (daily revenue * H)
                if curves and not pd.isna(curves.get("log_a")):
                    log_est = log_saturation(hypothetical_daily_spend, curves["log_a"], curves["log_b"]) * H
                else:
                    log_est = np.nan

                if curves and not pd.isna(curves.get("power_a")):
                    power_est = power_law(hypothetical_daily_spend, curves["power_a"], curves["power_b"]) * H
                else:
                    power_est = np.nan

                roas = {q: (preds[q] / hypothetical_cumulative_spend) if hypothetical_cumulative_spend > 0 else np.nan for q in QUANTILES}

                sim_rows.append({
                    "grain": grain,
                    "level": label,
                    "horizon_days": H,
                    "budget_multiplier": mult,
                    "historical_mean_daily_spend": round(hist_mean_daily_spend, 2),
                    "hypothetical_daily_spend": round(hypothetical_daily_spend, 2),
                    "hypothetical_cumulative_spend": round(hypothetical_cumulative_spend, 2),
                    "p10_revenue": round(preds[0.10], 2),
                    "p50_revenue": round(preds[0.50], 2),
                    "p90_revenue": round(preds[0.90], 2),
                    "p10_roas": round(roas[0.10], 2) if not pd.isna(roas[0.10]) else None,
                    "p50_roas": round(roas[0.50], 2) if not pd.isna(roas[0.50]) else None,
                    "p90_roas": round(roas[0.90], 2) if not pd.isna(roas[0.90]) else None,
                    "log_saturation_revenue_est": round(log_est, 2) if not pd.isna(log_est) else None,
                    "power_law_revenue_est": round(power_est, 2) if not pd.isna(power_est) else None,
                })

    # --- Response curve plots ---
    if curve_params:
        curves_df = pd.DataFrame(curve_params)
        curves_df.to_csv(outdir / "response_curve_params.csv", index=False)

        for _, row in curves_df.iterrows():
            grain = row["grain"]
            sub = df[df[grain_col] == grain]
            plot_data = sub[(sub["spend"] > 0) & (sub["revenue"] >= 0)]
            if len(plot_data) < 10:
                continue

            x = plot_data["spend"].values
            y = plot_data["revenue"].values

            # Spend grid for smooth curves
            spend_grid = np.linspace(0, x.max() * 1.2, 200)

            fig, ax = plt.subplots(figsize=(8, 5))
            ax.scatter(x, y, alpha=0.3, s=10, color="gray", label="Historical daily observations")

            if not pd.isna(row.get("log_a")):
                ax.plot(spend_grid, log_saturation(spend_grid, row["log_a"], row["log_b"]),
                        color="tab:blue", linewidth=2, label=f"Log-saturation (R²={row['log_r2']:.2f})")
            if not pd.isna(row.get("power_a")):
                ax.plot(spend_grid, power_law(spend_grid, row["power_a"], row["power_b"]),
                        color="tab:orange", linewidth=2, linestyle="--", label=f"Power law (R²={row['power_r2']:.2f})")
            if not pd.isna(row.get("hill_Vmax")):
                ax.plot(spend_grid, hill_function(spend_grid, row["hill_Vmax"], row["hill_K"], row["hill_n"]),
                        color="tab:green", linewidth=2, linestyle=":", label=f"Hill (R²={row['hill_r2']:.2f})")

            ax.set_title(f"{label} {grain} — Response curve")
            ax.set_xlabel("Daily spend")
            ax.set_ylabel("Daily revenue")
            ax.legend()
            fig.tight_layout()
            safe_grain = grain.replace("/", "-")
            fig.savefig(plots_dir / f"response_curve_{label}_{safe_grain}.png", dpi=110)
            plt.close(fig)

    # --- Save simulation ---
    sim_df = pd.DataFrame(sim_rows)
    if not sim_df.empty:
        sim_df.to_csv(outdir / "budget_simulation.csv", index=False)

    print(f"  [{label}] curves={len(curve_params)} grains, simulations={len(sim_df)} rows, "
          f"plots={len(list(plots_dir.glob('*.png')))} PNGs")
    return sim_df, pd.DataFrame(curve_params) if curve_params else pd.DataFrame()


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def run(features_channel_path, features_campaign_type_path, outdir):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    print("Stage 5 – Budget Simulation / Response-Curve Engine")
    print("=" * 55)

    s1, c1 = simulate_budget(features_channel_path, "platform", PLATFORMS,
                             outdir / "platform", "platform")
    s2, c2 = simulate_budget(features_campaign_type_path, "channel_grouping",
                             TOP_CAMPAIGN_TYPES, outdir / "campaign_type", "campaign_type")

    for name, frames in [
        ("budget_simulation.csv", [s1, s2]),
        ("response_curve_params.csv", [c1, c2]),
    ]:
        combined = pd.concat(frames, ignore_index=True)
        if not combined.empty:
            combined.to_csv(outdir / name, index=False)
            print(f"  Combined -> {outdir / name} ({len(combined)} rows)")

    print("\nStage 5 complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--features-channel", default="features_by_channel.csv")
    parser.add_argument("--features-campaign-type", default="features_by_campaign_type.csv")
    parser.add_argument("--outdir", default="./output")
    args = parser.parse_args()
    run(args.features_channel, args.features_campaign_type, args.outdir)
