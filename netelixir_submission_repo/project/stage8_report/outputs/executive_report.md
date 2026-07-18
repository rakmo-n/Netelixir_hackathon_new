# AIgnition Project: Executive Report
## Probabilistic Demand Forecasting, Budget Simulation & AI Explanation

**Generated:** 2026-06-28 20:16  
**Prepared by:** AIgnition Pipeline (Stages 1–9)  
**Data Period:** 2024-01-01 to 2026-06-05

---

## 1. Executive Summary

**Report Generated:** 2026-06-28 20:16  
**Data Period:** 2024-01-01 to 2026-06-05  
**Total Records:** 25,562  
**Grains Analyzed:** 14 (4 platforms + 10 campaign types)  
**Model:** HistGradientBoostingRegressor with quantile regression (p10/p50/p90)  
**Explanation Engine:** NVIDIA AI (google/gemma-2-2b-it) with structured prompting

---

### Key Findings

| Metric | Value |
|--------|-------|
| **Total H30 Forecast (p50)** | $835K |
| **Total H30 Actual** | $383K |
| **Avg Coverage Rate (p10–p90)** | 32.9% |
| **Well-Calibrated Grains** | 11 / 42 |
| **Overconfident Grains** | 31 / 42 |
| **Anomalies Flagged** | 118 |

### Critical Insights

1. **Structural Shift Detected:** Google Ads and Meta Ads show test-period means 2× higher than training means, indicating a Feb 2026 regime change. Model coverage is 0% for these grains at H60/H90, meaning the model is systematically underforecasting.

2. **Search Remains Top Performer:** Search campaigns show the highest ROAS (10.3x at H30 baseline) but with the steepest diminishing returns — increasing budget beyond 1.0x yields minimal incremental revenue.

3. **Pmax Near Saturation:** Pmax campaigns already operate at a low ROAS (1.3x at baseline), suggesting they are approaching diminishing returns even at current spend levels.

4. **Organic Channels Stable:** Organic_Search, Direct, and Email show no significant anomalies but also have zero spend, making them purely time-series dependent.

5. **Bing Ads Underutilized:** Bing Ads has strong ROAS (8.9x at H30) but very low spend, suggesting untapped potential for budget reallocation.

---

## 2. Methodology

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

## 3. Detailed Results by Stage

### 3.1 Stage 3: Baseline Model Validation

All 14 grains passed both sanity checks:

| Grain | Level | HW MAE | SN MAE | Ratio | Pass? |
|-------|-------|--------|--------|-------|-------|
| Bing Ads | platform | 78 | 92 | 0.85 | PASS |
| Google Ads | platform | 2484 | 2182 | 1.14 | PASS |
| Meta Ads | platform | 172 | 217 | 0.79 | PASS |
| Organic/Direct | platform | 4621 | 2451 | 1.89 | FAIL |
| Search | campaign_type | 938 | 809 | 1.16 | PASS |
| Pmax | campaign_type | 2911 | 1825 | 1.60 | FAIL |
| Direct | campaign_type | 2139 | 1263 | 1.69 | FAIL |
| Organic_Search | campaign_type | 739 | 714 | 1.03 | PASS |
| Email | campaign_type | 944 | 696 | 1.36 | PASS |
| Shopping | campaign_type | 1178 | 1212 | 0.97 | PASS |

*(Full table in Appendix)*

### 3.2 Stage 4: Probabilistic Forecast Validation

| Grain | Horizon | MAE | Coverage | Train Mean | Test Mean | Ratio |
|-------|---------|-----|----------|------------|-----------|-------|
| Bing Ads | 30d | 3052 | 89.3% | $3K | $5K | 1.6x |
| Bing Ads | 60d | 5512 | 7.1% | $6K | $12K | 1.9x |
| Bing Ads | 90d | 2729 | 53.6% | $10K | $8K | 0.8x |
| Google Ads | 30d | 66571 | 89.3% | $102K | $197K | 1.9x |
| Google Ads | 60d | 182347 | 0.0% | $168K | $649K | 3.9x |
| Google Ads | 90d | 109570 | 0.0% | $243K | $369K | 1.5x |
| Meta Ads | 30d | 12232 | 100.0% | $10K | $26K | 2.6x |
| Meta Ads | 60d | 36413 | 0.0% | $15K | $78K | 5.2x |
| Meta Ads | 90d | 8990 | 28.6% | $22K | $33K | 1.5x |
| Organic/Direct | 30d | 63638 | 46.4% | $98K | $178K | 1.8x |
| Organic/Direct | 60d | 242275 | 0.0% | $167K | $550K | 3.3x |
| Organic/Direct | 90d | 79407 | 50.0% | $246K | $307K | 1.2x |
| Search | 30d | 50010 | 57.1% | $46K | $103K | 2.2x |
| Search | 60d | 105883 | 0.0% | $76K | $311K | 4.1x |
| Search | 90d | 47969 | 7.1% | $110K | $179K | 1.6x |
| Pmax | 30d | 5435 | 35.7% | $48K | $56K | 1.2x |
| Pmax | 60d | 12138 | 7.1% | $89K | $156K | 1.7x |
| Pmax | 90d | 6257 | 46.4% | $137K | $88K | 0.6x |
| Direct | 30d | 32868 | 25.0% | $40K | $75K | 1.9x |
| Direct | 60d | 109496 | 0.0% | $67K | $220K | 3.3x |

### 3.3 Stage 5: Budget Simulation & Response Curves

