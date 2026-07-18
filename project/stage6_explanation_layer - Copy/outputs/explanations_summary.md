# Stage 6: AI-Generated Explanations Summary

Generated: 2026-06-28 19:30:32

Model: google/gemma-2-2b-it

---

## Bing Ads — H30

**Forecast:** $8,591 (p50) | **Range:** $0 – $7,426 (p10–p90)

**Actual:** $4,450 | **ROAS:** 3.54x

**Top Drivers:**
- dayofmonth_cos: 4.6191
- spend_lag_7: 1.7278
- spend_rolling_mean_30d: 1.0607

**Anomalies:**
- No Anomaly: No significant anomalies detected for this grain and horizon.

**Narrative:**

The forecast for Bing Ads revenue in the H30 horizon is projected to be $8,591, with a 6.84x return on ad spend. The top two drivers of this revenue are the day of the month and the spending trend over the past seven days.  There are no significant anomalies detected in this data.  We should analyze the day of the month and spending trends further to optimize campaign performance.

---

## Bing Ads — H60

**Forecast:** $6,673 (p50) | **Range:** $4,879 – $9,842 (p10–p90)

**Actual:** $14,182 | **ROAS:** 8.28x

**Top Drivers:**
- spend_rolling_mean_7d: 11.0297
- spend_rolling_mean_14d: 6.5521
- spend_lag_7: 1.9453

**Anomalies:**
- Overperformance: Actual revenue ($14,182) is ABOVE the p90 upper bound ($9,842).
- Large Forecast Error: Actual revenue deviates 113% from the p50 forecast.
- Low Coverage: Historical coverage rate is only 7.1%, meaning the model is often overconfident.

**Narrative:**

The forecast for Bing Ads revenue in H60 is $6,673, with a p50 of $6,673 and actual revenue of $14,182. The top two drivers of this revenue are the rolling average of spending over the past seven and fourteen days, which suggests a strong correlation with current spending patterns.  The model is showing an overperformance, with actual revenue exceeding the upper bound of the forecast.  Next, we should investigate the reasons behind the high actual revenue and explore ways to adjust the model's confidence level.

---

## Bing Ads — H90

**Forecast:** $5,507 (p50) | **Range:** $3,975 – $9,513 (p10–p90)

**Actual:** $10,412 | **ROAS:** 3.37x

**Top Drivers:**
- dayofmonth_sin: 39.7839
- spend: 34.5751
- spend_lag_1: 13.2812

**Anomalies:**
- Overperformance: Actual revenue ($10,412) is ABOVE the p90 upper bound ($9,513).
- Large Forecast Error: Actual revenue deviates 89% from the p50 forecast.

**Narrative:**

The forecast for Bing Ads revenue in H90 is $9,513, with a p50 of $5,507 and actual revenue of $10,412.  The top two drivers of this performance are the dayofmonth_sin feature and spending, both associated with higher revenue.  The actual revenue is above the p90 upper bound, suggesting a potential overperformance.  Next, we should investigate the specific factors driving this overperformance to understand the drivers of this unexpected result.

---

## Direct — H30

**Forecast:** $80,385 (p50) | **Range:** $97,594 – $118,910 (p10–p90)

**Actual:** $34,672 | **ROAS:** nanx

**Top Drivers:**
- dow_Monday: 4.7968
- dow_Thursday: 4.5012
- is_weekend: 3.7109

**Anomalies:**
- Underperformance: Actual revenue ($34,672) is BELOW the p10 lower bound ($97,594).
- Large Forecast Error: Actual revenue deviates 57% from the p50 forecast.
- Low Coverage: Historical coverage rate is only 25.0%, meaning the model is often overconfident.

**Narrative:**

The forecast predicts revenue of $80,385 with a p10 lower bound of $97,594, and the actual revenue is $34,672.  The top two drivers of revenue are the day of the week (Monday and Thursday) and whether it's a weekend.  The model is showing an underperformance compared to the p10 lower bound, and has a large forecast error.  Next, we should investigate the model's low coverage rate and explore ways to improve its accuracy.

---

## Direct — H60

**Forecast:** $103,831 (p50) | **Range:** $88,181 – $144,615 (p10–p90)

**Actual:** $253,311 | **ROAS:** nanx

**Top Drivers:**
- dayofmonth_sin: 291.9973
- dayofmonth_cos: 238.6900
- revenue_rolling_mean_30d: 76.7207

**Anomalies:**
- Overperformance: Actual revenue ($253,311) is ABOVE the p90 upper bound ($144,615).
- Large Forecast Error: Actual revenue deviates 144% from the p50 forecast.
- Low Coverage: Historical coverage rate is only 0.0%, meaning the model is often overconfident.

**Narrative:**

Our forecast predicts a revenue of $103,831 for the next period, with a p50 range of $88,181 to $144,615. The top two drivers of this forecast are the day of the month and the rolling 30-day revenue average.  The model is showing an overperformance in actual revenue, which is significantly higher than the upper bound of the forecast.  We should investigate the reasons for this overperformance to ensure accurate future projections.

---

## Direct — H90

**Forecast:** $81,048 (p50) | **Range:** $87,263 – $99,386 (p10–p90)

**Actual:** $174,504 | **ROAS:** nanx

