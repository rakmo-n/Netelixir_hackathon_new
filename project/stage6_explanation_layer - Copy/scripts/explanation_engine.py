"""
Stage 6: AI-Assisted Causal / Explanation Layer
Explanation Engine — Generates business narratives from model outputs using NVIDIA LLM API.
"""

import os
import json
import time
import warnings
from datetime import datetime
from pathlib import Path

import pandas as pd
import numpy as np
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()

# Try to import openai; install if missing
try:
    from openai import OpenAI
except ImportError:
    import subprocess
    subprocess.check_call(["pip", "install", "openai", "python-dotenv"])
    from openai import OpenAI

warnings.filterwarnings("ignore")

# ──────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ──────────────────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).parent.parent.parent
STAGE4_DIR = PROJECT_ROOT / "stage4_probabilistic_forecasting" / "outputs"
STAGE5_DIR = PROJECT_ROOT / "stage5_budget_simulation" / "outputs"
STAGE2_DIR = PROJECT_ROOT / "stage2_eda_feature_engineering" / "outputs"
OUTPUT_DIR = PROJECT_ROOT / "stage6_explanation_layer" / "outputs"

# NVIDIA LLM config
NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
LLM_MODEL = "google/gemma-2-2b-it"
LLM_TEMPERATURE = 0.2
LLM_TOP_P = 0.7
LLM_MAX_TOKENS = 400
API_DELAY_SECONDS = 1.5  # Rate-limiting between calls

HORIZON_LABELS = {30: "H30", 60: "H60", 90: "H90"}

# ──────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ──────────────────────────────────────────────────────────────────────────────

def load_data():
    """Load all required data sources."""
    print("Loading data sources...")
    
    forecasts = pd.read_csv(STAGE4_DIR / "probabilistic_forecasts.csv")
    feature_imp = pd.read_csv(STAGE4_DIR / "feature_importances.csv")
    val_metrics = pd.read_csv(STAGE4_DIR / "validation_metrics.csv")
    budget_sim = pd.read_csv(STAGE5_DIR / "budget_simulation.csv")
    
    # Convert dates
    forecasts["forecast_origin_date"] = pd.to_datetime(forecasts["forecast_origin_date"])
    
    print(f"  Forecasts: {len(forecasts)} rows")
    print(f"  Feature importances: {len(feature_imp)} rows")
    print(f"  Validation metrics: {len(val_metrics)} rows")
    print(f"  Budget simulations: {len(budget_sim)} rows")
    
    return forecasts, feature_imp, val_metrics, budget_sim


def get_latest_forecast(forecasts, grain, horizon):
    """Get the latest and previous forecast rows for a grain/horizon."""
    subset = forecasts[
        (forecasts["grain"] == grain) & (forecasts["horizon_days"] == horizon)
    ].sort_values("forecast_origin_date")
    
    if len(subset) < 2:
        return subset.iloc[-1] if len(subset) > 0 else None, None
    
    return subset.iloc[-1], subset.iloc[-2]


def get_top_features(feature_imp, grain, horizon, n=3):
    """Get top N features by average importance across quantiles."""
    subset = feature_imp[
        (feature_imp["grain"] == grain) & (feature_imp["horizon_days"] == horizon)
    ]
    
    if subset.empty:
        return []
    
    # Aggregate importance by feature (mean across quantiles)
    agg = subset.groupby("feature")["importance"].mean().reset_index()
    agg = agg.sort_values("importance", ascending=False)
    
    return agg.head(n).to_dict("records")


