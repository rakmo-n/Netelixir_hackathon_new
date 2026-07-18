#!/usr/bin/env python
"""
Stage 7: Dashboard & UI (Optimized)
Generates a self-contained HTML dashboard with embedded charts.
Optimized for speed by limiting chart generation.
"""

import warnings
import base64
import json
from io import BytesIO
from pathlib import Path
from datetime import datetime

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")
plt.style.use("default")

# ──────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ──────────────────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).parent.parent.parent
STAGE4_DIR = PROJECT_ROOT / "stage4_probabilistic_forecasting" / "outputs"
STAGE5_DIR = PROJECT_ROOT / "stage5_budget_simulation" / "outputs"
STAGE6_DIR = PROJECT_ROOT / "stage6_explanation_layer" / "outputs"
OUTPUT_DIR = PROJECT_ROOT / "stage7_dashboard_ui" / "outputs"

COLORS = {
    "p10": "#d4a373",
    "p50": "#4a90e2",
    "p90": "#d4a373",
    "actual": "#2ecc71",
    "band": "#4a90e2",
}

def fig_to_base64(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=72, bbox_inches="tight", facecolor="white")
    buf.seek(0)
    img = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return img

def load_data():
    print("Loading data...")
    forecasts = pd.read_csv(STAGE4_DIR / "probabilistic_forecasts.csv")
    forecasts["forecast_origin_date"] = pd.to_datetime(forecasts["forecast_origin_date"])
    budget_sim = pd.read_csv(STAGE5_DIR / "budget_simulation.csv")
    with open(STAGE6_DIR / "explanations_master.json", "r") as f:
        explanations = json.load(f)
    val_metrics = pd.read_csv(STAGE4_DIR / "validation_metrics.csv")
    print(f"  Loaded: {len(forecasts)} forecasts, {len(budget_sim)} sims, {len(explanations)} explanations")
    return forecasts, budget_sim, explanations, val_metrics

def generate_forecast_chart(forecasts, grain, horizon):
    subset = forecasts[(forecasts["grain"] == grain) & (forecasts["horizon_days"] == horizon)].sort_values("forecast_origin_date")
    if subset.empty:
        return None
    fig, ax = plt.subplots(figsize=(7, 2.5), facecolor="white")
    dates = subset["forecast_origin_date"]
    ax.fill_between(dates, subset["p10_revenue"], subset["p90_revenue"], alpha=0.2, color=COLORS["band"], label="80% CI")
    ax.plot(dates, subset["p50_revenue"], color=COLORS["p50"], linewidth=1.5, label="p50")
    actual = subset["actual_revenue"]
    if not actual.isna().all():
        ax.scatter(dates, actual, color=COLORS["actual"], s=15, zorder=5, label="Actual")
    ax.set_title(f"{grain} — H{horizon} Revenue", fontsize=10, fontweight="bold")
    ax.legend(loc="upper left", fontsize=7)
    ax.grid(True, alpha=0.3)
    ax.tick_params(axis="x", rotation=45, labelsize=7)
    ax.tick_params(axis="y", labelsize=7)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1e3:.0f}K" if x < 1e6 else f"${x/1e6:.1f}M"))
    fig.tight_layout()
    return fig_to_base64(fig)

def generate_budget_chart(budget_sim, grain, horizon):
    subset = budget_sim[(budget_sim["grain"] == grain) & (budget_sim["horizon_days"] == horizon)].sort_values("budget_multiplier")
    if subset.empty or len(subset) < 2:
        return None
    fig, ax = plt.subplots(figsize=(7, 2.5), facecolor="white")
    ax.plot(subset["budget_multiplier"], subset["p50_revenue"], marker="o", color=COLORS["p50"], linewidth=1.5, markersize=4)
    ax.fill_between(subset["budget_multiplier"], subset["p10_revenue"], subset["p90_revenue"], alpha=0.2, color=COLORS["band"])
    ax.axvline(x=1.0, color="gray", linestyle="--", alpha=0.5)
    ax.set_title(f"{grain} — H{horizon} Budget Simulation", fontsize=10, fontweight="bold")
    ax.set_xlabel("Budget Multiplier", fontsize=8)
    ax.set_ylabel("Revenue ($)", fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.tick_params(labelsize=7)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1e3:.0f}K" if x < 1e6 else f"${x/1e6:.1f}M"))
    fig.tight_layout()
    return fig_to_base64(fig)