**Top Drivers:**
- revenue_rolling_mean_14d: 589.0505
- dayofmonth_sin: 346.7471
- dow_Sunday: 25.8525

**Anomalies:**
- Overperformance: Actual revenue ($174,504) is ABOVE the p90 upper bound ($99,386).
- Large Forecast Error: Actual revenue deviates 115% from the p50 forecast.

**Narrative:**

Our forecast predicts revenue of $99,386 for the H90 period, with a median revenue of $81,048. The top two drivers of this forecast are a rolling revenue trend and the day of the month.  The actual revenue is significantly higher than the upper bound of our forecast, suggesting a potential overperformance.  We should investigate the factors driving this overperformance to ensure we are accurately forecasting future revenue.

---

## Email — H30

**Forecast:** $78,107 (p50) | **Range:** $48,153 – $83,807 (p10–p90)

**Actual:** $18,129 | **ROAS:** nanx

**Top Drivers:**
- revenue_rolling_mean_7d: 1343.8131
- revenue_rolling_mean_30d: 203.6467
- revenue_rolling_mean_14d: 47.8298

**Anomalies:**
- Underperformance: Actual revenue ($18,129) is BELOW the p10 lower bound ($48,153).
- Large Forecast Error: Actual revenue deviates 77% from the p50 forecast.
- Low Coverage: Historical coverage rate is only 39.3%, meaning the model is often overconfident.

**Narrative:**

The forecast predicts a revenue of $78,107 for the next period, with a p10 lower bound of $48,153.  The top two drivers of this forecast are a rolling 7-day revenue average and a rolling 30-day revenue average, both associated with strong revenue growth.  The actual revenue is below the p10 lower bound, indicating underperformance.  A next step should be to investigate the reasons for this underperformance and adjust the model accordingly.

---

## Email — H60

**Forecast:** $58,837 (p50) | **Range:** $50,321 – $83,231 (p10–p90)

**Actual:** $160,434 | **ROAS:** nanx

**Top Drivers:**
- revenue_rolling_mean_14d: 213.1537
- dayofmonth_cos: 166.2463
- dayofmonth_sin: 93.7334

**Anomalies:**
- Overperformance: Actual revenue ($160,434) is ABOVE the p90 upper bound ($83,231).
- Large Forecast Error: Actual revenue deviates 173% from the p50 forecast.
- Low Coverage: Historical coverage rate is only 0.0%, meaning the model is often overconfident.

**Narrative:**

The forecast predicts a revenue of $58,837 for the next period, with a 90th percentile revenue of $83,231.  The top two drivers of this forecast are a rolling revenue average and the day of the month.  The model is showing an overperformance in actual revenue, which is significantly higher than the upper bound of the forecast.  Next, we should investigate the model's high confidence level and explore ways to improve its accuracy.

---

## Email — H90

**Forecast:** $54,274 (p50) | **Range:** $51,897 – $58,302 (p10–p90)

**Actual:** $114,085 | **ROAS:** nanx

**Top Drivers:**
- revenue_rolling_mean_14d: 1156.2753
- dayofmonth_sin: 292.3340
- dow_Thursday: 4.1837

**Anomalies:**
- Overperformance: Actual revenue ($114,085) is ABOVE the p90 upper bound ($58,302).
- Large Forecast Error: Actual revenue deviates 110% from the p50 forecast.
- Low Coverage: Historical coverage rate is only 46.4%, meaning the model is often overconfident.

**Narrative:**

Our forecast predicts revenue of $54,274 for the H90 period, with an actual result of $114,085.  The top two drivers of this revenue are a rolling 14-day revenue average and the day of the month, suggesting these factors are influencing our performance.  The model is showing an overperformance, with actual revenue exceeding the upper bound of the forecast.  We should investigate the factors driving this high revenue and consider adjusting our marketing strategy accordingly.

---

## Google Ads — H30

**Forecast:** $224,412 (p50) | **Range:** $91,884 – $247,720 (p10–p90)

**Actual:** $97,569 | **ROAS:** 3.30x

**Top Drivers:**
- target_spend_30d: 23147.2793
- spend: 10166.5052
- spend_lag_7: 563.5485

**Anomalies:**
- Large Forecast Error: Actual revenue deviates 57% from the p50 forecast.

**Narrative:**

The forecast predicts $224,412 in revenue for GRAIN in H30, with a p50 of $224,412 and an actual revenue of $97,569. The top two drivers of this revenue are target spend over the past 30 days and overall spending, both associated with the campaign's performance.  The large forecast error, a deviation of 57% from the p50 forecast, suggests a need for further investigation.  A deeper analysis of the campaign's performance and spending patterns is recommended to understand the discrepancy and optimize future performance.

---

## Google Ads — H60

**Forecast:** $458,924 (p50) | **Range:** $361,059 – $510,545 (p10–p90)

**Actual:** $720,741 | **ROAS:** 1.45x

**Top Drivers:**
- target_spend_60d: 847.3730
- spend_rolling_mean_14d: 566.3081
- spend_rolling_mean_30d: 565.9928

**Anomalies:**
- Overperformance: Actual revenue ($720,741) is ABOVE the p90 upper bound ($510,545).
- Large Forecast Error: Actual revenue deviates 57% from the p50 forecast.
- Low Coverage: Historical coverage rate is only 0.0%, meaning the model is often overconfident.

**Narrative:**