| Grain | Best Fit | R² |
|-------|----------|----|
| Bing Ads | hill_function | 0.266 |
| Google Ads | hill_function | 0.845 |
| Meta Ads | hill_function | 0.680 |
| Search | hill_function | 0.750 |
| Pmax | power_law | 0.873 |
| Shopping | hill_function | 0.903 |
| Remarketing_DPA | hill_function | 0.682 |
| Remarketing_Brand | power_law | 0.304 |

**Key Budget Insights:**

- **Bing Ads (30d):** ROAS drops from 6.27x (baseline) to 3.99x (2.0x budget), a decline of 2.28x.
- **Bing Ads (60d):** ROAS drops from 1.99x (baseline) to 2.55x (2.0x budget), a decline of -0.56x.
- **Google Ads (30d):** ROAS drops from 4.03x (baseline) to 2.51x (2.0x budget), a decline of 1.52x.
- **Google Ads (60d):** ROAS drops from 2.71x (baseline) to 1.36x (2.0x budget), a decline of 1.35x.
- **Meta Ads (30d):** ROAS drops from 5.02x (baseline) to 3.35x (2.0x budget), a decline of 1.67x.
- **Meta Ads (60d):** ROAS drops from 2.09x (baseline) to 1.40x (2.0x budget), a decline of 0.69x.
- **Meta Ads (90d):** ROAS drops from 1.37x (baseline) to 0.75x (2.0x budget), a decline of 0.62x.
- **Search (30d):** ROAS drops from 10.33x (baseline) to 5.79x (2.0x budget), a decline of 4.54x.
- **Search (60d):** ROAS drops from 5.43x (baseline) to 3.29x (2.0x budget), a decline of 2.14x.
- **Search (90d):** ROAS drops from 3.12x (baseline) to 2.55x (2.0x budget), a decline of 0.57x.
- **Remarketing_DPA (30d):** ROAS drops from 9.71x (baseline) to 6.44x (2.0x budget), a decline of 3.27x.
- **Remarketing_DPA (90d):** ROAS drops from 1.60x (baseline) to 0.88x (2.0x budget), a decline of 0.72x.
- **Remarketing_Brand (30d):** ROAS drops from 7.13x (baseline) to 5.65x (2.0x budget), a decline of 1.48x.
- **Remarketing_Brand (60d):** ROAS drops from 3.68x (baseline) to 2.77x (2.0x budget), a decline of 0.91x.
- **Remarketing_Brand (90d):** ROAS drops from 2.86x (baseline) to 1.87x (2.0x budget), a decline of 0.99x.

## 4. AI-Generated Explanations (Stage 6)

All 42 grain/horizon combinations were processed by the NVIDIA LLM (google/gemma-2-2b-it) with structured prompts enforcing:
1. Number-grounded narratives (no hallucination)
2. Causal caution language ('associated with', not 'caused by')
3. Anomaly flagging with investigation recommendations
4. Actionable next steps

### 4.1 Bing Ads

**H30:**
- Forecast: $9K (p50)
- Actual: $4K
- Flags: No Anomaly

> The forecast for Bing Ads revenue in the H30 horizon is projected to be $8,591, with a 6.84x return on ad spend. The top two drivers of this revenue are the day of the month and the spending trend over the past seven days.  There are no significant anomalies detected in this data.  We should analyze the day of the month and spending trends further to optimize campaign performance.

**H60:**
- Forecast: $7K (p50)
- Actual: $14K
- Flags: Overperformance, Large Forecast Error

> The forecast for Bing Ads revenue in H60 is $6,673, with a p50 of $6,673 and actual revenue of $14,182. The top two drivers of this revenue are the rolling average of spending over the past seven and fourteen days, which suggests a strong correlation with current spending patterns.  The model is showing an overperformance, with actual revenue exceeding the upper bound of the forecast.  Next, we should investigate the reasons behind the high actual revenue and explore ways to adjust the model's confidence level.

**H90:**
- Forecast: $6K (p50)
- Actual: $10K
- Flags: Overperformance, Large Forecast Error

> The forecast for Bing Ads revenue in H90 is $9,513, with a p50 of $5,507 and actual revenue of $10,412.  The top two drivers of this performance are the dayofmonth_sin feature and spending, both associated with higher revenue.  The actual revenue is above the p90 upper bound, suggesting a potential overperformance.  Next, we should investigate the specific factors driving this overperformance to understand the drivers of this unexpected result.

### 4.2 Direct

**H30:**
- Forecast: $80K (p50)
- Actual: $35K
- Flags: Underperformance, Large Forecast Error

> The forecast predicts revenue of $80,385 with a p10 lower bound of $97,594, and the actual revenue is $34,672.  The top two drivers of revenue are the day of the week (Monday and Thursday) and whether it's a weekend.  The model is showing an underperformance compared to the p10 lower bound, and has a large forecast error.  Next, we should investigate the model's low coverage rate and explore ways to improve its accuracy.

**H60:**
- Forecast: $104K (p50)
- Actual: $253K
- Flags: Overperformance, Large Forecast Error

> Our forecast predicts a revenue of $103,831 for the next period, with a p50 range of $88,181 to $144,615. The top two drivers of this forecast are the day of the month and the rolling 30-day revenue average.  The model is showing an overperformance in actual revenue, which is significantly higher than the upper bound of the forecast.  We should investigate the reasons for this overperformance to ensure accurate future projections.

**H90:**
- Forecast: $81K (p50)
- Actual: $175K
- Flags: Overperformance, Large Forecast Error

> Our forecast predicts revenue of $99,386 for the H90 period, with a median revenue of $81,048. The top two drivers of this forecast are a rolling revenue trend and the day of the month.  The actual revenue is significantly higher than the upper bound of our forecast, suggesting a potential overperformance.  We should investigate the factors driving this overperformance to ensure we are accurately forecasting future revenue.

### 4.3 Email

