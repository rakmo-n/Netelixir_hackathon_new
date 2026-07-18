#!/usr/bin/env python
"""
Stage 9: Recommendations Engine
Generates prioritized, actionable recommendations by applying business rules
to the AI explanations, budget simulations, and validation metrics.

Rules are applied in priority order and produce structured JSON + Markdown.
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
STAGE4_DIR = PROJECT_ROOT / "stage4_probabilistic_forecasting" / "outputs"
STAGE5_DIR = PROJECT_ROOT / "stage5_budget_simulation" / "outputs"
STAGE6_DIR = PROJECT_ROOT / "stage6_explanation_layer" / "outputs"
OUTPUT_DIR = PROJECT_ROOT / "stage9_recommendations" / "outputs"

HORIZON_LABELS = {30: "H30", 60: "H60", 90: "H90"}

# ──────────────────────────────────────────────────────────────────────────────
# BUSINESS RULES
# ──────────────────────────────────────────────────────────────────────────────

def rule_structural_shift(exp, val_row):
    """Rule 1: If structural shift detected, recommend model retraining."""
    if val_row is not None and val_row["train_mean_revenue"] > 0:
        ratio = val_row["test_mean_revenue"] / val_row["train_mean_revenue"]
        if ratio > 2.0 or ratio < 0.5:
            return {
                "priority": 1,
                "category": "Model Risk",
                "title": f"Retrain model for {exp['grain']} ({exp['horizon_label']})",
                "description": f"Test-period mean ({ratio:.1f}x training mean) indicates a structural shift. Current model is miscalibrated.",
                "expected_impact": "Improved forecast accuracy by capturing new regime patterns.",
                "effort": "Medium (2–3 days to retrain with post-shift data)",
                "confidence": "High",
                "action": "Collect post-Feb 2026 data, add regime indicator feature, retrain HistGradientBoostingRegressor.",
                "grain": exp["grain"],
                "horizon": exp["horizon_label"],
            }
    return None


def rule_low_coverage(exp, val_row):
    """Rule 2: If coverage < 50%, recommend wider intervals or model change."""
    if val_row is not None and val_row["coverage_p10_p90"] < 0.5:
        return {
            "priority": 2,
            "category": "Model Calibration",
            "title": f"Widen prediction intervals for {exp['grain']} ({exp['horizon_label']})",
            "description": f"Coverage rate is only {val_row['coverage_p10_p90']:.1%}. Model is overconfident.",
            "expected_impact": "More reliable risk assessment. Fewer 'surprise' misses.",
            "effort": "Low (tune quantile parameters or switch to p5/p95)",
            "confidence": "High",
            "action": "Retrain with p5/p95 quantiles, or increase regularization to reduce overfitting.",
            "grain": exp["grain"],
            "horizon": exp["horizon_label"],
        }
    return None


def rule_high_roas_low_spend(budget_row):
    """Rule 3: If ROAS > 5x and spend is low, recommend budget increase."""
    if budget_row is None:
        return None
    daily_spend = budget_row.get("historical_mean_daily_spend", 0)
    if budget_row["p50_roas"] > 5.0 and daily_spend < 5000:
        return {
            "priority": 3,
            "category": "Budget Optimization",
            "title": f"Increase budget for {budget_row['grain']} ({budget_row['horizon_days']}d)",
            "description": f"High ROAS ({budget_row['p50_roas']:.2f}x) with low daily spend ({daily_spend:.0f} $/day). Underinvested channel.",
            "expected_impact": f"Revenue uplift: ~{(budget_row['p50_roas'] - 1):.1f}x per dollar of incremental spend.",
            "effort": "Low (increase daily budget in ad platform)",
            "confidence": "Medium",
            "action": f"Increase daily budget by 25–50% and monitor ROAS over next 14 days.",
            "grain": budget_row["grain"],
            "horizon": HORIZON_LABELS.get(budget_row["horizon_days"], str(budget_row["horizon_days"])),
        }
    return None


def rule_low_roas_high_spend(budget_row):
    """Rule 4: If ROAS < 1.5x and spend is high, recommend budget decrease or optimization."""
    if budget_row is None:
        return None
    daily_spend = budget_row.get("historical_mean_daily_spend", 0)
    if budget_row["p50_roas"] < 1.5 and daily_spend > 1000:
        return {
            "priority": 3,
            "category": "Budget Optimization",
            "title": f"Optimize or reduce spend for {budget_row['grain']} ({budget_row['horizon_days']}d)",
            "description": f"Low ROAS ({budget_row['p50_roas']:.2f}x) with significant daily spend ({daily_spend:.0f} $/day). Diminishing returns.",
            "expected_impact": "Cost savings of 20–40% with minimal revenue loss if spend is reallocated.",
            "effort": "Medium (audience/targeting review + A/B test)",
            "confidence": "Medium",
            "action": "Review audience targeting, pause underperforming ad groups, test new creatives. Consider 20% budget reduction.",
            "grain": budget_row["grain"],
            "horizon": HORIZON_LABELS.get(budget_row["horizon_days"], str(budget_row["horizon_days"])),
        }
    return None


def rule_large_forecast_error(exp, val_row):
    """Rule 5: If actual deviates >50% from p50, recommend investigation."""
    metrics = exp.get("metrics", {})
    actual = metrics.get("actual_revenue", 0)
    p50 = metrics.get("p50_revenue", 0)
    
    if p50 > 0 and abs(actual - p50) / p50 > 0.5:
        deviation = (actual - p50) / p50 * 100
        direction = "over" if deviation > 0 else "under"
        return {
            "priority": 2,
            "category": "Investigation",
            "title": f"Investigate {exp['grain']} ({exp['horizon_label']}) {direction}performance",
            "description": f"Actual revenue ({actual:,.0f}) deviates {abs(deviation):.0f}% from forecast ({p50:,.0f}).",
            "expected_impact": "Identify root cause (campaign changes, external factors, data issues).",
            "effort": "Low (1–2 hours of ad platform review)",
            "confidence": "High",
            "action": "Check ad platform for campaign changes, budget shifts, or tracking issues in the forecast period.",
            "grain": exp["grain"],
            "horizon": exp["horizon_label"],
        }
    return None


def rule_roas_collapse(exp):
    """Rule 6: If ROAS < 1.0x, immediate alert."""
    metrics = exp.get("metrics", {})
    if metrics.get("actual_roas", 999) < 1.0:
        return {
            "priority": 1,
            "category": "Urgent Alert",
            "title": f"URGENT: {exp['grain']} ({exp['horizon_label']}) is unprofitable",
            "description": f"ROAS is {metrics['actual_roas']:.2f}x — below breakeven. Every dollar spent loses money.",
            "expected_impact": "Immediate cost savings by pausing or restructuring.",
            "effort": "Low (pause campaign or reduce bids)",
            "confidence": "High",
            "action": "Pause campaign immediately. Audit landing pages, audience targeting, and creative relevance before restart.",
            "grain": exp["grain"],
            "horizon": exp["horizon_label"],
        }
    return None


def rule_search_optimization(budget_row):
    """Rule 7: Search has highest ROAS but steep dropoff — optimize spend level."""
    if budget_row is None:
        return None
    if budget_row["grain"] == "Search" and budget_row["horizon_days"] == 30:
        if budget_row["p50_roas"] > 8.0:
            return {
                "priority": 4,
                "category": "Strategic",
                "title": "Optimize Search campaign spend level",
                "description": f"Search has highest ROAS ({budget_row['p50_roas']:.2f}x) but response curve shows steep diminishing returns. Find the sweet spot.",
                "expected_impact": "Maximize incremental revenue without pushing into diminishing returns.",
                "effort": "Medium (run A/B budget tests at 0.8x, 1.0x, 1.2x multipliers)",
                "confidence": "Medium",
                "action": "Test budget multipliers between 0.8x and 1.2x over 2-week windows. Measure marginal ROAS at each level.",
                "grain": "Search",
                "horizon": "H30",
            }
    return None


# ──────────────────────────────────────────────────────────────────────────────
# MAIN ENGINE
# ──────────────────────────────────────────────────────────────────────────────

def load_data():
    """Load all required data."""
    print("Loading data...")
    
    with open(STAGE6_DIR / "explanations_master.json", "r") as f:
        explanations = json.load(f)
    
    val_metrics = pd.read_csv(STAGE4_DIR / "validation_metrics.csv")
    budget_sim = pd.read_csv(STAGE5_DIR / "budget_simulation.csv")
    
    print(f"  Explanations: {len(explanations)}")
    print(f"  Validation metrics: {len(val_metrics)}")
    print(f"  Budget simulations: {len(budget_sim)}")
    
    return explanations, val_metrics, budget_sim


def generate_recommendations(explanations, val_metrics, budget_sim):
    """Apply all rules to generate recommendations."""
    
    recommendations = []
    
    for exp in explanations:
        grain = exp["grain"]
        horizon = exp["horizon_days"]
        hlabel = HORIZON_LABELS.get(horizon, str(horizon))
        
        # Get matching rows
        val_row = val_metrics[
            (val_metrics["grain"] == grain) & (val_metrics["horizon_days"] == horizon)
        ]
        val_row = val_row.iloc[0] if len(val_row) > 0 else None
        
        budget_row = budget_sim[
            (budget_sim["grain"] == grain) & (budget_sim["horizon_days"] == horizon) & (budget_sim["budget_multiplier"] == 1.0)
        ]
        budget_row = budget_row.iloc[0] if len(budget_row) > 0 else None
        
        # Apply all rules
        for rule_fn in [
            rule_roas_collapse,
            rule_structural_shift,
            rule_low_coverage,
            rule_large_forecast_error,
            rule_high_roas_low_spend,
            rule_low_roas_high_spend,
            rule_search_optimization,
        ]:
            if rule_fn in [rule_high_roas_low_spend, rule_low_roas_high_spend, rule_search_optimization]:
                rec = rule_fn(budget_row)
            elif rule_fn in [rule_structural_shift, rule_low_coverage]:
                rec = rule_fn(exp, val_row)
            else:
                rec = rule_fn(exp, val_row) if rule_fn == rule_large_forecast_error else rule_fn(exp)
            
            if rec is not None and rec not in recommendations:
                recommendations.append(rec)
    
    # Remove duplicates based on title
    seen = set()
    unique = []
    for rec in recommendations:
        if rec["title"] not in seen:
            seen.add(rec["title"])
            unique.append(rec)
    
    # Sort by priority
    unique.sort(key=lambda x: x["priority"])
    
    return unique


def build_markdown(recommendations, explanations, val_metrics, budget_sim):
    """Build a human-readable Markdown report."""
    
    md = f"""# Stage 9: Recommendations Engine