def generate_overview_charts(forecasts, val_metrics):
    # Coverage heatmap
    fig, ax = plt.subplots(figsize=(8, 3), facecolor="white")
    pivot = val_metrics.pivot_table(index="grain", columns="horizon_days", values="coverage_p10_p90", aggfunc="mean")
    im = ax.imshow(pivot.values, cmap="RdYlGn", aspect="auto", vmin=0, vmax=1)
    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels([f"H{h}" for h in pivot.columns])
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index, fontsize=7)
    ax.set_title("Coverage Rate (p10-p90)", fontsize=11, fontweight="bold")
    for i in range(len(pivot.index)):
        for j in range(len(pivot.columns)):
            val = pivot.iloc[i, j]
            if not pd.isna(val):
                text_color = "white" if val < 0.3 or val > 0.8 else "black"
                ax.text(j, i, f"{val:.0%}", ha="center", va="center", color=text_color, fontsize=7)
    fig.colorbar(im, ax=ax, label="Coverage")
    fig.tight_layout()
    coverage_chart = fig_to_base64(fig)
    
    # Latest H30 bar chart
    fig, ax = plt.subplots(figsize=(8, 3), facecolor="white")
    latest = forecasts.loc[forecasts.groupby("grain")["forecast_origin_date"].idxmax()]
    latest_h30 = latest[latest["horizon_days"] == 30].sort_values("p50_revenue", ascending=True)
    y_pos = range(len(latest_h30))
    p50 = latest_h30["p50_revenue"].values
    p10 = latest_h30["p10_revenue"].values
    p90 = latest_h30["p90_revenue"].values
    labels = latest_h30["grain"].values
    ax.barh(y_pos, p50, color=COLORS["p50"], alpha=0.8)
    lower_err = np.maximum(p50 - p10, 0)
    upper_err = np.maximum(p90 - p50, 0)
    ax.errorbar(p50, y_pos, xerr=[lower_err, upper_err], fmt="none", color="#666", alpha=0.5, capsize=2)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=8)
    ax.set_title("Latest H30 Forecast by Grain", fontsize=11, fontweight="bold")
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1e3:.0f}K" if x < 1e6 else f"${x/1e6:.1f}M"))
    ax.grid(axis="x", alpha=0.3)
    fig.tight_layout()
    bar_chart = fig_to_base64(fig)
    return coverage_chart, bar_chart

HTML_STYLE = """<style>
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f7fa; color: #1a1a2e; line-height: 1.5; padding: 20px; margin: 0; }
  .header { background: linear-gradient(135deg, #1a1a2e, #16213e); color: white; padding: 24px 32px; border-radius: 12px; margin-bottom: 20px; }
  .header h1 { font-size: 26px; margin-bottom: 6px; }
  .header p { opacity: 0.8; font-size: 13px; margin: 0; }
  .header .meta { margin-top: 10px; font-size: 11px; opacity: 0.6; }
  .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(360px, 1fr)); gap: 16px; }
  .card { background: white; border-radius: 10px; padding: 18px; box-shadow: 0 1px 4px rgba(0,0,0,0.05); border: 1px solid #e0e4e8; }
  .card h3 { font-size: 15px; font-weight: 600; margin-bottom: 12px; color: #1a1a2e; border-bottom: 2px solid #e8f0fe; padding-bottom: 6px; }
  .card h4 { font-size: 12px; font-weight: 600; color: #666; margin: 12px 0 6px; text-transform: uppercase; letter-spacing: 0.5px; }
  .metric-row { display: flex; gap: 12px; margin-bottom: 12px; }
  .metric { flex: 1; background: #e8f0fe; padding: 10px 12px; border-radius: 6px; }
  .metric .label { font-size: 10px; color: #666; text-transform: uppercase; }
  .metric .value { font-size: 16px; font-weight: 700; color: #4a90e2; }
  .chart-img { width: 100%; border-radius: 6px; margin: 8px 0; }
  .narrative { background: #f8fafc; border-left: 3px solid #4a90e2; padding: 10px 14px; border-radius: 0 6px 6px 0; font-size: 12px; color: #333; margin: 10px 0; }
  .flag { display: inline-block; padding: 3px 8px; border-radius: 12px; font-size: 10px; font-weight: 600; margin: 2px 4px 2px 0; }
  .flag-alert { background: #fee2e2; color: #991b1b; }
  .flag-warning { background: #fef3c7; color: #92400e; }
  .flag-ok { background: #d1fae5; color: #065f46; }
  .features { font-size: 11px; color: #666; margin-top: 6px; }
  .features li { margin: 2px 0; }
  .section-title { font-size: 18px; font-weight: 700; margin: 24px 0 12px; color: #1a1a2e; }
  .overview-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 16px; margin-bottom: 20px; }
  .nav { display: flex; gap: 6px; margin-bottom: 16px; flex-wrap: wrap; }
  .nav a { background: white; padding: 6px 14px; border-radius: 16px; text-decoration: none; color: #4a90e2; font-size: 12px; font-weight: 500; border: 1px solid #e0e4e8; }
  .nav a:hover { background: #e8f0fe; }
</style>"""