def compute_metrics(current, previous, validation_row, grain, horizon):
    """Compute all metrics for the narrative."""
    metrics = {
        "grain": grain,
        "horizon": HORIZON_LABELS.get(horizon, str(horizon)),
        "forecast_date": current["forecast_origin_date"].strftime("%Y-%m-%d"),
        "p10_revenue": float(current["p10_revenue"]),
        "p50_revenue": float(current["p50_revenue"]),
        "p90_revenue": float(current["p90_revenue"]),
        "p10_roas": float(current["p10_roas"]),
        "p50_roas": float(current["p50_roas"]),
        "p90_roas": float(current["p90_roas"]),
        "actual_revenue": float(current["actual_revenue"]),
        "actual_spend": float(current["actual_spend"]),
        "actual_roas": float(current["actual_roas"]),
        "interval_width": float(current["p90_revenue"] - current["p10_revenue"]),
    }
    
    # Deltas vs previous period
    if previous is not None:
        metrics["prev_p50_revenue"] = float(previous["p50_revenue"])
        metrics["prev_p50_roas"] = float(previous["p50_roas"])
        metrics["delta_revenue"] = float(current["p50_revenue"] - previous["p50_revenue"])
        metrics["delta_roas"] = float(current["p50_roas"] - previous["p50_roas"])
        metrics["pct_change_revenue"] = (
            (current["p50_revenue"] - previous["p50_revenue"]) / previous["p50_revenue"] * 100
            if previous["p50_revenue"] != 0 else 0
        )
        metrics["prev_interval_width"] = float(previous["p90_revenue"] - previous["p10_revenue"])
        metrics["interval_width_change"] = metrics["interval_width"] - metrics["prev_interval_width"]
    else:
        metrics["prev_p50_revenue"] = None
        metrics["prev_p50_roas"] = None
        metrics["delta_revenue"] = 0.0
        metrics["delta_roas"] = 0.0
        metrics["pct_change_revenue"] = 0.0
        metrics["interval_width_change"] = 0.0
    
    # Validation metrics
    if validation_row is not None:
        metrics["coverage"] = float(validation_row["coverage_p10_p90"])
        metrics["mae"] = float(validation_row["mae"])
        metrics["train_mean"] = float(validation_row["train_mean_revenue"])
        metrics["test_mean"] = float(validation_row["test_mean_revenue"])
    else:
        metrics["coverage"] = None
        metrics["mae"] = None
        metrics["train_mean"] = None
        metrics["test_mean"] = None
    
    return metrics


def detect_anomalies(metrics, current):
    """Detect anomalies and return list of flag dicts."""
    flags = []
    
    # Flag 1: Actual outside prediction interval
    actual = metrics["actual_revenue"]
    p10 = metrics["p10_revenue"]
    p90 = metrics["p90_revenue"]
    
    if not pd.isna(actual) and not pd.isna(p10) and not pd.isna(p90):
        if actual < p10:
            flags.append({
                "type": "Underperformance",
                "description": f"Actual revenue (${actual:,.0f}) is BELOW the p10 lower bound (${p10:,.0f})."
            })
        elif actual > p90:
            flags.append({
                "type": "Overperformance",
                "description": f"Actual revenue (${actual:,.0f}) is ABOVE the p90 upper bound (${p90:,.0f})."
            })
    
    # Flag 2: ROAS collapse (below 1.0x = unprofitable)
    if metrics["actual_roas"] < 1.0:
        flags.append({
            "type": "ROAS Collapse",
            "description": f"Actual ROAS is {metrics['actual_roas']:.2f}x, below the 1.0x breakeven threshold."
        })
    
    # Flag 3: Large forecast error (actual vs p50)
    if not pd.isna(actual) and not pd.isna(metrics["p50_revenue"]) and metrics["p50_revenue"] > 0:
        pct_error = abs(actual - metrics["p50_revenue"]) / metrics["p50_revenue"] * 100
        if pct_error > 50:
            flags.append({
                "type": "Large Forecast Error",
                "description": f"Actual revenue deviates {pct_error:.0f}% from the p50 forecast."
            })
    
    # Flag 4: Coverage warning (from validation metrics)
    if metrics["coverage"] is not None and metrics["coverage"] < 0.5:
        flags.append({
            "type": "Low Coverage",
            "description": f"Historical coverage rate is only {metrics['coverage']:.1%}, meaning the model is often overconfident."
        })
    
    # Flag 5: Structural shift (train vs test mean)
    if metrics["train_mean"] is not None and metrics["test_mean"] is not None and metrics["train_mean"] > 0:
        ratio = metrics["test_mean"] / metrics["train_mean"]
        if ratio > 2.0 or ratio < 0.5:
            flags.append({
                "type": "Structural Shift",
                "description": f"Test-period mean is {ratio:.1f}x the training mean, suggesting a regime change."
            })
    
    if not flags:
        flags.append({
            "type": "No Anomaly",
            "description": "No significant anomalies detected for this grain and horizon."
        })
    
    return flags


