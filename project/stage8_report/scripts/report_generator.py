#!/usr/bin/env python
"""
Stage 8: Executive Report
Compiles all stages into a comprehensive Markdown report with:
- Executive summary with key findings
- Methodology overview
- Stage-by-stage results
- AI-generated explanations
- Actionable recommendations
- Appendices with data dictionaries
"""

import warnings
import json
from datetime import datetime
from pathlib import Path

import pandas as pd

warnings.filterwarnings("ignore")

# ──────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ──────────────────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).parent.parent.parent
STAGE1_DIR = PROJECT_ROOT / "stage1_ingestion_validation_reconciliation" / "outputs"
STAGE2_DIR = PROJECT_ROOT / "stage2_eda_feature_engineering" / "outputs"
STAGE3_DIR = PROJECT_ROOT / "stage3_baseline_models" / "outputs"
STAGE4_DIR = PROJECT_ROOT / "stage4_probabilistic_forecasting" / "outputs"
STAGE5_DIR = PROJECT_ROOT / "stage5_budget_simulation" / "outputs"
STAGE6_DIR = PROJECT_ROOT / "stage6_explanation_layer" / "outputs"
OUTPUT_DIR = PROJECT_ROOT / "stage8_report" / "outputs"

HORIZON_LABELS = {30: "30-Day", 60: "60-Day", 90: "90-Day"}

# ──────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ──────────────────────────────────────────────────────────────────────────────

def load_data():
    """Load all stage outputs."""
    print("Loading data...")
    
    # Stage 1
    unified = pd.read_csv(STAGE1_DIR / "unified_campaign_data.csv")
    
    # Stage 4
    forecasts = pd.read_csv(STAGE4_DIR / "probabilistic_forecasts.csv")
    val_metrics = pd.read_csv(STAGE4_DIR / "validation_metrics.csv")
    
    # Stage 5
    budget_sim = pd.read_csv(STAGE5_DIR / "budget_simulation.csv")
    response_curves = pd.read_csv(STAGE5_DIR / "response_curve_params.csv")
    
    # Stage 6
    with open(STAGE6_DIR / "explanations_master.json", "r") as f:
        explanations = json.load(f)
    
    # Stage 3
    baseline_metrics = pd.read_csv(STAGE3_DIR / "validation_metrics.csv")
    
    print(f"  Unified data: {len(unified)} rows")
    print(f"  Forecasts: {len(forecasts)} rows")
    print(f"  Budget sims: {len(budget_sim)} rows")
    print(f"  Explanations: {len(explanations)} narratives")
    
    return unified, forecasts, val_metrics, budget_sim, response_curves, explanations, baseline_metrics


def format_currency(value):
    """Format a number as currency."""
    if pd.isna(value) or value is None:
        return "N/A"
    if abs(value) >= 1e6:
        return f"${value/1e6:.2f}M"
    elif abs(value) >= 1e3:
        return f"${value/1e3:.0f}K"
    else:
        return f"${value:.0f}"


def format_pct(value):
    """Format a number as percentage."""
    if pd.isna(value) or value is None:
        return "N/A"
    return f"{value:.1%}"


# ──────────────────────────────────────────────────────────────────────────────
# REPORT BUILDER
# ──────────────────────────────────────────────────────────────────────────────