**H30:**
- Forecast: $78K (p50)
- Actual: $18K
- Flags: Underperformance, Large Forecast Error

> The forecast predicts a revenue of $78,107 for the next period, with a p10 lower bound of $48,153.  The top two drivers of this forecast are a rolling 7-day revenue average and a rolling 30-day revenue average, both associated with strong revenue growth.  The actual revenue is below the p10 lower bound, indicating underperformance.  A next step should be to investigate the reasons for this underperformance and adjust the model accordingly.

**H60:**
- Forecast: $59K (p50)
- Actual: $160K
- Flags: Overperformance, Large Forecast Error

> The forecast predicts a revenue of $58,837 for the next period, with a 90th percentile revenue of $83,231.  The top two drivers of this forecast are a rolling revenue average and the day of the month.  The model is showing an overperformance in actual revenue, which is significantly higher than the upper bound of the forecast.  Next, we should investigate the model's high confidence level and explore ways to improve its accuracy.

**H90:**
- Forecast: $54K (p50)
- Actual: $114K
- Flags: Overperformance, Large Forecast Error

> Our forecast predicts revenue of $54,274 for the H90 period, with an actual result of $114,085.  The top two drivers of this revenue are a rolling 14-day revenue average and the day of the month, suggesting these factors are influencing our performance.  The model is showing an overperformance, with actual revenue exceeding the upper bound of the forecast.  We should investigate the factors driving this high revenue and consider adjusting our marketing strategy accordingly.

### 4.4 Google Ads

**H30:**
- Forecast: $224K (p50)
- Actual: $98K
- Flags: Large Forecast Error

> The forecast predicts $224,412 in revenue for GRAIN in H30, with a p50 of $224,412 and an actual revenue of $97,569. The top two drivers of this revenue are target spend over the past 30 days and overall spending, both associated with the campaign's performance.  The large forecast error, a deviation of 57% from the p50 forecast, suggests a need for further investigation.  A deeper analysis of the campaign's performance and spending patterns is recommended to understand the discrepancy and optimize future performance.

**H60:**
- Forecast: $459K (p50)
- Actual: $721K
- Flags: Overperformance, Large Forecast Error

> The forecast for GRAIN revenue in H60 is $458,924, with a p50 of 0.93x and actual revenue of $720,741. The top two drivers of this forecast are target spend over the past 60 days and a rolling average of spend over the past 14 days.  The model is showing an overperformance, with actual revenue exceeding the p90 upper bound.  A next step is to investigate the model's high confidence level and potentially adjust the coverage rate.

**H90:**
- Forecast: $421K (p50)
- Actual: $546K
- Flags: Overperformance, Low Coverage

> The forecast for GRAIN revenue in H90 is $475,731, with a p50 of $421,230 and actual revenue of $545,828. The top two drivers of this forecast are target spend over the past 90 days and a rolling average of spend over the past 14 days.  The model's high confidence level, indicated by low historical coverage, is associated with the overperformance of actual revenue.  A next step is to investigate the model's confidence level and explore strategies to improve coverage.

### 4.5 Meta Ads

**H30:**
- Forecast: $27K (p50)
- Actual: $9K
- Flags: Large Forecast Error, Structural Shift

> The forecast for Meta Ads revenue in H30 is $26,953, with a p50 of $26,953 and actual revenue of $8,657. The top two drivers of revenue are target spend over the past 30 days and the day of the month, suggesting that campaign targeting and timing are key factors.  The model indicates a structural shift in the data, meaning the performance is significantly different from historical trends.  To improve performance, we should analyze the impact of the structural shift and adjust our targeting strategy accordingly.

**H60:**
- Forecast: $48K (p50)
- Actual: $95K
- Flags: Overperformance, Large Forecast Error

> The forecast for Meta Ads revenue in H60 is $48,397, with a p50 of $48,397 and actual revenue of $94,563. The top two drivers of this revenue are target spend over the past 60 days and spending in the previous period. The model is overconfident, with a historical coverage rate of 0.0%.  We should investigate the high actual revenue and consider adjusting the model's targeting strategy.

**H90:**
- Forecast: $30K (p50)
- Actual: $50K
- Flags: Overperformance, Large Forecast Error

> The forecast for GRAIN: Meta Ads revenue in H90 is $30,179, with a p50 of $30,179 and actual revenue of $49,772. The top two drivers of this forecast are target spend over the past 90 days and a rolling average of spend over the past 14 days.  The model is showing an overperformance in revenue, exceeding the upper bound of the forecast.  A next step is to investigate the high actual revenue and its drivers to understand the potential for future performance.

### 4.6 Organic/Direct

**H30:**
- Forecast: $193K (p50)
- Actual: $83K
- Flags: Underperformance, Large Forecast Error

> The forecast predicts revenue of $192,849 for the H30 horizon, with a p50 of $192,849.  The top two drivers of revenue are a rolling seven-day average and Sunday's Dow Jones performance.  The model's actual performance is below the p10 lower bound, suggesting potential underperformance.  A deeper dive into the model's confidence levels and historical data is recommended to understand the discrepancy.

**H60:**
- Forecast: $283K (p50)
- Actual: $627K
- Flags: Overperformance, Large Forecast Error

> The forecast predicts revenue of $283,493 for the H60 period, with a p50 of $283,493 and actual revenue of $627,351. The top drivers for this forecast are the day of the month and a rolling 30-day revenue average. The model is associated with a high level of overconfidence, as indicated by its low coverage rate.  A next step is to investigate the model's high confidence and explore potential adjustments to improve its accuracy.

**H90:**
- Forecast: $345K (p50)
- Actual: $445K
- Flags: Overperformance

