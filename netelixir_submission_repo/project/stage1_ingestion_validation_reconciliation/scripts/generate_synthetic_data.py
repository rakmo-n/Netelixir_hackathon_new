"""
Synthetic GA4 Sessions + Shopify Orders Generator
===================================================

WHY THIS EXISTS
----------------
No real GA4 property or Shopify store was available for this project (see
the data-sourcing conversation). Rather than chase mismatched public/sample
datasets that don't share dates or campaign names with the real Bing/Google/
Meta exports already collected, this script generates synthetic GA4 session
data and synthetic Shopify order data that ARE mathematically tied to the
real ad-platform data: same dates, same campaign names, same channel
groupings. That makes it possible to actually exercise the full ingestion ->
validation -> join -> reconciliation pipeline end to end.

THIS IS SIMULATED DATA. It is built from assumed session rates, conversion
rates, and order values per channel type -- not measured. Treat every number
downstream of this script as a stand-in for real data, not a real result.
Swap in actual GA4/Shopify exports the moment they're available; the join
keys and schema here are designed to match what those would look like.

MODELING APPROACH
------------------
For every (platform, campaign, date) row in the real ad data with clicks>0:
  - GA4 sessions = clicks * a channel-specific session rate (clicks don't
    perfectly equal sessions -- bounced clicks, ad blockers, multi-session
    users push this above or below 1.0 depending on channel intent).
  - Shopify orders = sessions * a channel-specific conversion rate, NOT the
    ad platform's own self-reported "conversions" field. This is
    deliberate: the three ad-platform exports use incompatible conversion
    definitions (Meta's "conversion" column is ~3x its own click count,
    which cannot be a literal order count), so building synthetic orders
    off clicks/sessions instead gives a coherent ground truth and lets the
    reconciliation step surface a believable ad-platform-vs-actual-orders
    gap, which mirrors the real-world discrepancy this kind of pipeline is
    built to catch.

On top of the paid-channel rows, a block of organic/direct/email/organic-
social baseline traffic is added per date, scaled relative to that date's
paid session volume, since no real ecommerce site's traffic or revenue is
100% ad-attributed.

OUTPUTS
-------
    synthetic_ga4_sessions.csv   - date, channel_grouping, platform,
                                    campaign_name, session_source_medium,
                                    sessions, avg_session_duration,
                                    engagement_rate, join_key
    synthetic_shopify_orders.csv - order_id, order_date, channel_grouping,
                                    platform, campaign_name, utm_source,
                                    utm_medium, revenue, join_key

join_key = "<date>|<channel_grouping>", matching the key already used in
ingest_validate_reconcile.py, so these drop straight into that pipeline.
"""

import argparse
import random
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 42

# ---------------------------------------------------------------------------
# Channel-level assumption tables. Ranges are deliberately wide -- this is
# meant to produce plausible, varied data, not a precise simulation.
# ---------------------------------------------------------------------------

SESSION_RATE_RANGES = {
    "Search": (0.90, 1.05),
    "Shopping": (0.85, 1.00),
    "Pmax": (0.80, 0.98),
    "Demand Gen": (0.75, 0.95),
    "Display": (0.55, 0.75),
    "Video": (0.45, 0.65),
    "_META_DEFAULT": (0.65, 0.85),
}

DURATION_RANGES = {  # seconds
    "Search": (60, 240),
    "Shopping": (50, 200),
    "Pmax": (40, 150),
    "Demand Gen": (30, 120),
    "Display": (10, 50),
    "Video": (15, 60),
    "_META_DEFAULT": (20, 90),
}

ENGAGEMENT_RANGES = {  # 0-1
    "Search": (0.45, 0.75),
    "Shopping": (0.40, 0.70),
    "Pmax": (0.35, 0.60),
    "Demand Gen": (0.30, 0.55),
    "Display": (0.10, 0.30),
    "Video": (0.15, 0.35),
    "_META_DEFAULT": (0.25, 0.50),
}