## Automated Recommendations from AIgnition Pipeline

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**Total Recommendations:** {len(recommendations)}  
**Rule Engine:** 7 business rules applied across 42 grain/horizon combinations

---

"""
    
    # Priority summary
    md += "## Priority Summary\n\n"
    md += "| Priority | Category | Count |\n"
    md += "|----------|----------|-------|\n"
    
    from collections import Counter
    priority_counts = Counter(r["priority"] for r in recommendations)
    category_counts = Counter(r["category"] for r in recommendations)
    
    for p in sorted(priority_counts.keys()):
        label = {1: "P1: Urgent", 2: "P2: High", 3: "P3: Medium", 4: "P4: Strategic"}.get(p, f"P{p}")
        md += f"| {label} | — | {priority_counts[p]} |\n"
    
    md += "\n| Category | Count |\n"
    md += "|----------|-------|\n"
    for cat, count in category_counts.most_common():
        md += f"| {cat} | {count} |\n"
    
    md += "\n---\n\n"
    
    # Detailed recommendations
    md += "## Detailed Recommendations\n\n"
    
    for i, rec in enumerate(recommendations, 1):
        priority_label = {1: "Urgent", 2: "High", 3: "Medium", 4: "Strategic"}.get(rec["priority"], f"P{rec['priority']}")
        
        md += f"### {i}. [{priority_label}] {rec['title']}\n\n"
        md += f"**Category:** {rec['category']}  \n"
        md += f"**Grain:** {rec['grain']} | **Horizon:** {rec['horizon']}  \n"
        md += f"**Confidence:** {rec['confidence']} | **Effort:** {rec['effort']}\n\n"
        md += f"**Description:** {rec['description']}\n\n"
        md += f"**Expected Impact:** {rec['expected_impact']}\n\n"
        md += f"**Action:** {rec['action']}\n\n"
        md += "---\n\n"
    
    # Quick reference table
    md += "## Quick Reference Table\n\n"
    md += "| # | Priority | Grain | Horizon | Category | Action |\n"
    md += "|---|----------|-------|---------|----------|--------|\n"
    for i, rec in enumerate(recommendations, 1):
        priority_label = {1: "Urgent", 2: "High", 3: "Medium", 4: "Strategic"}.get(rec["priority"], f"P{rec['priority']}")
        md += f"| {i} | {priority_label} | {rec['grain']} | {rec['horizon']} | {rec['category']} | {rec['action'][:60]}... |\n"
    
    md += "\n"
    
    return md


# ──────────────────────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("STAGE 9: Recommendations Engine")
    print("=" * 60)
    
    explanations, val_metrics, budget_sim = load_data()
    
    print("\nApplying business rules...")
    recommendations = generate_recommendations(explanations, val_metrics, budget_sim)
    
    print(f"Generated {len(recommendations)} recommendations.")
    
    # Save JSON
    json_path = OUTPUT_DIR / "recommendations.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "generated_at": datetime.now().isoformat(),
            "total_recommendations": len(recommendations),
            "rules_applied": 7,
            "recommendations": recommendations,
        }, f, indent=2, ensure_ascii=False)
    
    # Save Markdown
    md = build_markdown(recommendations, explanations, val_metrics, budget_sim)
    md_path = OUTPUT_DIR / "recommendations.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)
    
    print(f"\nJSON saved: {json_path}")
    print(f"Markdown saved: {md_path}")
    print(f"\nPriority breakdown:")
    from collections import Counter
    for p, c in sorted(Counter(r["priority"] for r in recommendations).items()):
        label = {1: "Urgent", 2: "High", 3: "Medium", 4: "Strategic"}.get(p, f"P{p}")
        print(f"  {label}: {c}")
    
    return 0


if __name__ == "__main__":
    exit(main())