def build_prompt(metrics, top_features, anomaly_flags, grain, horizon):
    """Build a concise, structured prompt for the LLM."""
    
    # Format features
    feature_text = ""
    for i, feat in enumerate(top_features[:3], 1):
        feature_text += f"{i}. {feat['feature']}: {feat['importance']:.4f}\n"
    
    # Format anomalies
    anomaly_text = ""
    for flag in anomaly_flags[:3]:
        anomaly_text += f"- {flag['type']}: {flag['description']}\n"
    
    prompt = f"""You are a senior marketing analyst. Write a concise 4-sentence business summary for a non-technical executive. Use ONLY the data provided. Do not invent numbers. Use cautious language ("associated with", "correlated with", "suggests") — never claim causation.

GRAIN: {grain}
HORIZON: {HORIZON_LABELS.get(horizon, str(horizon))}

FORECAST DATA (latest date: {metrics['forecast_date']}):
- p50 (median) revenue: ${metrics['p50_revenue']:,.0f}
- p10 (lower bound): ${metrics['p10_revenue']:,.0f}
- p90 (upper bound): ${metrics['p90_revenue']:,.0f}
- p50 ROAS: {metrics['p50_roas']:.2f}x
- Actual revenue: ${metrics['actual_revenue']:,.0f}
- Actual ROAS: {metrics['actual_roas']:.2f}x

CHANGE VS PREVIOUS PERIOD:
- Revenue delta: ${metrics['delta_revenue']:,.0f} ({metrics['pct_change_revenue']:+.1f}%)
- Interval width change: ${metrics['interval_width_change']:,.0f}

TOP 3 DRIVERS (by model feature importance):
{feature_text}

ANOMALY FLAGS:
{anomaly_text}

RULES:
1. Sentence 1: State the forecast number, interval, and actual result.
2. Sentence 2: Name the top 2 drivers and explain them in plain business terms.
3. Sentence 3: Mention the most important anomaly using cautious language.
4. Sentence 4: Recommend one specific, actionable next step.
5. Keep sentences short and clear. Avoid jargon.
6. Do NOT invent numbers. Use only the data above.
7. Do NOT claim causation. Use "associated with" or "correlated with."
"""
    return prompt


def call_llm(prompt, client):
    """Call the NVIDIA LLM API with retry logic."""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=LLM_MODEL,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=LLM_TEMPERATURE,
                top_p=LLM_TOP_P,
                max_tokens=LLM_MAX_TOKENS,
                stream=False
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"    API call failed (attempt {attempt+1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                return f"[ERROR: LLM API call failed after {max_retries} attempts. Error: {e}]"
    return "[ERROR: Unknown API failure]"