CONV_RATE_RANGES = {  # orders per session
    "Search": (0.015, 0.035),
    "Shopping": (0.015, 0.030),
    "Pmax": (0.006, 0.018),
    "Demand Gen": (0.005, 0.015),
    "Display": (0.001, 0.005),
    "Video": (0.001, 0.004),
    "_META_REMARKETING": (0.010, 0.025),  # warmer audience, converts better
    "_META_PROSPECTING": (0.003, 0.010),  # cold audience
}


def _meta_default_key(channel_grouping: str, table: str) -> tuple:
    if table == "conv":
        if channel_grouping.startswith("Remarketing"):
            return CONV_RATE_RANGES["_META_REMARKETING"]
        return CONV_RATE_RANGES["_META_PROSPECTING"]
    table_map = {"session": SESSION_RATE_RANGES, "duration": DURATION_RANGES, "engagement": ENGAGEMENT_RANGES}
    return table_map[table]["_META_DEFAULT"]


def get_range(channel_grouping: str, platform: str, table: str, rng_lookup: dict) -> tuple:
    if channel_grouping in rng_lookup:
        return rng_lookup[channel_grouping]
    if platform == "Meta Ads":
        return _meta_default_key(channel_grouping, table)
    # Fallback for any unmapped grouping -- use the widest, most conservative band
    return (0.5, 0.8) if table == "session" else (0.2, 0.4)


def get_source_medium(platform: str, channel_grouping: str) -> str:
    if platform == "Bing Ads":
        return "bing / cpc"
    if platform == "Google Ads":
        if channel_grouping == "Display":
            return "google / display"
        if channel_grouping == "Video":
            return "youtube / cpc"
        return "google / cpc"
    if platform == "Meta Ads":
        return "facebook / paid"
    return "(not set) / (not set)"


# Baseline (unpaid) traffic mix -- shares must sum to 1.0
BASELINE_CHANNELS = [
    {"channel_grouping": "Direct", "source_medium": "(direct) / (none)", "share": 0.35,
     "conv": (0.020, 0.050), "duration": (20, 90), "engagement": (0.30, 0.55)},
    {"channel_grouping": "Organic_Search", "source_medium": "google / organic", "share": 0.30,
     "conv": (0.015, 0.035), "duration": (60, 200), "engagement": (0.45, 0.70)},
    {"channel_grouping": "Email", "source_medium": " email", "share": 0.15,
     "conv": (0.030, 0.070), "duration": (30, 150), "engagement": (0.55, 0.85)},
    {"channel_grouping": "Organic_Social", "source_medium": "social / instagram", "share": 0.12,
     "conv": (0.005, 0.015), "duration": (10, 50), "engagement": (0.15, 0.35)},
    {"channel_grouping": "Organic_Search_Bing", "source_medium": "bing / organic", "share": 0.08,
     "conv": (0.010, 0.030), "duration": (40, 150), "engagement": (0.35, 0.60)},
]

ORDER_VALUE_LOGNORMAL_MEAN_LOG = np.log(55)  # centers order value around ~$55
ORDER_VALUE_LOGNORMAL_SIGMA = 0.45
ORDER_VALUE_CLIP = (12, 350)


# ---------------------------------------------------------------------------
# Generation
# ---------------------------------------------------------------------------

