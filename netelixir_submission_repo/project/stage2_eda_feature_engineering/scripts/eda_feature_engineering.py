"""
Stage 2: EDA and Feature Engineering
======================================

PURPOSE
-------
Builds on the stage-1 outputs (unified_campaign_data.csv + synthetic_shopify_orders.csv)
to: (1) decompose each channel's daily series into trend/seasonality/residual,
(2) compute historical ROAS distributions per channel and per campaign type,
(3) engineer lagged-spend / rolling-average / day-of-week / spend-share features,
and (4) cross-check any detected seasonality against the actual India/US retail
calendar rather than assuming festive effects exist.

DEFINITIONS USED HERE (see prior discussion in this project)
---------------------------------------------------------------
  channel       = platform: Bing Ads, Google Ads, Meta Ads, Organic/Direct
  campaign type = channel_grouping: Search, Pmax, Shopping, Display, Video,
                  Demand Gen, Generic, Prospecting_*, Remarketing_*, plus the
                  unpaid groupings (Direct, Organic_Search, Email, etc.)

WHAT'S REAL VS SYNTHETIC IN THIS ANALYSIS
-------------------------------------------
Ad spend and clicks are real (the original Bing/Google/Meta exports). Sessions
and orders are synthetic, generated proportional to real clicks with random
per-channel conversion rates -- they carry NO independent seasonality of their
own. That means: spend-series decomposition and the calendar cross-check below
are analyzing genuine patterns. Revenue-series decomposition will mostly mirror
whatever pattern already exists in spend, because that's how the synthetic
revenue was built, not because of a separately-modeled demand seasonality. This
is called out again in the calendar-check report so it isn't mistaken for an
independent revenue-seasonality finding.

OUTPUTS (all under --outdir)
-----------------------------
  decomposition_components.csv     - date, platform, series_type, observed/trend/seasonal/resid
  roas_distribution_by_channel.csv - ROAS summary stats per platform (weekly grain)
  roas_distribution_by_campaign_type.csv - same, per channel_grouping
  features_by_channel.csv          - engineered features at (date, platform) grain
  features_by_campaign_type.csv    - engineered features at (date, channel_grouping) grain
  seasonality_calendar_analysis.txt- narrative: which spend spikes line up with
                                      known India/US retail-calendar dates vs.
                                      generic weekly cyclicality
  plots/*.png                      - decomposition, ROAS, and calendar-overlay diagnostics

USAGE
-----
    python eda_feature_engineering.py \
        --unified unified_campaign_data.csv \
        --shopify synthetic_shopify_orders.csv \
        --outdir ./output
"""

import argparse
import calendar as cal
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose, STL

pd.options.mode.chained_assignment = None

# ---------------------------------------------------------------------------
# 1. RETAIL CALENDAR  (real dates, looked up for the data's actual date range)
# ---------------------------------------------------------------------------

def _nth_weekday(year: int, month: int, weekday: int, n: int) -> pd.Timestamp:
    """n-th occurrence (1-indexed) of `weekday` (Mon=0) in a given month/year."""
    c = cal.Calendar()
    days = [d for d in c.itermonthdates(year, month) if d.month == month and d.weekday() == weekday]
    return pd.Timestamp(days[n - 1])


def _last_weekday(year: int, month: int, weekday: int) -> pd.Timestamp:
    c = cal.Calendar()
    days = [d for d in c.itermonthdates(year, month) if d.month == month and d.weekday() == weekday]
    return pd.Timestamp(days[-1])