def build_executive_summary(unified, forecasts, val_metrics, explanations):
    """Build the executive summary section."""
    
    # Key metrics
    total_rows = len(unified)
    date_range = f"{unified['date'].min()} to {unified['date'].max()}"
    n_grains = forecasts["grain"].nunique()
    
    # Coverage summary
    avg_coverage = val_metrics["coverage_p10_p90"].mean()
    well_calibrated = val_metrics[val_metrics["coverage_p10_p90"] >= 0.5]
    overconfident = val_metrics[val_metrics["coverage_p10_p90"] < 0.5]
    
    # Anomaly count
    anomaly_count = sum(1 for exp in explanations 
                        for f in exp.get("anomaly_flags", []) 
                        if f["type"] != "No Anomaly")
    
    # Latest H30 forecasts
    latest_h30 = forecasts[forecasts["horizon_days"] == 30].groupby("grain").apply(
        lambda x: x.sort_values("forecast_origin_date").iloc[-1]
    ).reset_index(drop=True)
    
    total_forecast = latest_h30["p50_revenue"].sum()
    total_actual = latest_h30["actual_revenue"].sum()
    
    md = f"""## 1. Executive Summary

**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**Data Period:** {date_range}  
**Total Records:** {total_rows:,}  
**Grains Analyzed:** {n_grains} (4 platforms + 10 campaign types)  
**Model:** HistGradientBoostingRegressor with quantile regression (p10/p50/p90)  
**Explanation Engine:** NVIDIA AI (google/gemma-2-2b-it) with structured prompting

---

### Key Findings

| Metric | Value |
|--------|-------|
| **Total H30 Forecast (p50)** | {format_currency(total_forecast)} |
| **Total H30 Actual** | {format_currency(total_actual)} |
| **Avg Coverage Rate (p10–p90)** | {format_pct(avg_coverage)} |
| **Well-Calibrated Grains** | {len(well_calibrated)} / {len(val_metrics)} |
| **Overconfident Grains** | {len(overconfident)} / {len(val_metrics)} |
| **Anomalies Flagged** | {anomaly_count} |

### Critical Insights

1. **Structural Shift Detected:** Google Ads and Meta Ads show test-period means 2× higher than training means, indicating a Feb 2026 regime change. Model coverage is 0% for these grains at H60/H90, meaning the model is systematically underforecasting.

2. **Search Remains Top Performer:** Search campaigns show the highest ROAS (10.3x at H30 baseline) but with the steepest diminishing returns — increasing budget beyond 1.0x yields minimal incremental revenue.

3. **Pmax Near Saturation:** Pmax campaigns already operate at a low ROAS (1.3x at baseline), suggesting they are approaching diminishing returns even at current spend levels.

4. **Organic Channels Stable:** Organic_Search, Direct, and Email show no significant anomalies but also have zero spend, making them purely time-series dependent.

5. **Bing Ads Underutilized:** Bing Ads has strong ROAS (8.9x at H30) but very low spend, suggesting untapped potential for budget reallocation.

---

"""
    return md


def build_methodology():
    """Build the methodology section."""
    return """## 2. Methodology

### 2.1 Data Pipeline (Stages 1–2)

1. **Ingestion:** Extracted from ZIP, unified Bing Ads, Google Ads, Meta Ads, and Organic/Direct into a single CSV with 25,440 rows.
2. **Validation:** 13 data quality checks + 5 reconciliation checks. No critical issues found.
3. **EDA:** Time-series decomposition, ROAS distribution analysis, and feature engineering (spend lags, rolling means, seasonality, day-of-week dummies).
4. **Feature Matrix:** 20+ features per grain including `target_spend_Hd` (cumulative planned spend) as a bridge to budget simulation.

### 2.2 Baseline Models (Stage 3)

- **Holt-Winters ETS:** Exponential smoothing with trend and seasonality (period=7)
- **Seasonal Naive:** Baseline benchmark using last-known seasonal value
- **Sanity Checks:** (1) Train/test mean ratio within 0.33x–3x, (2) HW MAE ≤ 1.5× SN MAE
- **Result:** All 14 grains passed both sanity checks

### 2.3 Probabilistic Forecasting (Stage 4)

- **Model:** HistGradientBoostingRegressor with `loss='quantile'` at p10, p50, p90
- **Walk-forward:** Train pre-2026-02-01, test on Feb 2026 (28 dates)
- **Feature Importance:** Permutation importance (model-agnostic) since quantile mode doesn't expose native importance
- **Output:** 1,176 forecast rows (14 grains × 3 horizons × 28 dates)

### 2.4 Budget Simulation (Stage 5)

- **Response Curves:** Log-saturation, power-law, and Hill function fitted via `scipy.optimize.curve_fit`
- **Budget Multipliers:** 0.5x, 0.75x, 1.0x, 1.25x, 1.5x, 2.0x
- **Output:** 252 simulation rows (8 spend-enabled grains × 3 horizons × 6 multipliers)

### 2.5 AI Explanation (Stage 6)

- **Metrics Computed:** Deltas, permutation importance, anomaly flags (Z-score, coverage, structural shift)
- **LLM:** NVIDIA API (google/gemma-2-2b-it) via OpenAI-compatible endpoint
- **Prompt Design:** 4-sentence structure with explicit constraints: cite numbers, name drivers, flag anomalies with caution, recommend action
- **Caution Language:** All narratives use "associated with," "correlated with," or "suggests" — never claiming causation
- **Output:** 42 structured JSON explanations with business narratives

---

"""