def build_unified_ad_data(bing_path: str, google_path: str, meta_path: str) -> pd.DataFrame:
    """Re-derive the same normalized/parsed ad dataset the main pipeline
    builds, so this generator only needs the three raw platform CSVs as
    input (kept self-contained rather than importing the other script)."""
    import re

    NAME_PATTERN = re.compile(r"^(?P<prefix>.+?)_Campaign_(?P<num>\d+)$")
    AUDIENCE_SUFFIX_PATTERN = re.compile(r"^(?P<base>.+)_(?P<tag>TM|NTM)$")

    def parse_name(name):
        m = NAME_PATTERN.match(name.strip())
        if not m:
            return None
        prefix = m.group("prefix")
        tag_match = AUDIENCE_SUFFIX_PATTERN.match(prefix)
        return tag_match.group("base") if tag_match else prefix

    bing = pd.read_csv(bing_path)
    bing_df = pd.DataFrame({
        "date": pd.to_datetime(bing["TimePeriod"]),
        "platform": "Bing Ads",
        "campaign_name": bing["CampaignName"].astype(str),
        "clicks": bing["Clicks"],
    })

    google = pd.read_csv(google_path)
    google_df = pd.DataFrame({
        "date": pd.to_datetime(google["segments_date"]),
        "platform": "Google Ads",
        "campaign_name": google["campaign_name"].astype(str),
        "clicks": google["metrics_clicks"],
    })

    meta = pd.read_csv(meta_path)
    meta_df = pd.DataFrame({
        "date": pd.to_datetime(meta["date_start"]),
        "platform": "Meta Ads",
        "campaign_name": meta["campaign_name"].astype(str),
        "clicks": meta["clicks"],
    })

    df = pd.concat([bing_df, google_df, meta_df], ignore_index=True)
    df["channel_grouping"] = df["campaign_name"].apply(parse_name)
    df = df.dropna(subset=["channel_grouping"])
    df = df[df["clicks"] > 0].reset_index(drop=True)
    return df


def generate_paid_sessions_and_orders(ad_df: pd.DataFrame, rng: np.random.Generator):
    session_rows, order_rows = [], []
    order_id_counter = 1

    for row in ad_df.itertuples(index=False):
        cg, platform, clicks = row.channel_grouping, row.platform, row.clicks

        sess_lo, sess_hi = get_range(cg, platform, "session", SESSION_RATE_RANGES)
        sessions = max(0, int(round(clicks * rng.uniform(sess_lo, sess_hi))))

        dur_lo, dur_hi = get_range(cg, platform, "duration", DURATION_RANGES)
        eng_lo, eng_hi = get_range(cg, platform, "engagement", ENGAGEMENT_RANGES)

        session_rows.append({
            "date": row.date,
            "platform": platform,
            "campaign_name": row.campaign_name,
            "channel_grouping": cg,
            "session_source_medium": get_source_medium(platform, cg),
            "sessions": sessions,
            "avg_session_duration": round(rng.uniform(dur_lo, dur_hi), 2),
            "engagement_rate": round(rng.uniform(eng_lo, eng_hi), 4),
        })

        if sessions == 0:
            continue
        conv_lo, conv_hi = get_range(cg, platform, "conv", CONV_RATE_RANGES)
        n_orders = rng.binomial(sessions, rng.uniform(conv_lo, conv_hi))
        if n_orders == 0:
            continue
        revenues = np.clip(
            rng.lognormal(ORDER_VALUE_LOGNORMAL_MEAN_LOG, ORDER_VALUE_LOGNORMAL_SIGMA, size=n_orders),
            *ORDER_VALUE_CLIP,
        )
        for rev in revenues:
            order_rows.append({
                "order_id": order_id_counter,
                "order_date": row.date,
                "platform": platform,
                "campaign_name": row.campaign_name,
                "channel_grouping": cg,
                "utm_source": get_source_medium(platform, cg).split(" / ")[0],
                "utm_medium": get_source_medium(platform, cg).split(" / ")[1],
                "revenue": round(float(rev), 2),
            })
            order_id_counter += 1

    return session_rows, order_rows, order_id_counter