def build_retail_calendar(years: list) -> pd.DataFrame:
    """India + US retail-calendar dates. Fixed-date and rule-based holidays are
    computed; lunar/lunisolar festival dates (Diwali, Holi) are hardcoded from
    sourced lookups since they can't be derived from a simple rule."""
    DIWALI = {2024: "2024-11-01", 2025: "2025-10-20", 2026: "2026-11-08"}
    HOLI = {2024: "2024-03-25", 2025: "2025-03-14", 2026: "2026-03-04"}
    DUSSEHRA = {2024: "2024-10-12", 2025: "2025-10-02", 2026: "2026-10-21"}  # ~20 days before Diwali

    events = []
    for y in years:
        events += [
            ("India", "Republic Day", pd.Timestamp(f"{y}-01-26")),
            ("India", "Holi", pd.Timestamp(HOLI.get(y, f"{y}-03-15"))),
            ("India", "Independence Day", pd.Timestamp(f"{y}-08-15")),
            ("India", "Dussehra/Navratri end", pd.Timestamp(DUSSEHRA.get(y, f"{y}-10-10"))),
            ("India", "Diwali", pd.Timestamp(DIWALI.get(y, f"{y}-11-01"))),
            ("India", "Republic-style Big Billion Days/Great Indian Festival window",
             pd.Timestamp(DUSSEHRA.get(y, f"{y}-10-10")) - pd.Timedelta(days=10)),
            ("India", "Fiscal year-end push (Mar 31)", pd.Timestamp(f"{y}-03-31")),
            ("US", "New Year's Day", pd.Timestamp(f"{y}-01-01")),
            ("US", "Memorial Day", _last_weekday(y, 5, 0)),
            ("US", "Independence Day (US)", pd.Timestamp(f"{y}-07-04")),
            ("US", "Labor Day", _nth_weekday(y, 9, 0, 1)),
            ("US/Global", "Black Friday", _nth_weekday(y, 11, 3, 4) + pd.Timedelta(days=1)),
            ("US/Global", "Cyber Monday", _nth_weekday(y, 11, 3, 4) + pd.Timedelta(days=4)),
            ("US/Global", "Christmas", pd.Timestamp(f"{y}-12-25")),
            ("Generic", "End of Q1", pd.Timestamp(f"{y}-03-31")),
            ("Generic", "End of Q2", pd.Timestamp(f"{y}-06-30")),
            ("Generic", "End of Q3", pd.Timestamp(f"{y}-09-30")),
            ("Generic", "End of Q4 / Year-end push", pd.Timestamp(f"{y}-12-31")),
        ]
    return pd.DataFrame(events, columns=["region", "event", "date"]).sort_values("date").reset_index(drop=True)


# ---------------------------------------------------------------------------
# 2. LOAD + BUILD DAILY SERIES
# ---------------------------------------------------------------------------

def load_inputs(unified_path: str, shopify_path: str):
    ad = pd.read_csv(unified_path, parse_dates=["date"])
    orders = pd.read_csv(shopify_path, parse_dates=["order_date"])
    return ad, orders


def build_daily_series(ad: pd.DataFrame, orders: pd.DataFrame, grain_col: str) -> pd.DataFrame:
    """Full daily spend+revenue series for every value of grain_col
    ('platform' or 'channel_grouping'), reindexed across the complete date
    range with zero-fill for days a given series had no activity."""
    spend = ad.groupby(["date", grain_col])["spend"].sum().reset_index()
    revenue = orders.groupby(["order_date", grain_col])["revenue"].sum().reset_index() \
        .rename(columns={"order_date": "date"})

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
# 3. DECOMPOSITION
# ---------------------------------------------------------------------------

MIN_DAYS_FOR_DECOMPOSITION = 60  # need a handful of full weekly cycles

def decompose_series(daily: pd.DataFrame, grain_col: str, grain_value: str, value_col: str, period: int = 7):
    """Run both classical seasonal_decompose and STL on one (grain, value_col)
    series. Returns a long dataframe of components, or None if the series is
    too short/sparse to decompose meaningfully."""
    sub = daily[daily[grain_col] == grain_value].set_index("date")[value_col].asfreq("D").fillna(0.0)
    if len(sub) < MIN_DAYS_FOR_DECOMPOSITION or sub.sum() == 0:
        return None

    classical = seasonal_decompose(sub, model="additive", period=period, extrapolate_trend="freq")
    stl_res = STL(sub, period=period, robust=True).fit()

    out = pd.DataFrame({
        "date": sub.index,
        grain_col: grain_value,
        "series_type": value_col,
        "observed": sub.values,
        "trend_classical": classical.trend.values,
        "seasonal_classical": classical.seasonal.values,
        "resid_classical": classical.resid.values,
        "trend_stl": stl_res.trend,
        "seasonal_stl": stl_res.seasonal,
        "resid_stl": stl_res.resid,
    })
    return out


def plot_decomposition(components: pd.DataFrame, grain_value: str, value_col: str, outpath: Path):
    fig, axes = plt.subplots(4, 1, figsize=(11, 8), sharex=True)
    axes[0].plot(components["date"], components["observed"], color="#1f77b4")
    axes[0].set_title(f"{grain_value} -- {value_col} (observed)")
    axes[1].plot(components["date"], components["trend_stl"], color="#ff7f0e")
    axes[1].set_title("Trend (STL)")
    axes[2].plot(components["date"], components["seasonal_stl"], color="#2ca02c")
    axes[2].set_title("Weekly seasonal component (STL, period=7)")
    axes[3].plot(components["date"], components["resid_stl"], color="#d62728")
    axes[3].axhline(0, color="black", linewidth=0.5)
    axes[3].set_title("Residual (STL) -- spikes here are what the calendar check looks at")
    fig.tight_layout()
    fig.savefig(outpath, dpi=110)
    plt.close(fig)