def build_card(exp, forecasts, budget_sim, grain, horizon):
    metrics = exp.get("metrics", {})
    flags = exp.get("anomaly_flags", [])
    features = exp.get("top_features", [])
    narrative = exp.get("narrative", "No narrative.")
    
    fchart = generate_forecast_chart(forecasts, grain, horizon)
    bchart = generate_budget_chart(budget_sim, grain, horizon) if grain in ["Bing Ads", "Google Ads", "Meta Ads", "Organic/Direct"] else None
    
    flag_html = ""
    for flag in flags[:3]:
        cls = "flag-alert" if flag["type"] in ["ROAS Collapse", "Underperformance", "Structural Shift"] else "flag-warning" if flag["type"] in ["Large Forecast Error", "Low Coverage"] else "flag-ok"
        flag_html += f'<span class="flag {cls}">{flag["type"]}</span>'
    
    feat_html = "<ul class='features'>"
    for feat in features[:3]:
        feat_html += f"<li><strong>{feat['feature']}</strong>: {feat['importance']:.4f}</li>"
    feat_html += "</ul>"
    
    return f"""
    <div class="card" id="{grain.replace(' ', '_').replace('/', '_')}_H{horizon}">
      <h3>{grain} — H{horizon}</h3>
      <div class="metric-row">
        <div class="metric"><div class="label">p50 Revenue</div><div class="value">${metrics.get('p50_revenue', 0):,.0f}</div></div>
        <div class="metric"><div class="label">p50 ROAS</div><div class="value">{metrics.get('p50_roas', 0):.2f}x</div></div>
        <div class="metric"><div class="label">Actual</div><div class="value">${metrics.get('actual_revenue', 0):,.0f}</div></div>
      </div>
      <div>{flag_html}</div>
      <div class="narrative">{narrative}</div>
      <h4>Forecast</h4>
      {f'<img class="chart-img" src="data:image/png;base64,{fchart}" />' if fchart else '<p style="font-size:11px; color:#666;">No chart.</p>'}
      {f'<h4>Budget Simulation</h4><img class="chart-img" src="data:image/png;base64,{bchart}" />' if bchart else ''}
      <h4>Top Drivers</h4>{feat_html}
    </div>
    """