The forecast for GRAIN revenue in H60 is $458,924, with a p50 of 0.93x and actual revenue of $720,741. The top two drivers of this forecast are target spend over the past 60 days and a rolling average of spend over the past 14 days.  The model is showing an overperformance, with actual revenue exceeding the p90 upper bound.  A next step is to investigate the model's high confidence level and potentially adjust the coverage rate.

---

## Google Ads — H90

**Forecast:** $421,230 (p50) | **Range:** $438,854 – $475,731 (p10–p90)

**Actual:** $545,828 | **ROAS:** 1.58x

**Top Drivers:**
- target_spend_90d: 16311.3157
- spend_rolling_mean_14d: 466.8965
- spend_lag_7: 184.7874

**Anomalies:**
- Overperformance: Actual revenue ($545,828) is ABOVE the p90 upper bound ($475,731).
- Low Coverage: Historical coverage rate is only 0.0%, meaning the model is often overconfident.

**Narrative:**

The forecast for GRAIN revenue in H90 is $475,731, with a p50 of $421,230 and actual revenue of $545,828. The top two drivers of this forecast are target spend over the past 90 days and a rolling average of spend over the past 14 days.  The model's high confidence level, indicated by low historical coverage, is associated with the overperformance of actual revenue.  A next step is to investigate the model's confidence level and explore strategies to improve coverage.

---

## Meta Ads — H30

**Forecast:** $26,953 (p50) | **Range:** $0 – $44,733 (p10–p90)

**Actual:** $8,657 | **ROAS:** 2.53x

**Top Drivers:**
- target_spend_30d: 2362.9765
- dayofmonth_sin: 34.4882
- spend_share_of_total: 18.0624

**Anomalies:**
- Large Forecast Error: Actual revenue deviates 68% from the p50 forecast.
- Structural Shift: Test-period mean is 2.6x the training mean, suggesting a regime change.

**Narrative:**

The forecast for Meta Ads revenue in H30 is $26,953, with a p50 of $26,953 and actual revenue of $8,657. The top two drivers of revenue are target spend over the past 30 days and the day of the month, suggesting that campaign targeting and timing are key factors.  The model indicates a structural shift in the data, meaning the performance is significantly different from historical trends.  To improve performance, we should analyze the impact of the structural shift and adjust our targeting strategy accordingly.

---

## Meta Ads — H60

**Forecast:** $48,397 (p50) | **Range:** $0 – $50,287 (p10–p90)

**Actual:** $94,563 | **ROAS:** 1.62x

**Top Drivers:**
- target_spend_60d: 89.0307
- spend_lag_7: 68.8765
- spend: 25.8471

**Anomalies:**
- Overperformance: Actual revenue ($94,563) is ABOVE the p90 upper bound ($50,287).
- Large Forecast Error: Actual revenue deviates 95% from the p50 forecast.
- Low Coverage: Historical coverage rate is only 0.0%, meaning the model is often overconfident.

**Narrative:**

The forecast for Meta Ads revenue in H60 is $48,397, with a p50 of $48,397 and actual revenue of $94,563. The top two drivers of this revenue are target spend over the past 60 days and spending in the previous period. The model is overconfident, with a historical coverage rate of 0.0%.  We should investigate the high actual revenue and consider adjusting the model's targeting strategy.

---

## Meta Ads — H90

**Forecast:** $30,179 (p50) | **Range:** $28,662 – $42,033 (p10–p90)

**Actual:** $49,772 | **ROAS:** 1.63x

**Top Drivers:**
- target_spend_90d: 3638.4764
- spend_rolling_mean_14d: 128.3193
- revenue_rolling_mean_30d: 101.7045

**Anomalies:**
- Overperformance: Actual revenue ($49,772) is ABOVE the p90 upper bound ($42,033).
- Large Forecast Error: Actual revenue deviates 65% from the p50 forecast.
- Low Coverage: Historical coverage rate is only 28.6%, meaning the model is often overconfident.

**Narrative:**

The forecast for GRAIN: Meta Ads revenue in H90 is $30,179, with a p50 of $30,179 and actual revenue of $49,772. The top two drivers of this forecast are target spend over the past 90 days and a rolling average of spend over the past 14 days.  The model is showing an overperformance in revenue, exceeding the upper bound of the forecast.  A next step is to investigate the high actual revenue and its drivers to understand the potential for future performance.

---

## Organic/Direct — H30

**Forecast:** $192,849 (p50) | **Range:** $206,354 – $330,569 (p10–p90)

**Actual:** $83,452 | **ROAS:** nanx

**Top Drivers:**
- revenue_rolling_mean_7d: 134.1416
- dow_Sunday: 16.5076
- dow_Thursday: 4.5456

**Anomalies:**
- Underperformance: Actual revenue ($83,452) is BELOW the p10 lower bound ($206,354).
- Large Forecast Error: Actual revenue deviates 57% from the p50 forecast.
- Low Coverage: Historical coverage rate is only 46.4%, meaning the model is often overconfident.

**Narrative:**

The forecast predicts revenue of $192,849 for the H30 horizon, with a p50 of $192,849.  The top two drivers of revenue are a rolling seven-day average and Sunday's Dow Jones performance.  The model's actual performance is below the p10 lower bound, suggesting potential underperformance.  A deeper dive into the model's confidence levels and historical data is recommended to understand the discrepancy.