# ──────────────────────────────────────────────────────────────────────────────
# MAIN EXECUTION
# ──────────────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("STAGE 6: AI-Assisted Causal / Explanation Layer")
    print("=" * 60)
    
    # Initialize LLM client
    if not NVIDIA_API_KEY:
        print("ERROR: NVIDIA_API_KEY not found in environment. Check .env file.")
        return 1
    
    client = OpenAI(base_url=NVIDIA_BASE_URL, api_key=NVIDIA_API_KEY)
    print(f"LLM client initialized: {LLM_MODEL}")
    
    # Load data
    forecasts, feature_imp, val_metrics, budget_sim = load_data()
    
    # Get unique grains and horizons
    grains = sorted(forecasts["grain"].unique())
    horizons = sorted(forecasts["horizon_days"].unique())
    
    print(f"\nGrains: {grains}")
    print(f"Horizons: {horizons}")
    print(f"Total combinations: {len(grains) * len(horizons)}")
    print("-" * 60)
    
    # Process each grain/horizon combination
    results = []
    total = len(grains) * len(horizons)
    count = 0
    
    for grain in grains:
        for horizon in horizons:
            count += 1
            label = f"{grain} / {HORIZON_LABELS.get(horizon, str(horizon))}"
            print(f"[{count:3d}/{total}] Processing {label}...", end=" ")
            
            # Get forecast rows
            current, previous = get_latest_forecast(forecasts, grain, horizon)
            if current is None:
                print("SKIP (no data)")
                continue
            
            # Get validation metrics row
            val_row = val_metrics[
                (val_metrics["grain"] == grain) & (val_metrics["horizon_days"] == horizon)
            ]
            val_row = val_row.iloc[0] if len(val_row) > 0 else None
            
            # Compute metrics
            metrics = compute_metrics(current, previous, val_row, grain, horizon)
            
            # Get top features
            top_features = get_top_features(feature_imp, grain, horizon, n=3)
            
            # Detect anomalies
            anomaly_flags = detect_anomalies(metrics, current)
            
            # Build prompt and call LLM
            prompt = build_prompt(metrics, top_features, anomaly_flags, grain, horizon)
            narrative = call_llm(prompt, client)
            
            print(f"DONE ({len(narrative)} chars)")
            
            # Save individual file
            safe_grain = grain.replace(" ", "_").replace("/", "_")
            filename = f"explanation_{safe_grain}_{HORIZON_LABELS.get(horizon, str(horizon))}.json"
            filepath = OUTPUT_DIR / filename
            
            # Convert metrics to JSON-serializable types
            metrics_serializable = {}
            for k, v in metrics.items():
                if isinstance(v, (np.integer, np.int64, np.int32)):
                    metrics_serializable[k] = int(v)
                elif isinstance(v, (np.floating, np.float64, np.float32)):
                    metrics_serializable[k] = float(v)
                elif isinstance(v, pd.Timestamp):
                    metrics_serializable[k] = v.strftime("%Y-%m-%d")
                else:
                    metrics_serializable[k] = v
            
            result = {
                "grain": grain,
                "level": "platform" if grain in ["Bing Ads", "Google Ads", "Meta Ads", "Organic/Direct"] else "campaign_type",
                "horizon_days": int(horizon),
                "horizon_label": HORIZON_LABELS.get(horizon, str(horizon)),
                "generated_at": datetime.now().isoformat(),
                "metrics": metrics_serializable,
                "top_features": top_features,
                "anomaly_flags": anomaly_flags,
                "prompt": prompt,
                "narrative": narrative,
            }
            
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            results.append(result)
            
            # Rate limiting
            if count < total:
                time.sleep(API_DELAY_SECONDS)
    
    # Save master summary
    master_path = OUTPUT_DIR / "explanations_master.json"
    with open(master_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Save human-readable markdown summary
    md_path = OUTPUT_DIR / "explanations_summary.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Stage 6: AI-Generated Explanations Summary\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"Model: {LLM_MODEL}\n\n")
        f.write("---\n\n")
        
        for r in results:
            f.write(f"## {r['grain']} — {r['horizon_label']}\n\n")
            f.write(f"**Forecast:** ${r['metrics']['p50_revenue']:,.0f} (p50) ")
            f.write(f"| **Range:** ${r['metrics']['p10_revenue']:,.0f} – ${r['metrics']['p90_revenue']:,.0f} (p10–p90)\n\n")
            f.write(f"**Actual:** ${r['metrics']['actual_revenue']:,.0f} | **ROAS:** {r['metrics']['actual_roas']:.2f}x\n\n")
            f.write(f"**Top Drivers:**\n")
            for feat in r['top_features'][:3]:
                f.write(f"- {feat['feature']}: {feat['importance']:.4f}\n")
            f.write(f"\n**Anomalies:**\n")
            for flag in r['anomaly_flags'][:3]:
                f.write(f"- {flag['type']}: {flag['description']}\n")
            f.write(f"\n**Narrative:**\n\n{r['narrative']}\n\n")
            f.write("---\n\n")
    
    print("-" * 60)
    print(f"Done! Generated {len(results)} explanations.")
    print(f"Master JSON: {master_path}")
    print(f"Summary Markdown: {md_path}")
    print(f"Individual JSONs: {OUTPUT_DIR}/explanation_*.json")
    
    return 0


if __name__ == "__main__":
    exit(main())