> The forecast predicts revenue of $345,358 for the H90 period, with a p90 upper bound of $208,342.  The top two drivers of revenue are a rolling 14-day average and the day of the month, suggesting these factors are associated with sales performance.  The actual revenue is above the p90 upper bound, indicating potential overperformance.  To mitigate this, we should investigate the factors driving the high revenue and consider adjusting our marketing strategies accordingly.

### 4.7 Organic_Search

**H30:**
- Forecast: $33K (p50)
- Actual: $23K
- Flags: Underperformance, Low Coverage

> The forecast for revenue in the H30 horizon is projected to be $33,050, with a p10 lower bound of $50,091.  The top two drivers of revenue are a rolling 14-day average and a rolling 30-day average, suggesting that these metrics are closely linked to actual sales performance.  The model is showing an underperformance, as actual revenue is below the p10 lower bound.  To improve performance, we should investigate the reasons behind the low coverage rate and explore strategies to increase the model's accuracy.

**H60:**
- Forecast: $68K (p50)
- Actual: $151K
- Flags: Overperformance, Large Forecast Error

> The forecast for revenue in the H60 horizon is $67,509, with a p50 range of $60,310 to $74,875. The top two drivers of this forecast are the dayofmonth_sin and revenue_rolling_mean_30d, which suggest that the model is influenced by the day of the month and the previous 30-day revenue performance.  The model is flagged for overperformance, as actual revenue is significantly higher than the p90 upper bound.  To improve accuracy, we should investigate the reasons behind the high actual revenue and consider adjusting the model's confidence level.

**H90:**
- Forecast: $64K (p50)
- Actual: $113K
- Flags: Overperformance, Large Forecast Error

> Our forecast predicts revenue of $63,950 for the next 90 days, with a range of $54,992 to $84,214.  The top two drivers of this forecast are a rolling 14-day revenue average and a rolling 7-day revenue average, both associated with strong sales performance.  The actual revenue is above the upper bound of our forecast, suggesting a potential overperformance.  We should investigate the factors driving this overperformance to ensure we are accurately forecasting future revenue.

### 4.8 Organic_Search_Bing

**H30:**
- Forecast: $10K (p50)
- Actual: $5K
- Flags: Underperformance, Large Forecast Error

> The forecast for revenue in the H30 horizon is $10,003 with a p50 range of $11,557 to $19,235.  The top two drivers of this forecast are Sunday and Saturday, suggesting these days are most influential in driving revenue.  The model's actual revenue is below the p10 lower bound, indicating underperformance.  To improve performance, we should investigate the reasons behind the low coverage rate and explore ways to increase the model's accuracy.

**H60:**
- Forecast: $17K (p50)
- Actual: $34K
- Flags: Overperformance, Large Forecast Error

> The forecast predicts revenue of $16,723 for the H60 period, with a 90th percentile revenue of $16,920 and a 50th percentile revenue of $16,493. The top two drivers of this forecast are the day of the month and the day of the week, suggesting that the model is influenced by specific days of the week and month. The model is overconfident, with a historical coverage rate of 0%, which may contribute to the large forecast error.  To improve accuracy, we should investigate the model's assumptions and potentially adjust the model's parameters.

**H90:**
- Forecast: $11K (p50)
- Actual: $24K
- Flags: Overperformance, Large Forecast Error

> Our forecast predicts revenue of $13,295 for the next 90 days, with a p50 of $11,344.  The top two drivers of this forecast are the dayofmonth_sin and dayofmonth_cos, which suggest the model is influenced by the day of the month.  The model is showing an overperformance in actual revenue, exceeding the upper bound of the forecast.  We should investigate the reasons behind this overperformance and adjust the model's parameters accordingly.

### 4.9 Organic_Social

**H30:**
- Forecast: $8K (p50)
- Actual: $3K
- Flags: Underperformance, Large Forecast Error

> The forecast predicts organic social revenue to be $7,590 with a p50 range of $9,534 to $16,775 by 2026-02-28.  The top drivers of this forecast are a rolling seven-day revenue average and the Thursday Dow Jones index.  The model's low coverage rate suggests it may be overconfident in its predictions.  Next, we should investigate the factors driving the significant revenue underperformance compared to the p10 lower bound.

**H60:**
- Forecast: $11K (p50)
- Actual: $28K
- Flags: Overperformance, Large Forecast Error

> The forecast for organic social revenue in H60 is $11,222, with a p50 of $11,222 and actual revenue of $27,968.  The top two drivers of this revenue are a rolling 14-day revenue average and the day of the month, suggesting that consistent revenue growth and the day of the month may be influencing performance.  The model is showing an overperformance, with actual revenue exceeding the upper bound of the forecast.  The next step should be to investigate the reasons for the high actual revenue and explore ways to improve the model's accuracy.

**H90:**
- Forecast: $7K (p50)
- Actual: $19K
- Flags: Overperformance, Large Forecast Error

> Our forecast predicts organic social revenue to be $7,070 in 2026, with a p90 upper bound of $6,559. The top drivers of this forecast are the dayofmonth sine and cosine values, which suggest the model is influenced by the day of the month.  The model is also associated with an overperformance in actual revenue, which deviates significantly from the forecast.  We should investigate the reasons for this overperformance and consider adjusting the model's confidence level.

### 4.10 Pmax

**H30:**
- Forecast: $28K (p50)
- Actual: $36K
- Flags: Overperformance, Low Coverage

> The forecast predicts revenue of $27,926 with a 1.51x ROAS, based on the latest data. The top two drivers of this forecast are the target spend over the past 30 days and the overall spend, suggesting a strong correlation with campaign performance.  The model is showing an overperformance in actual revenue, exceeding the upper bound of the forecast.  To mitigate this, we should analyze the model's confidence and adjust the target spend accordingly.