---

## Organic/Direct — H60

**Forecast:** $283,493 (p50) | **Range:** $223,573 – $338,648 (p10–p90)

**Actual:** $627,351 | **ROAS:** nanx

**Top Drivers:**
- dayofmonth_sin: 596.2959
- revenue_rolling_mean_30d: 116.2153
- is_weekend: 28.6277

**Anomalies:**
- Overperformance: Actual revenue ($627,351) is ABOVE the p90 upper bound ($338,648).
- Large Forecast Error: Actual revenue deviates 121% from the p50 forecast.
- Low Coverage: Historical coverage rate is only 0.0%, meaning the model is often overconfident.

**Narrative:**

The forecast predicts revenue of $283,493 for the H60 period, with a p50 of $283,493 and actual revenue of $627,351. The top drivers for this forecast are the day of the month and a rolling 30-day revenue average. The model is associated with a high level of overconfidence, as indicated by its low coverage rate.  A next step is to investigate the model's high confidence and explore potential adjustments to improve its accuracy.

---

## Organic/Direct — H90

**Forecast:** $345,358 (p50) | **Range:** $202,292 – $208,342 (p10–p90)

**Actual:** $445,041 | **ROAS:** nanx

**Top Drivers:**
- revenue_rolling_mean_14d: 3345.8194
- dayofmonth_sin: 713.7485
- dayofmonth_cos: 486.7603

**Anomalies:**
- Overperformance: Actual revenue ($445,041) is ABOVE the p90 upper bound ($208,342).

**Narrative:**

The forecast predicts revenue of $345,358 for the H90 period, with a p90 upper bound of $208,342.  The top two drivers of revenue are a rolling 14-day average and the day of the month, suggesting these factors are associated with sales performance.  The actual revenue is above the p90 upper bound, indicating potential overperformance.  To mitigate this, we should investigate the factors driving the high revenue and consider adjusting our marketing strategies accordingly.

---

## Organic_Search — H30

**Forecast:** $33,050 (p50) | **Range:** $50,091 – $63,877 (p10–p90)

**Actual:** $22,827 | **ROAS:** nanx

**Top Drivers:**
- revenue_rolling_mean_14d: 412.7856
- revenue_rolling_mean_30d: 170.3582
- dow_Thursday: 40.3678

**Anomalies:**
- Underperformance: Actual revenue ($22,827) is BELOW the p10 lower bound ($50,091).
- Low Coverage: Historical coverage rate is only 32.1%, meaning the model is often overconfident.

**Narrative:**

The forecast for revenue in the H30 horizon is projected to be $33,050, with a p10 lower bound of $50,091.  The top two drivers of revenue are a rolling 14-day average and a rolling 30-day average, suggesting that these metrics are closely linked to actual sales performance.  The model is showing an underperformance, as actual revenue is below the p10 lower bound.  To improve performance, we should investigate the reasons behind the low coverage rate and explore strategies to increase the model's accuracy.

---

## Organic_Search — H60

**Forecast:** $67,509 (p50) | **Range:** $60,310 – $74,875 (p10–p90)

**Actual:** $151,252 | **ROAS:** nanx

**Top Drivers:**
- dayofmonth_sin: 155.5678
- revenue_rolling_mean_30d: 55.1201
- dayofmonth_cos: 18.3580

**Anomalies:**
- Overperformance: Actual revenue ($151,252) is ABOVE the p90 upper bound ($74,875).
- Large Forecast Error: Actual revenue deviates 124% from the p50 forecast.
- Low Coverage: Historical coverage rate is only 0.0%, meaning the model is often overconfident.

**Narrative:**

The forecast for revenue in the H60 horizon is $67,509, with a p50 range of $60,310 to $74,875. The top two drivers of this forecast are the dayofmonth_sin and revenue_rolling_mean_30d, which suggest that the model is influenced by the day of the month and the previous 30-day revenue performance.  The model is flagged for overperformance, as actual revenue is significantly higher than the p90 upper bound.  To improve accuracy, we should investigate the reasons behind the high actual revenue and consider adjusting the model's confidence level.

---

## Organic_Search — H90

**Forecast:** $63,950 (p50) | **Range:** $54,992 – $84,214 (p10–p90)

**Actual:** $113,401 | **ROAS:** nanx

**Top Drivers:**
- revenue_rolling_mean_14d: 1727.4537
- revenue_rolling_mean_7d: 313.8325
- dayofmonth_sin: 308.9823

**Anomalies:**
- Overperformance: Actual revenue ($113,401) is ABOVE the p90 upper bound ($84,214).
- Large Forecast Error: Actual revenue deviates 77% from the p50 forecast.

**Narrative:**

Our forecast predicts revenue of $63,950 for the next 90 days, with a range of $54,992 to $84,214.  The top two drivers of this forecast are a rolling 14-day revenue average and a rolling 7-day revenue average, both associated with strong sales performance.  The actual revenue is above the upper bound of our forecast, suggesting a potential overperformance.  We should investigate the factors driving this overperformance to ensure we are accurately forecasting future revenue.

---

## Organic_Search_Bing — H30

**Forecast:** $10,003 (p50) | **Range:** $11,557 – $19,235 (p10–p90)

**Actual:** $4,798 | **ROAS:** nanx