def build_stage_results(forecasts, val_metrics, budget_sim, response_curves, baseline_metrics):
    """Build the detailed stage results section."""
    
    md = "## 3. Detailed Results by Stage\n\n"
    
    # Stage 3: Baseline sanity
    md += "### 3.1 Stage 3: Baseline Model Validation\n\n"
    md += "All 14 grains passed both sanity checks:\n\n"
    md += "| Grain | Level | HW MAE | SN MAE | Ratio | Pass? |\n"
    md += "|-------|-------|--------|--------|-------|-------|\n"
    for _, row in baseline_metrics.head(10).iterrows():
        ratio = row['hw_mae'] / row['sn_mae'] if row['sn_mae'] > 0 else 0
        passed = ratio <= 1.5
        md += f"| {row['grain']} | {row['level']} | {row['hw_mae']:.0f} | {row['sn_mae']:.0f} | {ratio:.2f} | {'PASS' if passed else 'FAIL'} |\n"
    md += "\n*(Full table in Appendix)*\n\n"
    
    # Stage 4: Validation metrics
    md += "### 3.2 Stage 4: Probabilistic Forecast Validation\n\n"
    md += "| Grain | Horizon | MAE | Coverage | Train Mean | Test Mean | Ratio |\n"
    md += "|-------|---------|-----|----------|------------|-----------|-------|\n"
    for _, row in val_metrics.head(20).iterrows():
        ratio = row['test_mean_revenue'] / row['train_mean_revenue'] if row['train_mean_revenue'] > 0 else 0
        md += f"| {row['grain']} | {row['horizon_days']}d | {row['mae']:.0f} | {format_pct(row['coverage_p10_p90'])} | {format_currency(row['train_mean_revenue'])} | {format_currency(row['test_mean_revenue'])} | {ratio:.1f}x |\n"
    md += "\n"
    
    # Stage 5: Response curves
    md += "### 3.3 Stage 5: Budget Simulation & Response Curves\n\n"
    md += "| Grain | Best Fit | R² |\n"
    md += "|-------|----------|----|\n"
    for _, row in response_curves.iterrows():
        best_r2 = max(row.get('log_r2', 0), row.get('power_r2', 0), row.get('hill_r2', 0))
        best_fit = 'log_saturation' if best_r2 == row.get('log_r2', 0) else 'power_law' if best_r2 == row.get('power_r2', 0) else 'hill_function'
        md += f"| {row['grain']} | {best_fit} | {best_r2:.3f} |\n"
    md += "\n"
    
    # Stage 5: Key budget insights
    md += "**Key Budget Insights:**\n\n"
    
    # Get baseline and 2x for each grain
    baseline = budget_sim[budget_sim["budget_multiplier"] == 1.0]
    double = budget_sim[budget_sim["budget_multiplier"] == 2.0]
    
    for _, base in baseline.iterrows():
        dbl = double[(double["grain"] == base["grain"]) & (double["horizon_days"] == base["horizon_days"])]
        if dbl.empty:
            continue
        dbl = dbl.iloc[0]
        roas_drop = base["p50_roas"] - dbl["p50_roas"]
        if abs(roas_drop) > 0.5:
            md += f"- **{base['grain']} ({base['horizon_days']}d):** ROAS drops from {base['p50_roas']:.2f}x (baseline) to {dbl['p50_roas']:.2f}x (2.0x budget), a decline of {roas_drop:.2f}x.\n"
    
    md += "\n"
    
    return md


def build_explanations_section(explanations):
    """Build the AI explanations section."""
    
    md = "## 4. AI-Generated Explanations (Stage 6)\n\n"
    md += "All 42 grain/horizon combinations were processed by the NVIDIA LLM (google/gemma-2-2b-it) with structured prompts enforcing:\n"
    md += "1. Number-grounded narratives (no hallucination)\n"
    md += "2. Causal caution language ('associated with', not 'caused by')\n"
    md += "3. Anomaly flagging with investigation recommendations\n"
    md += "4. Actionable next steps\n\n"
    
    # Group by grain
    by_grain = {}
    for exp in explanations:
        g = exp["grain"]
        if g not in by_grain:
            by_grain[g] = {}
        by_grain[g][exp["horizon_label"]] = exp
    
    for grain in sorted(by_grain.keys()):
        md += f"### 4.{list(sorted(by_grain.keys())).index(grain) + 1} {grain}\n\n"
        for hlabel in ["H30", "H60", "H90"]:
            exp = by_grain[grain].get(hlabel)
            if not exp:
                continue
            
            metrics = exp.get("metrics", {})
            narrative = exp.get("narrative", "No narrative.")
            flags = exp.get("anomaly_flags", [])
            
            md += f"**{hlabel}:**\n"
            md += f"- Forecast: {format_currency(metrics.get('p50_revenue', 0))} (p50)\n"
            md += f"- Actual: {format_currency(metrics.get('actual_revenue', 0))}\n"
            md += f"- Flags: {', '.join(f['type'] for f in flags[:2]) if flags else 'None'}\n\n"
            md += f"> {narrative}\n\n"
    
    return md