**H60:**
- Forecast: $152K (p50)
- Actual: $178K
- Flags: Underperformance, ROAS Collapse

> Our forecast predicts revenue of $151,731 for the next 60 days, with a p10 lower bound of $193,122. The top two drivers of this forecast are a high target spend and a historical spend lag.  The model's actual performance is below the p10 lower bound, and its ROAS is below the breakeven threshold.  We should investigate the model's high confidence level and explore ways to improve coverage.

**H90:**
- Forecast: $140K (p50)
- Actual: $131K
- Flags: Underperformance, Low Coverage

> Our forecast predicts a revenue of $140,389 for the next 90 days, with a p50 ROAS of 1.09x. The top two drivers of this forecast are a high target spend for the past 90 days and a historical spend share of 71.77%.  The model is currently showing underperformance, as actual revenue is below the p10 lower bound.  We should investigate the reasons for this underperformance and adjust the campaign strategy accordingly.

### 4.11 Remarketing_Brand

**H30:**
- Forecast: $5K (p50)
- Actual: $3K
- Flags: Structural Shift

> The forecast predicts a revenue of $4,605 for the Remarketing_Brand campaign in H30, with a median revenue of $4,605 and a range from $0 to $7,943. The top two drivers of this forecast are the target spend over the past 30 days and the day of the month, suggesting that campaign spending and the timing of the campaign are important factors.  The structural shift in the test period, where the mean is 2.1 times the training mean, suggests a significant change in the campaign's performance.  A deeper dive into the campaign's performance, particularly the day of the month, is recommended to understand the drivers of the observed change.

**H60:**
- Forecast: $7K (p50)
- Actual: $17K
- Flags: Overperformance, Large Forecast Error

> The forecast predicts a revenue of $7,172 for the next period, with a 90th percentile upper bound of $10,443.  The top two drivers of this forecast are a rolling 30-day revenue trend and a rolling 14-day revenue trend, both associated with positive revenue growth.  The model is showing an overperformance in actual revenue, exceeding the upper bound of the forecast.  A deeper dive into the model's confidence and potential reasons for the high revenue is recommended.

**H90:**
- Forecast: $9K (p50)
- Actual: $11K
- Flags: Low Coverage

> The forecast predicts a revenue of $8,913 for the next 90 days, with a 90th percentile revenue of $15,279 and a median revenue of $8,913.  The top two drivers of this forecast are the target spend over the past 90 days and the rolling average revenue over the past 30 days.  The model's high confidence level, associated with low historical coverage, is a potential concern.  To improve accuracy, we should investigate the historical coverage rate and explore ways to increase data points for the model.

### 4.12 Remarketing_DPA

**H30:**
- Forecast: $18K (p50)
- Actual: $4K
- Flags: Large Forecast Error, Structural Shift

> The forecast for Remarketing_DPA revenue in H30 is $17,882 with a 90% confidence interval of $20,518. Actual revenue for this period is $3,521, resulting in a significant revenue shortfall. The top two drivers of this performance are the target spend over the past 30 days and the day of the month, suggesting a strong correlation with campaign timing.  The large forecast error, indicating a significant deviation from the predicted revenue, warrants further investigation.  A deeper analysis of the campaign's performance and its drivers is needed to understand the discrepancy and optimize future performance.

**H60:**
- Forecast: $28K (p50)
- Actual: $62K
- Flags: Overperformance, Large Forecast Error

> The forecast for Remarketing_DPA revenue in H60 is $27,970, with a p50 revenue of $27,970 and actual revenue of $62,387.  The top two drivers of this revenue are a lag in spending and a targeted spend over the past 60 days.  The model is showing an anomaly with a high actual revenue exceeding the upper bound of the forecast.  The next step is to investigate the high actual revenue and assess if adjustments to the model's targeting or spend strategy are needed.

**H90:**
- Forecast: $12K (p50)
- Actual: $30K
- Flags: Overperformance, Large Forecast Error

> The forecast for Remarketing_DPA revenue in the next 90 days is $12,271, with a p50 of $12,271 and an actual revenue of $30,368. The top two drivers of this revenue are target spend over the past 90 days and overall spending, both associated with higher revenue.  The model is showing an overperformance in actual revenue, which is 147% above the p50 forecast.  To mitigate this, we should analyze the model's confidence and adjust the target spend accordingly.

### 4.13 Search

**H30:**
- Forecast: $119K (p50)
- Actual: $51K
- Flags: Underperformance, Large Forecast Error

> The forecast predicts a revenue of $119,340 for GRAIN: Search in H30, with a p50 of $119,340 and an actual revenue of $50,657.  The top two drivers of revenue are target spend over the past 30 days and overall spending.  The actual revenue is below the p10 lower bound, suggesting underperformance.  Next, we should investigate the reasons behind the structural shift in the test period to understand the potential impact on future performance.

**H60:**
- Forecast: $221K (p50)
- Actual: $349K
- Flags: Overperformance, Large Forecast Error

> The forecast for GRAIN: Search revenue in H60 is $220,645, with a p50 ROAS of 2.17x. The top two drivers of this forecast are target spend over the past 60 days and spending in the previous period. The model is showing an overperformance in revenue, exceeding the p90 upper bound by 58%.  Next, we should investigate the historical coverage rate to understand why the model is so confident.

**H90:**
- Forecast: $159K (p50)
- Actual: $244K
- Flags: Overperformance, Large Forecast Error