**Top Drivers:**
- dow_Sunday: 1.9605
- dow_Saturday: 0.9055
- dow_Thursday: 0.2129

**Anomalies:**
- Underperformance: Actual revenue ($4,798) is BELOW the p10 lower bound ($11,557).
- Large Forecast Error: Actual revenue deviates 52% from the p50 forecast.
- Low Coverage: Historical coverage rate is only 42.9%, meaning the model is often overconfident.

**Narrative:**

The forecast for revenue in the H30 horizon is $10,003 with a p50 range of $11,557 to $19,235.  The top two drivers of this forecast are Sunday and Saturday, suggesting these days are most influential in driving revenue.  The model's actual revenue is below the p10 lower bound, indicating underperformance.  To improve performance, we should investigate the reasons behind the low coverage rate and explore ways to increase the model's accuracy.

---

## Organic_Search_Bing — H60

**Forecast:** $16,723 (p50) | **Range:** $16,493 – $16,920 (p10–p90)

**Actual:** $34,387 | **ROAS:** nanx

**Top Drivers:**
- dayofmonth_cos: 31.9523
- dow_Sunday: 1.0874
- is_weekend: 0.7490

**Anomalies:**
- Overperformance: Actual revenue ($34,387) is ABOVE the p90 upper bound ($16,920).
- Large Forecast Error: Actual revenue deviates 106% from the p50 forecast.
- Low Coverage: Historical coverage rate is only 0.0%, meaning the model is often overconfident.

**Narrative:**

The forecast predicts revenue of $16,723 for the H60 period, with a 90th percentile revenue of $16,920 and a 50th percentile revenue of $16,493. The top two drivers of this forecast are the day of the month and the day of the week, suggesting that the model is influenced by specific days of the week and month. The model is overconfident, with a historical coverage rate of 0%, which may contribute to the large forecast error.  To improve accuracy, we should investigate the model's assumptions and potentially adjust the model's parameters.

---

## Organic_Search_Bing — H90

**Forecast:** $11,344 (p50) | **Range:** $11,587 – $13,295 (p10–p90)

**Actual:** $24,159 | **ROAS:** nanx

**Top Drivers:**
- dayofmonth_sin: 83.7190
- dayofmonth_cos: 46.1973
- revenue_rolling_mean_30d: 12.8174

**Anomalies:**
- Overperformance: Actual revenue ($24,159) is ABOVE the p90 upper bound ($13,295).
- Large Forecast Error: Actual revenue deviates 113% from the p50 forecast.
- Low Coverage: Historical coverage rate is only 42.9%, meaning the model is often overconfident.

**Narrative:**

Our forecast predicts revenue of $13,295 for the next 90 days, with a p50 of $11,344.  The top two drivers of this forecast are the dayofmonth_sin and dayofmonth_cos, which suggest the model is influenced by the day of the month.  The model is showing an overperformance in actual revenue, exceeding the upper bound of the forecast.  We should investigate the reasons behind this overperformance and adjust the model's parameters accordingly.

---

## Organic_Social — H30

**Forecast:** $7,590 (p50) | **Range:** $9,534 – $16,775 (p10–p90)

**Actual:** $3,026 | **ROAS:** nanx

**Top Drivers:**
- revenue_rolling_mean_7d: 24.3723
- dow_Thursday: 0.7939
- spend_lag_7: 0.0000

**Anomalies:**
- Underperformance: Actual revenue ($3,026) is BELOW the p10 lower bound ($9,534).
- Large Forecast Error: Actual revenue deviates 60% from the p50 forecast.
- Low Coverage: Historical coverage rate is only 39.3%, meaning the model is often overconfident.

**Narrative:**

The forecast predicts organic social revenue to be $7,590 with a p50 range of $9,534 to $16,775 by 2026-02-28.  The top drivers of this forecast are a rolling seven-day revenue average and the Thursday Dow Jones index.  The model's low coverage rate suggests it may be overconfident in its predictions.  Next, we should investigate the factors driving the significant revenue underperformance compared to the p10 lower bound.

---

## Organic_Social — H60

**Forecast:** $11,222 (p50) | **Range:** $6,975 – $12,315 (p10–p90)

**Actual:** $27,968 | **ROAS:** nanx

**Top Drivers:**
- revenue_rolling_mean_14d: 102.3170
- dayofmonth_cos: 43.1585
- revenue_rolling_mean_7d: 18.6323

**Anomalies:**
- Overperformance: Actual revenue ($27,968) is ABOVE the p90 upper bound ($12,315).
- Large Forecast Error: Actual revenue deviates 149% from the p50 forecast.
- Low Coverage: Historical coverage rate is only 0.0%, meaning the model is often overconfident.

**Narrative:**

The forecast for organic social revenue in H60 is $11,222, with a p50 of $11,222 and actual revenue of $27,968.  The top two drivers of this revenue are a rolling 14-day revenue average and the day of the month, suggesting that consistent revenue growth and the day of the month may be influencing performance.  The model is showing an overperformance, with actual revenue exceeding the upper bound of the forecast.  The next step should be to investigate the reasons for the high actual revenue and explore ways to improve the model's accuracy.

---

## Organic_Social — H90

**Forecast:** $7,070 (p50) | **Range:** $6,254 – $6,559 (p10–p90)

**Actual:** $18,893 | **ROAS:** nanx