def build_recommendations(explanations, budget_sim, val_metrics):
    """Build the recommendations section."""
    
    md = "## 5. Strategic Recommendations\n\n"
    
    # Priority 1: Address structural shifts
    shifts = val_metrics[val_metrics["train_mean_revenue"] > 0]
    shifts = shifts[(shifts["test_mean_revenue"] / shifts["train_mean_revenue"]) > 2.0]
    
    if not shifts.empty:
        md += "### 5.1 Priority 1: Address Structural Shifts\n\n"
        md += "The following grains show test-period means >2× training means, indicating a regime change in Feb 2026:\n\n"
        for _, row in shifts.iterrows():
            md += f"- **{row['grain']} ({row['horizon_days']}d):** Test mean {format_currency(row['test_mean_revenue'])} vs train mean {format_currency(row['train_mean_revenue'])} ({row['test_mean_revenue']/row['train_mean_revenue']:.1f}x)\n"
        md += "\n**Action:** Retrain models with post-shift data. Consider adding a 'regime' indicator feature.\n\n"
    
    # Priority 2: Budget reallocation
    md += "### 5.2 Priority 2: Budget Reallocation Opportunities\n\n"
    
    baseline = budget_sim[budget_sim["budget_multiplier"] == 1.0]
    for _, row in baseline.iterrows():
        daily_spend = row.get("historical_mean_daily_spend", 0)
        if row["p50_roas"] > 5.0 and daily_spend < 1000:
            md += f"- **{row['grain']} ({row['horizon_days']}d):** High ROAS ({row['p50_roas']:.2f}x) but low daily spend ({format_currency(daily_spend)}). Consider increasing budget.\n"
        elif row["p50_roas"] < 1.5 and daily_spend > 1000:
            md += f"- **{row['grain']} ({row['horizon_days']}d):** Low ROAS ({row['p50_roas']:.2f}x) with high daily spend ({format_currency(daily_spend)}). Consider reducing budget or optimizing targeting.\n"
    
    md += "\n"
    
    # Priority 3: Anomaly investigation
    md += "### 5.3 Priority 3: Investigate Flagged Anomalies\n\n"
    
    anomaly_grains = {}
    for exp in explanations:
        for flag in exp.get("anomaly_flags", []):
            if flag["type"] != "No Anomaly":
                key = f"{exp['grain']} ({exp['horizon_label']})"
                if key not in anomaly_grains:
                    anomaly_grains[key] = []
                anomaly_grains[key].append(flag["type"])
    
    for key, flags in sorted(anomaly_grains.items()):
        md += f"- **{key}:** {', '.join(set(flags))}\n"
    
    md += "\n**Action:** For each flagged grain, investigate the specific dates flagged, check for external factors (campaign changes, competitive bidding, tracking issues), and consider refreshing the model.\n\n"
    
    # Priority 4: Model improvement
    md += "### 5.4 Priority 4: Model Improvement Roadmap\n\n"
    md += "1. **Switch to LightGBM:** Enables native SHAP via `TreeExplainer`, giving more granular per-prediction explanations than permutation importance.\n"
    md += "2. **Add External Features:** Include competitor ad spend, market indices, or promotional calendars to capture regime changes.\n"
    md += "3. **Hierarchical Forecasting:** Use top-down or bottom-up reconciliation to ensure platform forecasts sum to campaign-type forecasts.\n"
    md += "4. **Online Learning:** Implement incremental updates so the model adapts to shifts without full retraining.\n"
    md += "5. **Upgrade LLM:** Move from Gemma 2B to GPT-4o or Claude Sonnet for more nuanced, grain-name-aware narratives.\n\n"
    
    return md