# ---------------------------------------------------------------------------
# 4. ROAS DISTRIBUTIONS  (weekly grain -- daily ROAS is too noisy at low spend)
# ---------------------------------------------------------------------------

def compute_roas_distribution(daily: pd.DataFrame, grain_col: str) -> pd.DataFrame:
    weekly = daily.copy()
    weekly["week"] = weekly["date"].dt.to_period("W").astype(str)
    weekly = weekly.groupby([grain_col, "week"]).agg(spend=("spend", "sum"), revenue=("revenue", "sum")).reset_index()
    weekly = weekly[weekly["spend"] > 0]
    weekly["roas"] = weekly["revenue"] / weekly["spend"]

    summary = weekly.groupby(grain_col)["roas"].agg(
        n_weeks="count", mean="mean", median="median", std="std",
        p10=lambda s: s.quantile(0.10), p90=lambda s: s.quantile(0.90),
        min="min", max="max",
    ).reset_index().sort_values("mean", ascending=False)
    return summary, weekly


def plot_roas_distribution(weekly: pd.DataFrame, grain_col: str, outpath: Path, top_n: int = 8):
    top_groups = weekly.groupby(grain_col)["roas"].count().sort_values(ascending=False).head(top_n).index
    sub = weekly[weekly[grain_col].isin(top_groups)]
    fig, ax = plt.subplots(figsize=(10, 6))
    order = sub.groupby(grain_col)["roas"].median().sort_values(ascending=False).index
    data = [sub[sub[grain_col] == g]["roas"].values for g in order]
    ax.boxplot(data, tick_labels=list(order), vert=True, showfliers=False)
    ax.set_ylabel("Weekly ROAS (revenue / spend)")
    ax.set_title(f"Weekly ROAS distribution by {grain_col} (top {top_n} by data volume)")
    plt.xticks(rotation=45, ha="right")
    fig.tight_layout()
    fig.savefig(outpath, dpi=110)
    plt.close(fig)


# ---------------------------------------------------------------------------
# 5. FEATURE ENGINEERING
# ---------------------------------------------------------------------------

def engineer_features(daily: pd.DataFrame, grain_col: str) -> pd.DataFrame:
    df = daily.sort_values([grain_col, "date"]).copy()

    # Spend-share-of-total: each grain value's share of that day's total spend
    # across every value of the same grain (e.g. each platform's share of
    # total daily ad spend across all platforms).
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
# 6. CALENDAR CROSS-CHECK
# ---------------------------------------------------------------------------

def find_spend_spikes(components: pd.DataFrame, z_thresh: float = 2.0) -> pd.DataFrame:
    """Flag days where STL residual (spend series) is an outlier relative to
    its own distribution -- i.e. spend that the trend + weekly-seasonal model
    can't explain. These are the candidate 'irregular event' days."""
    resid = components["resid_stl"]
    z = (resid - resid.mean()) / resid.std(ddof=0)
    spikes = components[z.abs() > z_thresh].copy()
    spikes["z_score"] = z[z.abs() > z_thresh]
    return spikes.sort_values("z_score", ascending=False)


def match_spikes_to_calendar(spikes: pd.DataFrame, retail_calendar: pd.DataFrame, window_days: int = 3) -> pd.DataFrame:
    matches = []
    for _, row in spikes.iterrows():
        nearby = retail_calendar[(retail_calendar["date"] - row["date"]).abs() <= pd.Timedelta(days=window_days)]
        matches.append({
            "date": row["date"],
            "platform": row.get("platform"),
            "z_score": round(row["z_score"], 2),
            "matched_event": "; ".join(nearby["event"].tolist()) if not nearby.empty else "(no calendar match -- likely generic spend pulse)",
        })
    return pd.DataFrame(matches)


def write_calendar_report(all_matches: dict, weekly_seasonality_notes: list, outpath: Path):
    lines = [
        "SEASONALITY / RETAIL-CALENDAR CROSS-CHECK",
        "=" * 45,
        "",
        "METHODOLOGY: spend (not revenue) is decomposed first because spend is",
        "real data; revenue is synthetic and was generated proportional to real",
        "clicks, so it inherits spend's patterns rather than carrying an",
        "independently-modeled seasonality of its own. Spikes are detected from",
        "the STL residual (what trend + weekly seasonality can't explain), then",
        "checked against actual India/US retail-calendar dates -- this is",
        "detect-first, explain-after, not an assumed-calendar overlay.",
        "",
        "WEEKLY (GENERIC) SEASONALITY",
        "-" * 30,
    ]
    lines += weekly_seasonality_notes
    lines.append("")
    lines.append("IRREGULAR SPIKES vs. RETAIL CALENDAR")
    lines.append("-" * 38)
    for platform, df in all_matches.items():
        lines.append(f"\n[{platform}] spend spikes (|z| > 2.0 on STL residual):")
        if df.empty:
            lines.append("    none detected at this threshold.")
        for _, r in df.head(10).iterrows():
            lines.append(f"    {r['date'].date()} (z={r['z_score']}): {r['matched_event']}")
    path = outpath
    path.write_text("\n".join(lines))