**Top Drivers:**
- dayofmonth_sin: 19.4673
- dayofmonth_cos: 6.2487
- is_weekend: 1.3143

**Anomalies:**
- Overperformance: Actual revenue ($18,893) is ABOVE the p90 upper bound ($6,559).
- Large Forecast Error: Actual revenue deviates 167% from the p50 forecast.
- Low Coverage: Historical coverage rate is only 42.9%, meaning the model is often overconfident.

**Narrative:**

Our forecast predicts organic social revenue to be $7,070 in 2026, with a p90 upper bound of $6,559. The top drivers of this forecast are the dayofmonth sine and cosine values, which suggest the model is influenced by the day of the month.  The model is also associated with an overperformance in actual revenue, which deviates significantly from the forecast.  We should investigate the reasons for this overperformance and consider adjusting the model's confidence level.

---

## Pmax — H30

**Forecast:** $27,926 (p50) | **Range:** $26,282 – $32,691 (p10–p90)

**Actual:** $36,308 | **ROAS:** 1.96x

**Top Drivers:**
- target_spend_30d: 10439.7730
- spend: 780.6661
- spend_share_of_total: 118.0264

**Anomalies:**
- Overperformance: Actual revenue ($36,308) is ABOVE the p90 upper bound ($32,691).
- Low Coverage: Historical coverage rate is only 35.7%, meaning the model is often overconfident.

**Narrative:**

The forecast predicts revenue of $27,926 with a 1.51x ROAS, based on the latest data. The top two drivers of this forecast are the target spend over the past 30 days and the overall spend, suggesting a strong correlation with campaign performance.  The model is showing an overperformance in actual revenue, exceeding the upper bound of the forecast.  To mitigate this, we should analyze the model's confidence and adjust the target spend accordingly.

---

## Pmax — H60

**Forecast:** $151,731 (p50) | **Range:** $193,122 – $170,355 (p10–p90)

**Actual:** $177,932 | **ROAS:** 0.92x

**Top Drivers:**
- target_spend_60d: 10512.7185
- spend_lag_1: 149.1714
- spend_rolling_mean_14d: 107.1611

**Anomalies:**
- Underperformance: Actual revenue ($177,932) is BELOW the p10 lower bound ($193,122).
- ROAS Collapse: Actual ROAS is 0.92x, below the 1.0x breakeven threshold.
- Low Coverage: Historical coverage rate is only 7.1%, meaning the model is often overconfident.

**Narrative:**

Our forecast predicts revenue of $151,731 for the next 60 days, with a p10 lower bound of $193,122. The top two drivers of this forecast are a high target spend and a historical spend lag.  The model's actual performance is below the p10 lower bound, and its ROAS is below the breakeven threshold.  We should investigate the model's high confidence level and explore ways to improve coverage.

---

## Pmax — H90

**Forecast:** $140,389 (p50) | **Range:** $132,795 – $139,610 (p10–p90)

**Actual:** $130,916 | **ROAS:** 1.01x

**Top Drivers:**
- target_spend_90d: 11422.4238
- spend_lag_7: 146.7154
- spend_share_of_total: 71.7701

**Anomalies:**
- Underperformance: Actual revenue ($130,916) is BELOW the p10 lower bound ($132,795).
- Low Coverage: Historical coverage rate is only 46.4%, meaning the model is often overconfident.

**Narrative:**

Our forecast predicts a revenue of $140,389 for the next 90 days, with a p50 ROAS of 1.09x. The top two drivers of this forecast are a high target spend for the past 90 days and a historical spend share of 71.77%.  The model is currently showing underperformance, as actual revenue is below the p10 lower bound.  We should investigate the reasons for this underperformance and adjust the campaign strategy accordingly.

---

## Remarketing_Brand — H30

**Forecast:** $4,605 (p50) | **Range:** $0 – $7,943 (p10–p90)

**Actual:** $3,200 | **ROAS:** 5.30x

**Top Drivers:**
- target_spend_30d: 304.1698
- dayofmonth_sin: 14.2307
- dayofmonth_cos: 9.3886

**Anomalies:**
- Structural Shift: Test-period mean is 2.1x the training mean, suggesting a regime change.

**Narrative:**

The forecast predicts a revenue of $4,605 for the Remarketing_Brand campaign in H30, with a median revenue of $4,605 and a range from $0 to $7,943. The top two drivers of this forecast are the target spend over the past 30 days and the day of the month, suggesting that campaign spending and the timing of the campaign are important factors.  The structural shift in the test period, where the mean is 2.1 times the training mean, suggests a significant change in the campaign's performance.  A deeper dive into the campaign's performance, particularly the day of the month, is recommended to understand the drivers of the observed change.

---

## Remarketing_Brand — H60

**Forecast:** $7,172 (p50) | **Range:** $0 – $10,443 (p10–p90)

**Actual:** $16,845 | **ROAS:** 2.54x

**Top Drivers:**
- revenue_rolling_mean_30d: 1.9259
- revenue_rolling_mean_14d: 1.9177
- dayofmonth_sin: 1.0563

**Anomalies:**
- Overperformance: Actual revenue ($16,845) is ABOVE the p90 upper bound ($10,443).
- Large Forecast Error: Actual revenue deviates 135% from the p50 forecast.
- Low Coverage: Historical coverage rate is only 7.1%, meaning the model is often overconfident.