def build_dashboard(forecasts, budget_sim, explanations, val_metrics):
    print("Generating overview charts...")
    coverage_chart, bar_chart = generate_overview_charts(forecasts, val_metrics)
    
    exp_by_grain = {}
    for exp in explanations:
        g = exp["grain"]
        if g not in exp_by_grain:
            exp_by_grain[g] = {}
        exp_by_grain[g][exp["horizon_label"]] = exp
    
    all_grains = sorted(forecasts["grain"].unique())
    platforms = [g for g in all_grains if g in ["Bing Ads", "Google Ads", "Meta Ads", "Organic/Direct"]]
    campaign_types = [g for g in all_grains if g not in platforms]
    
    html = f"<!DOCTYPE html><html><head><meta charset='UTF-8'><title>AIgnition Dashboard</title>{HTML_STYLE}</head><body>"
    
    html += f"""
    <div class="header">
      <h1>AIgnition Dashboard</h1>
      <p>Probabilistic Forecasting, Budget Simulation & AI Explanation Layer</p>
      <div class="meta">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | Model: HistGradientBoostingRegressor (p10/p50/p90) | LLM: google/gemma-2-2b-it</div>
    </div>
    <div class="nav">
      <a href="#overview">Overview</a>
      <a href="#platforms-h30">Platforms H30</a>
      <a href="#platforms-h60">Platforms H60</a>
      <a href="#platforms-h90">Platforms H90</a>
      <a href="#campaigns-h30">Campaigns H30</a>
      <a href="#campaigns-h60">Campaigns H60</a>
      <a href="#campaigns-h90">Campaigns H90</a>
    </div>
    """
    
    # Overview
    html += '<div class="section-title" id="overview">Portfolio Overview</div>'
    html += '<div class="overview-grid">'
    html += f'<div class="card"><h3>Model Coverage Rate</h3><img class="chart-img" src="data:image/png;base64,{coverage_chart}" /></div>'
    html += f'<div class="card"><h3>Latest H30 Forecasts</h3><img class="chart-img" src="data:image/png;base64,{bar_chart}" /></div>'
    html += '</div>'
    
    # Platforms - H30
    html += '<div class="section-title" id="platforms-h30">Platforms (H30)</div><div class="grid">'
    for grain in platforms:
        exp = exp_by_grain.get(grain, {}).get("H30")
        if exp:
            html += build_card(exp, forecasts, budget_sim, grain, 30)
    html += '</div>'
    
    # Platforms - H60
    html += '<div class="section-title" id="platforms-h60">Platforms (H60)</div><div class="grid">'
    for grain in platforms:
        exp = exp_by_grain.get(grain, {}).get("H60")
        if exp:
            html += build_card(exp, forecasts, budget_sim, grain, 60)
    html += '</div>'
    
    # Platforms - H90
    html += '<div class="section-title" id="platforms-h90">Platforms (H90)</div><div class="grid">'
    for grain in platforms:
        exp = exp_by_grain.get(grain, {}).get("H90")
        if exp:
            html += build_card(exp, forecasts, budget_sim, grain, 90)
    html += '</div>'
    
    # Campaign Types - H30
    html += '<div class="section-title" id="campaigns-h30">Campaign Types (H30)</div><div class="grid">'
    for grain in campaign_types:
        exp = exp_by_grain.get(grain, {}).get("H30")
        if exp:
            html += build_card(exp, forecasts, budget_sim, grain, 30)
    html += '</div>'
    
    # Campaign Types - H60
    html += '<div class="section-title" id="campaigns-h60">Campaign Types (H60)</div><div class="grid">'
    for grain in campaign_types:
        exp = exp_by_grain.get(grain, {}).get("H60")
        if exp:
            html += build_card(exp, forecasts, budget_sim, grain, 60)
    html += '</div>'
    
    # Campaign Types - H90
    html += '<div class="section-title" id="campaigns-h90">Campaign Types (H90)</div><div class="grid">'
    for grain in campaign_types:
        exp = exp_by_grain.get(grain, {}).get("H90")
        if exp:
            html += build_card(exp, forecasts, budget_sim, grain, 90)
    html += '</div>'
    
    html += "</body></html>"
    return html

def main():
    print("=" * 60)
    print("STAGE 7: Dashboard & UI")
    print("=" * 60)
    
    forecasts, budget_sim, explanations, val_metrics = load_data()
    
    print("Building dashboard HTML...")
    html = build_dashboard(forecasts, budget_sim, explanations, val_metrics)
    
    output_path = OUTPUT_DIR / "dashboard.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    size_mb = len(html) / (1024 * 1024)
    print(f"\nDashboard saved: {output_path}")
    print(f"File size: {size_mb:.1f} MB")
    print(f"Open: file:///{output_path}")
    
    return 0

if __name__ == "__main__":
    exit(main())