# ---------------------------------------------------------------------------
# 7. MAIN
# ---------------------------------------------------------------------------

def run(unified_path, shopify_path, outdir):
    outdir = Path(outdir)
    plots_dir = outdir / "plots"
    plots_dir.mkdir(parents=True, exist_ok=True)

    ad, orders = load_inputs(unified_path, shopify_path)
    daily_by_platform = build_daily_series(ad, orders, "platform")
    daily_by_campaign_type = build_daily_series(ad, orders, "channel_grouping")

    years = list(range(daily_by_platform["date"].dt.year.min(), daily_by_platform["date"].dt.year.max() + 1))
    retail_calendar = build_retail_calendar(years)

    # --- Decomposition (per platform, both spend and revenue) ---
    all_components = []
    spike_matches = {}
    weekly_notes = []
    for platform in sorted(daily_by_platform["platform"].unique()):
        for value_col in ("spend", "revenue"):
            comp = decompose_series(daily_by_platform, "platform", platform, value_col)
            if comp is None:
                continue
            all_components.append(comp)
            plot_decomposition(comp, platform, value_col, plots_dir / f"decomposition_{platform.replace('/', '-')}_{value_col}.png")

            if value_col == "spend":
                seasonal_amp = comp["seasonal_stl"].abs().mean()
                observed_mean = comp["observed"].mean()
                pct = 100 * seasonal_amp / observed_mean if observed_mean else 0
                weekly_notes.append(
                    f"  {platform}: average weekly-seasonal swing is ~{pct:.1f}% of mean daily spend "
                    f"(STL period=7) -- {'a meaningfully repeating weekly pattern' if pct > 5 else 'a weak/negligible weekly pattern'}."
                )
                spikes = find_spend_spikes(comp)
                spike_matches[platform] = match_spikes_to_calendar(spikes, retail_calendar)

    components_df = pd.concat(all_components, ignore_index=True) if all_components else pd.DataFrame()
    if not components_df.empty:
        components_df.to_csv(outdir / "decomposition_components.csv", index=False)

    write_calendar_report(spike_matches, weekly_notes, outdir / "seasonality_calendar_analysis.txt")

    # --- ROAS distributions ---
    channel_roas_summary, channel_roas_weekly = compute_roas_distribution(daily_by_platform, "platform")
    campaign_roas_summary, campaign_roas_weekly = compute_roas_distribution(daily_by_campaign_type, "channel_grouping")
    channel_roas_summary.to_csv(outdir / "roas_distribution_by_channel.csv", index=False)
    campaign_roas_summary.to_csv(outdir / "roas_distribution_by_campaign_type.csv", index=False)
    plot_roas_distribution(channel_roas_weekly, "platform", plots_dir / "roas_boxplot_by_channel.png")
    plot_roas_distribution(campaign_roas_weekly, "channel_grouping", plots_dir / "roas_boxplot_by_campaign_type.png")

    # --- Feature engineering ---
    features_by_channel = engineer_features(daily_by_platform, "platform")
    features_by_campaign_type = engineer_features(daily_by_campaign_type, "channel_grouping")
    features_by_channel.to_csv(outdir / "features_by_channel.csv", index=False)
    features_by_campaign_type.to_csv(outdir / "features_by_campaign_type.csv", index=False)

    print(f"Decomposition components: {outdir / 'decomposition_components.csv'} ({len(components_df)} rows)")
    print(f"ROAS by channel: {outdir / 'roas_distribution_by_channel.csv'} ({len(channel_roas_summary)} channels)")
    print(f"ROAS by campaign type: {outdir / 'roas_distribution_by_campaign_type.csv'} ({len(campaign_roas_summary)} types)")
    print(f"Features by channel: {outdir / 'features_by_channel.csv'} ({len(features_by_channel)} rows)")
    print(f"Features by campaign type: {outdir / 'features_by_campaign_type.csv'} ({len(features_by_campaign_type)} rows)")
    print(f"Calendar cross-check: {outdir / 'seasonality_calendar_analysis.txt'}")
    print(f"Plots: {plots_dir}/ ({len(list(plots_dir.glob('*.png')))} PNG files)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--unified", default="unified_campaign_data.csv")
    parser.add_argument("--shopify", default="synthetic_shopify_orders.csv")
    parser.add_argument("--outdir", default="./output")
    args = parser.parse_args()
    run(args.unified, args.shopify, args.outdir)