**Narrative:**

The forecast predicts a revenue of $7,172 for the next period, with a 90th percentile upper bound of $10,443.  The top two drivers of this forecast are a rolling 30-day revenue trend and a rolling 14-day revenue trend, both associated with positive revenue growth.  The model is showing an overperformance in actual revenue, exceeding the upper bound of the forecast.  A deeper dive into the model's confidence and potential reasons for the high revenue is recommended.

---

## Remarketing_Brand — H90

**Forecast:** $8,913 (p50) | **Range:** $0 – $15,279 (p10–p90)

**Actual:** $11,271 | **ROAS:** 2.58x

**Top Drivers:**
- target_spend_90d: 436.7683
- revenue_rolling_mean_30d: 43.5942
- spend_lag_14: 8.3306

**Anomalies:**
- Low Coverage: Historical coverage rate is only 32.1%, meaning the model is often overconfident.

**Narrative:**

The forecast predicts a revenue of $8,913 for the next 90 days, with a 90th percentile revenue of $15,279 and a median revenue of $8,913.  The top two drivers of this forecast are the target spend over the past 90 days and the rolling average revenue over the past 30 days.  The model's high confidence level, associated with low historical coverage, is a potential concern.  To improve accuracy, we should investigate the historical coverage rate and explore ways to increase data points for the model.

---

## Remarketing_DPA — H30

**Forecast:** $17,882 (p50) | **Range:** $0 – $20,518 (p10–p90)

**Actual:** $3,521 | **ROAS:** 3.96x

**Top Drivers:**
- target_spend_30d: 2479.1800
- dayofmonth_sin: 19.9358
- dow_Monday: 0.4878

**Anomalies:**
- Large Forecast Error: Actual revenue deviates 80% from the p50 forecast.
- Structural Shift: Test-period mean is 3.3x the training mean, suggesting a regime change.

**Narrative:**

The forecast for Remarketing_DPA revenue in H30 is $17,882 with a 90% confidence interval of $20,518. Actual revenue for this period is $3,521, resulting in a significant revenue shortfall. The top two drivers of this performance are the target spend over the past 30 days and the day of the month, suggesting a strong correlation with campaign timing.  The large forecast error, indicating a significant deviation from the predicted revenue, warrants further investigation.  A deeper analysis of the campaign's performance and its drivers is needed to understand the discrepancy and optimize future performance.

---

## Remarketing_DPA — H60

**Forecast:** $27,970 (p50) | **Range:** $5,363 – $28,091 (p10–p90)

**Actual:** $62,387 | **ROAS:** 2.52x

**Top Drivers:**
- spend_lag_14: 8.5084
- target_spend_60d: 4.9209
- revenue_rolling_mean_14d: 0.3345

**Anomalies:**
- Overperformance: Actual revenue ($62,387) is ABOVE the p90 upper bound ($28,091).
- Large Forecast Error: Actual revenue deviates 123% from the p50 forecast.
- Low Coverage: Historical coverage rate is only 0.0%, meaning the model is often overconfident.

**Narrative:**

The forecast for Remarketing_DPA revenue in H60 is $27,970, with a p50 revenue of $27,970 and actual revenue of $62,387.  The top two drivers of this revenue are a lag in spending and a targeted spend over the past 60 days.  The model is showing an anomaly with a high actual revenue exceeding the upper bound of the forecast.  The next step is to investigate the high actual revenue and assess if adjustments to the model's targeting or spend strategy are needed.

---

## Remarketing_DPA — H90

**Forecast:** $12,271 (p50) | **Range:** $7,729 – $24,136 (p10–p90)

**Actual:** $30,368 | **ROAS:** 2.31x

**Top Drivers:**
- target_spend_90d: 737.6700
- spend: 159.4017
- revenue_rolling_mean_14d: 3.2988

**Anomalies:**
- Overperformance: Actual revenue ($30,368) is ABOVE the p90 upper bound ($24,136).
- Large Forecast Error: Actual revenue deviates 147% from the p50 forecast.
- Low Coverage: Historical coverage rate is only 0.0%, meaning the model is often overconfident.

**Narrative:**

The forecast for Remarketing_DPA revenue in the next 90 days is $12,271, with a p50 of $12,271 and an actual revenue of $30,368. The top two drivers of this revenue are target spend over the past 90 days and overall spending, both associated with higher revenue.  The model is showing an overperformance in actual revenue, which is 147% above the p50 forecast.  To mitigate this, we should analyze the model's confidence and adjust the target spend accordingly.

---

## Search — H30

**Forecast:** $119,340 (p50) | **Range:** $59,652 – $188,612 (p10–p90)

**Actual:** $50,657 | **ROAS:** 7.34x

**Top Drivers:**
- target_spend_30d: 12059.9996
- spend: 1729.1003
- spend_lag_1: 114.4959

**Anomalies:**
- Underperformance: Actual revenue ($50,657) is BELOW the p10 lower bound ($59,652).
- Large Forecast Error: Actual revenue deviates 58% from the p50 forecast.
- Structural Shift: Test-period mean is 2.2x the training mean, suggesting a regime change.

**Narrative:**