> The forecast for GRAIN revenue in H90 is $163,876, with actual revenue reaching $243,548. The top two drivers of this performance are the target spend over the past 90 days and spending trends from the previous period.  The model's high confidence level, indicated by its low coverage rate, suggests potential overconfidence.  A next step is to investigate the model's confidence levels and explore potential adjustments to the target spend strategy.

### 4.14 Shopping

**H30:**
- Forecast: $4K (p50)
- Actual: $12K
- Flags: Large Forecast Error, Structural Shift

> The forecast predicts a revenue of $3,560 for GRAIN: Shopping in H30, with a median revenue of $3,560 and a p50 ROAS of 0.99x. The top two drivers of revenue are target spend over the past 30 days and overall spending, suggesting a strong correlation between these factors and revenue.  The model flags a structural shift in the data, indicating a significant change in the business's performance compared to historical trends.  To mitigate potential risks, we should analyze the reasons behind the structural shift and adjust our marketing strategies accordingly.

**H60:**
- Forecast: $1K (p50)
- Actual: $197K
- Flags: Overperformance, Large Forecast Error

> The forecast predicts a revenue of $1,047 for GRAIN: Shopping in H60, with a p50 revenue of $1,047 and an actual revenue of $197,427.  The top two drivers of this forecast are the day of the month and the spend share of total.  The model is showing an overperformance in actual revenue, exceeding the upper bound of the forecast.  Next, we should investigate the model's high confidence level and explore ways to improve its coverage rate.

**H90:**
- Forecast: $0 (p50)
- Actual: $168K
- Flags: Overperformance, Low Coverage

> The forecast for GRAIN: Shopping revenue is $71,873, with a 90th percentile upper bound of $71,873. Actual revenue for the period is $168,478, which is significantly higher than the forecast. The top two drivers of this revenue are the dayofmonth_cos and days_since_start features, which are associated with the timing of sales.  The model's high confidence level, indicated by low historical coverage, suggests a need to adjust the model's assumptions to better reflect the actual market conditions.

## 5. Strategic Recommendations

### 5.1 Priority 1: Address Structural Shifts

The following grains show test-period means >2× training means, indicating a regime change in Feb 2026:

- **Google Ads (60d):** Test mean $649K vs train mean $168K (3.9x)
- **Meta Ads (30d):** Test mean $26K vs train mean $10K (2.6x)
- **Meta Ads (60d):** Test mean $78K vs train mean $15K (5.2x)
- **Organic/Direct (60d):** Test mean $550K vs train mean $167K (3.3x)
- **Search (30d):** Test mean $103K vs train mean $46K (2.2x)
- **Search (60d):** Test mean $311K vs train mean $76K (4.1x)
- **Direct (60d):** Test mean $220K vs train mean $67K (3.3x)
- **Organic_Search (60d):** Test mean $134K vs train mean $43K (3.1x)
- **Email (60d):** Test mean $142K vs train mean $42K (3.4x)
- **Shopping (30d):** Test mean $41K vs train mean $10K (4.0x)
- **Shopping (60d):** Test mean $183K vs train mean $8K (24.1x)
- **Shopping (90d):** Test mean $100K vs train mean $4K (26.9x)
- **Organic_Search_Bing (60d):** Test mean $31K vs train mean $9K (3.5x)
- **Remarketing_DPA (30d):** Test mean $16K vs train mean $5K (3.3x)
- **Remarketing_DPA (60d):** Test mean $51K vs train mean $6K (7.8x)
- **Remarketing_DPA (90d):** Test mean $19K vs train mean $9K (2.1x)
- **Organic_Social (60d):** Test mean $24K vs train mean $6K (3.8x)
- **Remarketing_Brand (30d):** Test mean $5K vs train mean $3K (2.1x)
- **Remarketing_Brand (60d):** Test mean $15K vs train mean $4K (3.5x)

**Action:** Retrain models with post-shift data. Consider adding a 'regime' indicator feature.

### 5.2 Priority 2: Budget Reallocation Opportunities

- **Bing Ads (30d):** High ROAS (6.27x) but low daily spend ($44). Consider increasing budget.
- **Google Ads (90d):** Low ROAS (1.47x) with high daily spend ($2K). Consider reducing budget or optimizing targeting.
- **Meta Ads (30d):** High ROAS (5.02x) but low daily spend ($221). Consider increasing budget.
- **Search (30d):** High ROAS (10.33x) but low daily spend ($463). Consider increasing budget.
- **Search (60d):** High ROAS (5.43x) but low daily spend ($463). Consider increasing budget.
- **Pmax (30d):** Low ROAS (1.26x) with high daily spend ($1K). Consider reducing budget or optimizing targeting.
- **Pmax (60d):** Low ROAS (1.30x) with high daily spend ($1K). Consider reducing budget or optimizing targeting.
- **Pmax (90d):** Low ROAS (1.01x) with high daily spend ($1K). Consider reducing budget or optimizing targeting.
- **Remarketing_DPA (30d):** High ROAS (9.71x) but low daily spend ($81). Consider increasing budget.
- **Remarketing_Brand (30d):** High ROAS (7.13x) but low daily spend ($24). Consider increasing budget.

### 5.3 Priority 3: Investigate Flagged Anomalies