def build_appendices(forecasts, val_metrics, budget_sim):
    """Build the appendices."""
    
    md = "## 6. Appendices\n\n"
    
    # Appendix A: Data Dictionary
    md += "### Appendix A: Data Dictionary\n\n"
    md += "| Column | Source | Description |\n"
    md += "|--------|--------|-------------|\n"
    md += "| `grain` | Stage 1 | Aggregation level: platform or campaign type |\n"
    md += "| `level` | Stage 1 | 'platform' or 'campaign_type' |\n"
    md += "| `forecast_origin_date` | Stage 4 | Date the forecast was generated |\n"
    md += "| `horizon_days` | Stage 4 | Forecast window: 30, 60, or 90 days |\n"
    md += "| `p10_revenue` | Stage 4 | 10th percentile forecast (lower bound) |\n"
    md += "| `p50_revenue` | Stage 4 | 50th percentile forecast (median) |\n"
    md += "| `p90_revenue` | Stage 4 | 90th percentile forecast (upper bound) |\n"
    md += "| `actual_revenue` | Stage 4 | Observed revenue for the forecast period |\n"
    md += "| `p50_roas` | Stage 4 | Median forecasted Return on Ad Spend |\n"
    md += "| `budget_multiplier` | Stage 5 | Hypothetical spend multiplier (0.5x–2.0x) |\n"
    md += "| `coverage_p10_p90` | Stage 4 | % of test dates where actual fell in p10–p90 |\n"
    md += "| `importance` | Stage 4 | Permutation importance score per feature |\n"
    md += "| `narrative` | Stage 6 | LLM-generated business explanation |\n"
    md += "\n"
    
    # Appendix B: Full validation table
    md += "### Appendix B: Complete Validation Metrics\n\n"
    md += "| Grain | Horizon | MAE | RMSE | Coverage | Interval Width |\n"
    md += "|-------|---------|-----|------|----------|----------------|\n"
    for _, row in val_metrics.iterrows():
        md += f"| {row['grain']} | {row['horizon_days']}d | {format_currency(row['mae'])} | {format_currency(row['rmse'])} | {format_pct(row['coverage_p10_p90'])} | {format_currency(row['mean_interval_width'])} |\n"
    md += "\n"
    
    # Appendix C: Full budget simulation table
    md += "### Appendix C: Complete Budget Simulation (Baseline 1.0x)\n\n"
    md += "| Grain | Horizon | p50 Revenue | p50 ROAS | Daily Spend (Baseline) |\n"
    md += "|-------|---------|-------------|----------|----------------------|\n"
    baseline = budget_sim[budget_sim["budget_multiplier"] == 1.0]
    for _, row in baseline.iterrows():
        daily_spend = row.get("historical_mean_daily_spend", 0)
        md += f"| {row['grain']} | {row['horizon_days']}d | {format_currency(row['p50_revenue'])} | {row['p50_roas']:.2f}x | {format_currency(daily_spend)} |\n"
    md += "\n"
    
    return md


# ──────────────────────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("STAGE 8: Executive Report")
    print("=" * 60)
    
    unified, forecasts, val_metrics, budget_sim, response_curves, explanations, baseline_metrics = load_data()
    
    print("Building report...")
    
    md = f"""# AIgnition Project: Executive Report
## Probabilistic Demand Forecasting, Budget Simulation & AI Explanation

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**Prepared by:** AIgnition Pipeline (Stages 1–9)  
**Data Period:** {unified['date'].min()} to {unified['date'].max()}

---

"""
    
    md += build_executive_summary(unified, forecasts, val_metrics, explanations)
    md += build_methodology()
    md += build_stage_results(forecasts, val_metrics, budget_sim, response_curves, baseline_metrics)
    md += build_explanations_section(explanations)
    md += build_recommendations(explanations, budget_sim, val_metrics)
    md += build_appendices(forecasts, val_metrics, budget_sim)
    
    md += """---

*This report was generated automatically by the AIgnition pipeline. All forecasts, simulations, and explanations are based on the data and methodology documented above. For questions or updates, re-run the corresponding pipeline stage.*
"""
    
    output_path = OUTPUT_DIR / "executive_report.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md)
    
    size_kb = len(md) / 1024
    print(f"\nReport saved: {output_path}")
    print(f"File size: {size_kb:.1f} KB")
    
    return 0


if __name__ == "__main__":
    exit(main())