The forecast predicts a revenue of $119,340 for GRAIN: Search in H30, with a p50 of $119,340 and an actual revenue of $50,657.  The top two drivers of revenue are target spend over the past 30 days and overall spending.  The actual revenue is below the p10 lower bound, suggesting underperformance.  Next, we should investigate the reasons behind the structural shift in the test period to understand the potential impact on future performance.

---

## Search — H60

**Forecast:** $220,645 (p50) | **Range:** $166,450 – $220,279 (p10–p90)

**Actual:** $349,072 | **ROAS:** 3.44x

**Top Drivers:**
- target_spend_60d: 712.5561
- spend_lag_1: 267.0344
- spend_rolling_mean_7d: 225.6485

**Anomalies:**
- Overperformance: Actual revenue ($349,072) is ABOVE the p90 upper bound ($220,279).
- Large Forecast Error: Actual revenue deviates 58% from the p50 forecast.
- Low Coverage: Historical coverage rate is only 0.0%, meaning the model is often overconfident.

**Narrative:**

The forecast for GRAIN: Search revenue in H60 is $220,645, with a p50 ROAS of 2.17x. The top two drivers of this forecast are target spend over the past 60 days and spending in the previous period. The model is showing an overperformance in revenue, exceeding the p90 upper bound by 58%.  Next, we should investigate the historical coverage rate to understand why the model is so confident.

---

## Search — H90

**Forecast:** $158,876 (p50) | **Range:** $145,935 – $163,876 (p10–p90)

**Actual:** $243,548 | **ROAS:** 4.58x

**Top Drivers:**
- target_spend_90d: 657.2509
- spend_lag_1: 135.6816
- spend_rolling_mean_7d: 53.9517

**Anomalies:**
- Overperformance: Actual revenue ($243,548) is ABOVE the p90 upper bound ($163,876).
- Large Forecast Error: Actual revenue deviates 53% from the p50 forecast.
- Low Coverage: Historical coverage rate is only 7.1%, meaning the model is often overconfident.

**Narrative:**

The forecast for GRAIN revenue in H90 is $163,876, with actual revenue reaching $243,548. The top two drivers of this performance are the target spend over the past 90 days and spending trends from the previous period.  The model's high confidence level, indicated by its low coverage rate, suggests potential overconfidence.  A next step is to investigate the model's confidence levels and explore potential adjustments to the target spend strategy.

---

## Shopping — H30

**Forecast:** $3,560 (p50) | **Range:** $0 – $78,956 (p10–p90)

**Actual:** $12,204 | **ROAS:** 3.38x

**Top Drivers:**
- target_spend_30d: 784.7189
- spend: 617.9534
- dayofmonth_cos: 85.5679

**Anomalies:**
- Large Forecast Error: Actual revenue deviates 243% from the p50 forecast.
- Structural Shift: Test-period mean is 4.0x the training mean, suggesting a regime change.

**Narrative:**

The forecast predicts a revenue of $3,560 for GRAIN: Shopping in H30, with a median revenue of $3,560 and a p50 ROAS of 0.99x. The top two drivers of revenue are target spend over the past 30 days and overall spending, suggesting a strong correlation between these factors and revenue.  The model flags a structural shift in the data, indicating a significant change in the business's performance compared to historical trends.  To mitigate potential risks, we should analyze the reasons behind the structural shift and adjust our marketing strategies accordingly.

---

## Shopping — H60

**Forecast:** $1,047 (p50) | **Range:** $0 – $138,575 (p10–p90)

**Actual:** $197,427 | **ROAS:** 1.10x

**Top Drivers:**
- dayofmonth_sin: 2.9780
- spend_share_of_total: 1.8403
- dayofmonth_cos: 0.5661

**Anomalies:**
- Overperformance: Actual revenue ($197,427) is ABOVE the p90 upper bound ($138,575).
- Large Forecast Error: Actual revenue deviates 18754% from the p50 forecast.
- Low Coverage: Historical coverage rate is only 0.0%, meaning the model is often overconfident.

**Narrative:**

The forecast predicts a revenue of $1,047 for GRAIN: Shopping in H60, with a p50 revenue of $1,047 and an actual revenue of $197,427.  The top two drivers of this forecast are the day of the month and the spend share of total.  The model is showing an overperformance in actual revenue, exceeding the upper bound of the forecast.  Next, we should investigate the model's high confidence level and explore ways to improve its coverage rate.

---

## Shopping — H90

**Forecast:** $0 (p50) | **Range:** $0 – $71,873 (p10–p90)

**Actual:** $168,478 | **ROAS:** 1.15x

**Top Drivers:**
- dayofmonth_cos: 0.0000
- dayofmonth_sin: 0.0000
- days_since_start: 0.0000

**Anomalies:**
- Overperformance: Actual revenue ($168,478) is ABOVE the p90 upper bound ($71,873).
- Low Coverage: Historical coverage rate is only 0.0%, meaning the model is often overconfident.
- Structural Shift: Test-period mean is 26.9x the training mean, suggesting a regime change.

**Narrative:**

The forecast for GRAIN: Shopping revenue is $71,873, with a 90th percentile upper bound of $71,873. Actual revenue for the period is $168,478, which is significantly higher than the forecast. The top two drivers of this revenue are the dayofmonth_cos and days_since_start features, which are associated with the timing of sales.  The model's high confidence level, indicated by low historical coverage, suggests a need to adjust the model's assumptions to better reflect the actual market conditions.

---