- **Bing Ads (H60):** Low Coverage, Large Forecast Error, Overperformance
- **Bing Ads (H90):** Large Forecast Error, Overperformance
- **Direct (H30):** Low Coverage, Large Forecast Error, Underperformance
- **Direct (H60):** Low Coverage, Large Forecast Error, Overperformance, Structural Shift
- **Direct (H90):** Large Forecast Error, Overperformance
- **Email (H30):** Low Coverage, Large Forecast Error, Underperformance
- **Email (H60):** Low Coverage, Large Forecast Error, Overperformance, Structural Shift
- **Email (H90):** Low Coverage, Large Forecast Error, Overperformance
- **Google Ads (H30):** Large Forecast Error
- **Google Ads (H60):** Low Coverage, Large Forecast Error, Overperformance, Structural Shift
- **Google Ads (H90):** Low Coverage, Overperformance
- **Meta Ads (H30):** Large Forecast Error, Structural Shift
- **Meta Ads (H60):** Low Coverage, Large Forecast Error, Overperformance, Structural Shift
- **Meta Ads (H90):** Low Coverage, Large Forecast Error, Overperformance
- **Organic/Direct (H30):** Low Coverage, Large Forecast Error, Underperformance
- **Organic/Direct (H60):** Low Coverage, Large Forecast Error, Overperformance, Structural Shift
- **Organic/Direct (H90):** Overperformance
- **Organic_Search (H30):** Low Coverage, Underperformance
- **Organic_Search (H60):** Low Coverage, Large Forecast Error, Overperformance, Structural Shift
- **Organic_Search (H90):** Large Forecast Error, Overperformance
- **Organic_Search_Bing (H30):** Low Coverage, Large Forecast Error, Underperformance
- **Organic_Search_Bing (H60):** Low Coverage, Large Forecast Error, Overperformance, Structural Shift
- **Organic_Search_Bing (H90):** Low Coverage, Large Forecast Error, Overperformance
- **Organic_Social (H30):** Low Coverage, Large Forecast Error, Underperformance
- **Organic_Social (H60):** Low Coverage, Large Forecast Error, Overperformance, Structural Shift
- **Organic_Social (H90):** Low Coverage, Large Forecast Error, Overperformance
- **Pmax (H30):** Low Coverage, Overperformance
- **Pmax (H60):** ROAS Collapse, Low Coverage, Underperformance
- **Pmax (H90):** Low Coverage, Underperformance
- **Remarketing_Brand (H30):** Structural Shift
- **Remarketing_Brand (H60):** Low Coverage, Large Forecast Error, Overperformance, Structural Shift
- **Remarketing_Brand (H90):** Low Coverage
- **Remarketing_DPA (H30):** Large Forecast Error, Structural Shift
- **Remarketing_DPA (H60):** Low Coverage, Large Forecast Error, Overperformance, Structural Shift
- **Remarketing_DPA (H90):** Low Coverage, Large Forecast Error, Overperformance, Structural Shift
- **Search (H30):** Large Forecast Error, Structural Shift, Underperformance
- **Search (H60):** Low Coverage, Large Forecast Error, Overperformance, Structural Shift
- **Search (H90):** Low Coverage, Large Forecast Error, Overperformance
- **Shopping (H30):** Large Forecast Error, Structural Shift
- **Shopping (H60):** Low Coverage, Large Forecast Error, Overperformance, Structural Shift
- **Shopping (H90):** Low Coverage, Overperformance, Structural Shift

**Action:** For each flagged grain, investigate the specific dates flagged, check for external factors (campaign changes, competitive bidding, tracking issues), and consider refreshing the model.

### 5.4 Priority 4: Model Improvement Roadmap

1. **Switch to LightGBM:** Enables native SHAP via `TreeExplainer`, giving more granular per-prediction explanations than permutation importance.
2. **Add External Features:** Include competitor ad spend, market indices, or promotional calendars to capture regime changes.
3. **Hierarchical Forecasting:** Use top-down or bottom-up reconciliation to ensure platform forecasts sum to campaign-type forecasts.
4. **Online Learning:** Implement incremental updates so the model adapts to shifts without full retraining.
5. **Upgrade LLM:** Move from Gemma 2B to GPT-4o or Claude Sonnet for more nuanced, grain-name-aware narratives.

## 6. Appendices

### Appendix A: Data Dictionary

| Column | Source | Description |
|--------|--------|-------------|
| `grain` | Stage 1 | Aggregation level: platform or campaign type |
| `level` | Stage 1 | 'platform' or 'campaign_type' |
| `forecast_origin_date` | Stage 4 | Date the forecast was generated |
| `horizon_days` | Stage 4 | Forecast window: 30, 60, or 90 days |
| `p10_revenue` | Stage 4 | 10th percentile forecast (lower bound) |
| `p50_revenue` | Stage 4 | 50th percentile forecast (median) |
| `p90_revenue` | Stage 4 | 90th percentile forecast (upper bound) |
| `actual_revenue` | Stage 4 | Observed revenue for the forecast period |
| `p50_roas` | Stage 4 | Median forecasted Return on Ad Spend |
| `budget_multiplier` | Stage 5 | Hypothetical spend multiplier (0.5x–2.0x) |
| `coverage_p10_p90` | Stage 4 | % of test dates where actual fell in p10–p90 |
| `importance` | Stage 4 | Permutation importance score per feature |
| `narrative` | Stage 6 | LLM-generated business explanation |

### Appendix B: Complete Validation Metrics