def generate_baseline_traffic(dates: pd.Series, paid_sessions_by_date: pd.Series,
                               rng: np.random.Generator, order_id_start: int):
    session_rows, order_rows = [], []
    order_id_counter = order_id_start

    for d in dates:
        paid_total = paid_sessions_by_date.get(d, 0)
        baseline_total = paid_total * rng.uniform(0.35, 0.55)
        if baseline_total <= 0:
            baseline_total = rng.uniform(20, 80)  # floor for dates with no paid traffic at all

        for ch in BASELINE_CHANNELS:
            sessions = max(0, int(round(baseline_total * ch["share"] * rng.uniform(0.85, 1.15))))
            dur_lo, dur_hi = ch["duration"]
            eng_lo, eng_hi = ch["engagement"]
            session_rows.append({
                "date": d,
                "platform": "Organic/Direct",
                "campaign_name": "(not tagged)",
                "channel_grouping": ch["channel_grouping"],
                "session_source_medium": ch["source_medium"],
                "sessions": sessions,
                "avg_session_duration": round(rng.uniform(dur_lo, dur_hi), 2),
                "engagement_rate": round(rng.uniform(eng_lo, eng_hi), 4),
            })
            if sessions == 0:
                continue
            conv_lo, conv_hi = ch["conv"]
            n_orders = rng.binomial(sessions, rng.uniform(conv_lo, conv_hi))
            if n_orders == 0:
                continue
            revenues = np.clip(
                rng.lognormal(ORDER_VALUE_LOGNORMAL_MEAN_LOG, ORDER_VALUE_LOGNORMAL_SIGMA, size=n_orders),
                *ORDER_VALUE_CLIP,
            )
            src, med = ch["source_medium"].split(" / ") if " / " in ch["source_medium"] else (ch["source_medium"], "")
            for rev in revenues:
                order_rows.append({
                    "order_id": order_id_counter,
                    "order_date": d,
                    "platform": "Organic/Direct",
                    "campaign_name": "(not tagged)",
                    "channel_grouping": ch["channel_grouping"],
                    "utm_source": src.strip(),
                    "utm_medium": med.strip(),
                    "revenue": round(float(rev), 2),
                })
                order_id_counter += 1

    return session_rows, order_rows


def run(bing_path, google_path, meta_path, outdir):
    random.seed(SEED)
    rng = np.random.default_rng(SEED)
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    ad_df = build_unified_ad_data(bing_path, google_path, meta_path)

    paid_session_rows, paid_order_rows, next_order_id = generate_paid_sessions_and_orders(ad_df, rng)

    paid_sessions_df = pd.DataFrame(paid_session_rows)
    paid_sessions_by_date = paid_sessions_df.groupby("date")["sessions"].sum()
    all_dates = pd.Series(sorted(ad_df["date"].unique()))

    baseline_session_rows, baseline_order_rows = generate_baseline_traffic(
        all_dates, paid_sessions_by_date, rng, next_order_id
    )

    sessions_df = pd.concat([paid_sessions_df, pd.DataFrame(baseline_session_rows)], ignore_index=True)
    orders_df = pd.concat([pd.DataFrame(paid_order_rows), pd.DataFrame(baseline_order_rows)], ignore_index=True)

    sessions_df["date"] = pd.to_datetime(sessions_df["date"])
    orders_df["order_date"] = pd.to_datetime(orders_df["order_date"])

    sessions_df["join_key"] = sessions_df["date"].dt.strftime("%Y-%m-%d") + "|" + sessions_df["channel_grouping"]
    orders_df["join_key"] = orders_df["order_date"].dt.strftime("%Y-%m-%d") + "|" + orders_df["channel_grouping"]

    sessions_df = sessions_df.sort_values(["date", "platform", "campaign_name"]).reset_index(drop=True)
    orders_df = orders_df.sort_values(["order_date", "order_id"]).reset_index(drop=True)

    sessions_df.to_csv(outdir / "synthetic_ga4_sessions.csv", index=False)
    orders_df.to_csv(outdir / "synthetic_shopify_orders.csv", index=False)

    print(f"GA4 sessions (synthetic): {len(sessions_df)} rows -> {outdir / 'synthetic_ga4_sessions.csv'}")
    print(f"Shopify orders (synthetic): {len(orders_df)} rows, ${orders_df['revenue'].sum():,.2f} total revenue "
          f"-> {outdir / 'synthetic_shopify_orders.csv'}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bing", default="bing_campaign_stats.csv")
    parser.add_argument("--google", default="google_ads_campaign_stats.csv")
    parser.add_argument("--meta", default="meta_ads_campaign_stats.csv")
    parser.add_argument("--outdir", default="./output")
    args = parser.parse_args()
    run(args.bing, args.google, args.meta, args.outdir)