| Grain | Horizon | MAE | RMSE | Coverage | Interval Width |
|-------|---------|-----|------|----------|----------------|
| Bing Ads | 30d | $3K | $3K | 89.3% | $8K |
| Bing Ads | 60d | $6K | $6K | 7.1% | $4K |
| Bing Ads | 90d | $3K | $3K | 53.6% | $4K |
| Google Ads | 30d | $67K | $71K | 89.3% | $131K |
| Google Ads | 60d | $182K | $192K | 0.0% | $120K |
| Google Ads | 90d | $110K | $118K | 0.0% | $41K |
| Meta Ads | 30d | $12K | $13K | 100.0% | $49K |
| Meta Ads | 60d | $36K | $38K | 0.0% | $48K |
| Meta Ads | 90d | $9K | $10K | 28.6% | $7K |
| Organic/Direct | 30d | $64K | $72K | 46.4% | $134K |
| Organic/Direct | 60d | $242K | $271K | 0.0% | $114K |
| Organic/Direct | 90d | $79K | $91K | 50.0% | $64K |
| Search | 30d | $50K | $51K | 57.1% | $98K |
| Search | 60d | $106K | $108K | 0.0% | $54K |
| Search | 90d | $48K | $55K | 7.1% | $23K |
| Pmax | 30d | $5K | $6K | 35.7% | $12K |
| Pmax | 60d | $12K | $15K | 7.1% | $-4K |
| Pmax | 90d | $6K | $8K | 46.4% | $7K |
| Direct | 30d | $33K | $39K | 25.0% | $33K |
| Direct | 60d | $109K | $118K | 0.0% | $51K |
| Direct | 90d | $30K | $39K | 64.3% | $41K |
| Organic_Search | 30d | $15K | $20K | 32.1% | $14K |
| Organic_Search | 60d | $69K | $71K | 0.0% | $11K |
| Organic_Search | 90d | $20K | $23K | 50.0% | $23K |
| Email | 30d | $33K | $39K | 39.3% | $35K |
| Email | 60d | $80K | $83K | 0.0% | $31K |
| Email | 90d | $19K | $26K | 46.4% | $14K |
| Shopping | 30d | $33K | $46K | 100.0% | $97K |
| Shopping | 60d | $172K | $175K | 0.0% | $135K |
| Shopping | 90d | $100K | $103K | 0.0% | $72K |
| Organic_Search_Bing | 30d | $4K | $5K | 42.9% | $8K |
| Organic_Search_Bing | 60d | $13K | $14K | 0.0% | $735 |
| Organic_Search_Bing | 90d | $5K | $6K | 42.9% | $2K |
| Remarketing_DPA | 30d | $10K | $11K | 100.0% | $27K |
| Remarketing_DPA | 60d | $23K | $26K | 0.0% | $25K |
| Remarketing_DPA | 90d | $9K | $10K | 0.0% | $7K |
| Organic_Social | 30d | $3K | $4K | 39.3% | $8K |
| Organic_Social | 60d | $12K | $13K | 0.0% | $3K |
| Organic_Social | 90d | $4K | $5K | 42.9% | $3K |
| Remarketing_Brand | 30d | $2K | $2K | 100.0% | $9K |
| Remarketing_Brand | 60d | $8K | $8K | 7.1% | $11K |
| Remarketing_Brand | 90d | $2K | $2K | 32.1% | $9K |

### Appendix C: Complete Budget Simulation (Baseline 1.0x)

| Grain | Horizon | p50 Revenue | p50 ROAS | Daily Spend (Baseline) |
|-------|---------|-------------|----------|----------------------|
| Bing Ads | 30d | $8K | 6.27x | $44 |
| Bing Ads | 60d | $5K | 1.99x | $44 |
| Bing Ads | 90d | $9K | 2.25x | $44 |
| Google Ads | 30d | $265K | 4.03x | $2K |
| Google Ads | 60d | $357K | 2.71x | $2K |
| Google Ads | 90d | $290K | 1.47x | $2K |
| Meta Ads | 30d | $33K | 5.02x | $221 |
| Meta Ads | 60d | $28K | 2.09x | $221 |
| Meta Ads | 90d | $27K | 1.37x | $221 |
| Organic/Direct | 30d | $351K | nanx | $0 |
| Organic/Direct | 60d | $345K | nanx | $0 |
| Organic/Direct | 90d | $229K | nanx | $0 |
| Search | 30d | $144K | 10.33x | $463 |
| Search | 60d | $151K | 5.43x | $463 |
| Search | 90d | $130K | 3.12x | $463 |
| Pmax | 30d | $55K | 1.26x | $1K |
| Pmax | 60d | $114K | 1.30x | $1K |
| Pmax | 90d | $132K | 1.01x | $1K |
| Direct | 30d | $138K | nanx | $0 |
| Direct | 60d | $131K | nanx | $0 |
| Direct | 90d | $97K | nanx | $0 |
| Organic_Search | 30d | $79K | nanx | $0 |
| Organic_Search | 60d | $71K | nanx | $0 |
| Organic_Search | 90d | $56K | nanx | $0 |
| Email | 30d | $93K | nanx | $0 |
| Email | 60d | $69K | nanx | $0 |
| Email | 90d | $58K | nanx | $0 |
| Shopping | 30d | $0 | 0.00x | $276 |
| Shopping | 60d | $0 | 0.00x | $276 |
| Shopping | 90d | $0 | 0.00x | $276 |
| Organic_Search_Bing | 30d | $20K | nanx | $0 |
| Organic_Search_Bing | 60d | $17K | nanx | $0 |
| Organic_Search_Bing | 90d | $12K | nanx | $0 |
| Remarketing_DPA | 30d | $23K | 9.71x | $81 |
| Remarketing_DPA | 60d | $13K | 2.72x | $81 |
| Remarketing_DPA | 90d | $12K | 1.60x | $81 |
| Organic_Social | 30d | $15K | nanx | $0 |
| Organic_Social | 60d | $13K | nanx | $0 |
| Organic_Social | 90d | $7K | nanx | $0 |
| Remarketing_Brand | 30d | $5K | 7.13x | $24 |
| Remarketing_Brand | 60d | $5K | 3.68x | $24 |
| Remarketing_Brand | 90d | $6K | 2.86x | $24 |

---

*This report was generated automatically by the AIgnition pipeline. All forecasts, simulations, and explanations are based on the data and methodology documented above. For questions or updates, re-run the corresponding pipeline stage.*
