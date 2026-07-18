# Stage 9: Recommendations Engine
## Automated Recommendations from AIgnition Pipeline

**Generated:** 2026-06-28 20:04  
**Total Recommendations:** 94  
**Rule Engine:** 7 business rules applied across 42 grain/horizon combinations

---

## Priority Summary

| Priority | Category | Count |
|----------|----------|-------|
| P1: Urgent | — | 20 |
| P2: High | — | 63 |
| P3: Medium | — | 10 |
| P4: Strategic | — | 1 |

| Category | Count |
|----------|-------|
| Investigation | 32 |
| Model Calibration | 31 |
| Model Risk | 19 |
| Budget Optimization | 10 |
| Urgent Alert | 1 |
| Strategic | 1 |

---

## Detailed Recommendations

### 1. [Urgent] Retrain model for Direct (H60)

**Category:** Model Risk  
**Grain:** Direct | **Horizon:** H60  
**Confidence:** High | **Effort:** Medium (2–3 days to retrain with post-shift data)

**Description:** Test-period mean (3.3x training mean) indicates a structural shift. Current model is miscalibrated.

**Expected Impact:** Improved forecast accuracy by capturing new regime patterns.

**Action:** Collect post-Feb 2026 data, add regime indicator feature, retrain HistGradientBoostingRegressor.

---

### 2. [Urgent] Retrain model for Email (H60)

**Category:** Model Risk  
**Grain:** Email | **Horizon:** H60  
**Confidence:** High | **Effort:** Medium (2–3 days to retrain with post-shift data)

**Description:** Test-period mean (3.4x training mean) indicates a structural shift. Current model is miscalibrated.

**Expected Impact:** Improved forecast accuracy by capturing new regime patterns.

**Action:** Collect post-Feb 2026 data, add regime indicator feature, retrain HistGradientBoostingRegressor.

---

### 3. [Urgent] Retrain model for Google Ads (H60)

**Category:** Model Risk  
**Grain:** Google Ads | **Horizon:** H60  
**Confidence:** High | **Effort:** Medium (2–3 days to retrain with post-shift data)

**Description:** Test-period mean (3.9x training mean) indicates a structural shift. Current model is miscalibrated.

**Expected Impact:** Improved forecast accuracy by capturing new regime patterns.

**Action:** Collect post-Feb 2026 data, add regime indicator feature, retrain HistGradientBoostingRegressor.

---

### 4. [Urgent] Retrain model for Meta Ads (H30)

**Category:** Model Risk  
**Grain:** Meta Ads | **Horizon:** H30  
**Confidence:** High | **Effort:** Medium (2–3 days to retrain with post-shift data)

**Description:** Test-period mean (2.6x training mean) indicates a structural shift. Current model is miscalibrated.

**Expected Impact:** Improved forecast accuracy by capturing new regime patterns.

**Action:** Collect post-Feb 2026 data, add regime indicator feature, retrain HistGradientBoostingRegressor.

---

### 5. [Urgent] Retrain model for Meta Ads (H60)

**Category:** Model Risk  
**Grain:** Meta Ads | **Horizon:** H60  
**Confidence:** High | **Effort:** Medium (2–3 days to retrain with post-shift data)

**Description:** Test-period mean (5.2x training mean) indicates a structural shift. Current model is miscalibrated.

**Expected Impact:** Improved forecast accuracy by capturing new regime patterns.

**Action:** Collect post-Feb 2026 data, add regime indicator feature, retrain HistGradientBoostingRegressor.

---

### 6. [Urgent] Retrain model for Organic/Direct (H60)

**Category:** Model Risk  
**Grain:** Organic/Direct | **Horizon:** H60  
**Confidence:** High | **Effort:** Medium (2–3 days to retrain with post-shift data)

**Description:** Test-period mean (3.3x training mean) indicates a structural shift. Current model is miscalibrated.

**Expected Impact:** Improved forecast accuracy by capturing new regime patterns.

**Action:** Collect post-Feb 2026 data, add regime indicator feature, retrain HistGradientBoostingRegressor.

---

### 7. [Urgent] Retrain model for Organic_Search (H60)

**Category:** Model Risk  
**Grain:** Organic_Search | **Horizon:** H60  
**Confidence:** High | **Effort:** Medium (2–3 days to retrain with post-shift data)

**Description:** Test-period mean (3.1x training mean) indicates a structural shift. Current model is miscalibrated.

**Expected Impact:** Improved forecast accuracy by capturing new regime patterns.

**Action:** Collect post-Feb 2026 data, add regime indicator feature, retrain HistGradientBoostingRegressor.

---

### 8. [Urgent] Retrain model for Organic_Search_Bing (H60)

**Category:** Model Risk  
**Grain:** Organic_Search_Bing | **Horizon:** H60  
**Confidence:** High | **Effort:** Medium (2–3 days to retrain with post-shift data)

**Description:** Test-period mean (3.5x training mean) indicates a structural shift. Current model is miscalibrated.

**Expected Impact:** Improved forecast accuracy by capturing new regime patterns.

**Action:** Collect post-Feb 2026 data, add regime indicator feature, retrain HistGradientBoostingRegressor.

---

### 9. [Urgent] Retrain model for Organic_Social (H60)

**Category:** Model Risk  
**Grain:** Organic_Social | **Horizon:** H60  
**Confidence:** High | **Effort:** Medium (2–3 days to retrain with post-shift data)

**Description:** Test-period mean (3.8x training mean) indicates a structural shift. Current model is miscalibrated.

**Expected Impact:** Improved forecast accuracy by capturing new regime patterns.

**Action:** Collect post-Feb 2026 data, add regime indicator feature, retrain HistGradientBoostingRegressor.

---

### 10. [Urgent] URGENT: Pmax (H60) is unprofitable

**Category:** Urgent Alert  
**Grain:** Pmax | **Horizon:** H60  
**Confidence:** High | **Effort:** Low (pause campaign or reduce bids)

**Description:** ROAS is 0.92x — below breakeven. Every dollar spent loses money.

**Expected Impact:** Immediate cost savings by pausing or restructuring.

**Action:** Pause campaign immediately. Audit landing pages, audience targeting, and creative relevance before restart.

---

### 11. [Urgent] Retrain model for Remarketing_Brand (H30)

**Category:** Model Risk  
**Grain:** Remarketing_Brand | **Horizon:** H30  
**Confidence:** High | **Effort:** Medium (2–3 days to retrain with post-shift data)

**Description:** Test-period mean (2.1x training mean) indicates a structural shift. Current model is miscalibrated.

**Expected Impact:** Improved forecast accuracy by capturing new regime patterns.

**Action:** Collect post-Feb 2026 data, add regime indicator feature, retrain HistGradientBoostingRegressor.

---

### 12. [Urgent] Retrain model for Remarketing_Brand (H60)

**Category:** Model Risk  
**Grain:** Remarketing_Brand | **Horizon:** H60  
**Confidence:** High | **Effort:** Medium (2–3 days to retrain with post-shift data)

**Description:** Test-period mean (3.5x training mean) indicates a structural shift. Current model is miscalibrated.

**Expected Impact:** Improved forecast accuracy by capturing new regime patterns.

**Action:** Collect post-Feb 2026 data, add regime indicator feature, retrain HistGradientBoostingRegressor.

---

### 13. [Urgent] Retrain model for Remarketing_DPA (H30)

**Category:** Model Risk  
**Grain:** Remarketing_DPA | **Horizon:** H30  
**Confidence:** High | **Effort:** Medium (2–3 days to retrain with post-shift data)

**Description:** Test-period mean (3.3x training mean) indicates a structural shift. Current model is miscalibrated.

**Expected Impact:** Improved forecast accuracy by capturing new regime patterns.

**Action:** Collect post-Feb 2026 data, add regime indicator feature, retrain HistGradientBoostingRegressor.

---

### 14. [Urgent] Retrain model for Remarketing_DPA (H60)

**Category:** Model Risk  
**Grain:** Remarketing_DPA | **Horizon:** H60  
**Confidence:** High | **Effort:** Medium (2–3 days to retrain with post-shift data)

**Description:** Test-period mean (7.8x training mean) indicates a structural shift. Current model is miscalibrated.

**Expected Impact:** Improved forecast accuracy by capturing new regime patterns.

**Action:** Collect post-Feb 2026 data, add regime indicator feature, retrain HistGradientBoostingRegressor.

---

### 15. [Urgent] Retrain model for Remarketing_DPA (H90)

**Category:** Model Risk  
**Grain:** Remarketing_DPA | **Horizon:** H90  
**Confidence:** High | **Effort:** Medium (2–3 days to retrain with post-shift data)

**Description:** Test-period mean (2.1x training mean) indicates a structural shift. Current model is miscalibrated.

**Expected Impact:** Improved forecast accuracy by capturing new regime patterns.

**Action:** Collect post-Feb 2026 data, add regime indicator feature, retrain HistGradientBoostingRegressor.

---

### 16. [Urgent] Retrain model for Search (H30)

**Category:** Model Risk  
**Grain:** Search | **Horizon:** H30  
**Confidence:** High | **Effort:** Medium (2–3 days to retrain with post-shift data)

**Description:** Test-period mean (2.2x training mean) indicates a structural shift. Current model is miscalibrated.

**Expected Impact:** Improved forecast accuracy by capturing new regime patterns.

**Action:** Collect post-Feb 2026 data, add regime indicator feature, retrain HistGradientBoostingRegressor.

---

### 17. [Urgent] Retrain model for Search (H60)

**Category:** Model Risk  
**Grain:** Search | **Horizon:** H60  
**Confidence:** High | **Effort:** Medium (2–3 days to retrain with post-shift data)

**Description:** Test-period mean (4.1x training mean) indicates a structural shift. Current model is miscalibrated.

**Expected Impact:** Improved forecast accuracy by capturing new regime patterns.

**Action:** Collect post-Feb 2026 data, add regime indicator feature, retrain HistGradientBoostingRegressor.

---

### 18. [Urgent] Retrain model for Shopping (H30)

**Category:** Model Risk  
**Grain:** Shopping | **Horizon:** H30  
**Confidence:** High | **Effort:** Medium (2–3 days to retrain with post-shift data)

**Description:** Test-period mean (4.0x training mean) indicates a structural shift. Current model is miscalibrated.

**Expected Impact:** Improved forecast accuracy by capturing new regime patterns.

**Action:** Collect post-Feb 2026 data, add regime indicator feature, retrain HistGradientBoostingRegressor.

---

### 19. [Urgent] Retrain model for Shopping (H60)

**Category:** Model Risk  
**Grain:** Shopping | **Horizon:** H60  
**Confidence:** High | **Effort:** Medium (2–3 days to retrain with post-shift data)

**Description:** Test-period mean (24.1x training mean) indicates a structural shift. Current model is miscalibrated.

**Expected Impact:** Improved forecast accuracy by capturing new regime patterns.

**Action:** Collect post-Feb 2026 data, add regime indicator feature, retrain HistGradientBoostingRegressor.

---

### 20. [Urgent] Retrain model for Shopping (H90)

**Category:** Model Risk  
**Grain:** Shopping | **Horizon:** H90  
**Confidence:** High | **Effort:** Medium (2–3 days to retrain with post-shift data)

**Description:** Test-period mean (26.9x training mean) indicates a structural shift. Current model is miscalibrated.

**Expected Impact:** Improved forecast accuracy by capturing new regime patterns.

**Action:** Collect post-Feb 2026 data, add regime indicator feature, retrain HistGradientBoostingRegressor.

---

### 21. [High] Widen prediction intervals for Bing Ads (H60)

**Category:** Model Calibration  
**Grain:** Bing Ads | **Horizon:** H60  
**Confidence:** High | **Effort:** Low (tune quantile parameters or switch to p5/p95)

**Description:** Coverage rate is only 7.1%. Model is overconfident.

**Expected Impact:** More reliable risk assessment. Fewer 'surprise' misses.

**Action:** Retrain with p5/p95 quantiles, or increase regularization to reduce overfitting.

---

### 22. [High] Investigate Bing Ads (H60) overperformance

**Category:** Investigation  
**Grain:** Bing Ads | **Horizon:** H60  
**Confidence:** High | **Effort:** Low (1–2 hours of ad platform review)

**Description:** Actual revenue (14,182) deviates 113% from forecast (6,673).

**Expected Impact:** Identify root cause (campaign changes, external factors, data issues).

**Action:** Check ad platform for campaign changes, budget shifts, or tracking issues in the forecast period.

---

### 23. [High] Investigate Bing Ads (H90) overperformance

**Category:** Investigation  
**Grain:** Bing Ads | **Horizon:** H90  
**Confidence:** High | **Effort:** Low (1–2 hours of ad platform review)

**Description:** Actual revenue (10,412) deviates 89% from forecast (5,507).

**Expected Impact:** Identify root cause (campaign changes, external factors, data issues).

**Action:** Check ad platform for campaign changes, budget shifts, or tracking issues in the forecast period.

---

### 24. [High] Widen prediction intervals for Direct (H30)

**Category:** Model Calibration  
**Grain:** Direct | **Horizon:** H30  
**Confidence:** High | **Effort:** Low (tune quantile parameters or switch to p5/p95)

**Description:** Coverage rate is only 25.0%. Model is overconfident.

**Expected Impact:** More reliable risk assessment. Fewer 'surprise' misses.

**Action:** Retrain with p5/p95 quantiles, or increase regularization to reduce overfitting.

---

### 25. [High] Investigate Direct (H30) underperformance

**Category:** Investigation  
**Grain:** Direct | **Horizon:** H30  
**Confidence:** High | **Effort:** Low (1–2 hours of ad platform review)

**Description:** Actual revenue (34,672) deviates 57% from forecast (80,385).

**Expected Impact:** Identify root cause (campaign changes, external factors, data issues).

**Action:** Check ad platform for campaign changes, budget shifts, or tracking issues in the forecast period.

---

### 26. [High] Widen prediction intervals for Direct (H60)

**Category:** Model Calibration  
**Grain:** Direct | **Horizon:** H60  
**Confidence:** High | **Effort:** Low (tune quantile parameters or switch to p5/p95)

**Description:** Coverage rate is only 0.0%. Model is overconfident.

**Expected Impact:** More reliable risk assessment. Fewer 'surprise' misses.

**Action:** Retrain with p5/p95 quantiles, or increase regularization to reduce overfitting.

---

### 27. [High] Investigate Direct (H60) overperformance

**Category:** Investigation  
**Grain:** Direct | **Horizon:** H60  
**Confidence:** High | **Effort:** Low (1–2 hours of ad platform review)

**Description:** Actual revenue (253,311) deviates 144% from forecast (103,831).

**Expected Impact:** Identify root cause (campaign changes, external factors, data issues).

**Action:** Check ad platform for campaign changes, budget shifts, or tracking issues in the forecast period.

---

### 28. [High] Investigate Direct (H90) overperformance

**Category:** Investigation  
**Grain:** Direct | **Horizon:** H90  
**Confidence:** High | **Effort:** Low (1–2 hours of ad platform review)

**Description:** Actual revenue (174,504) deviates 115% from forecast (81,048).

**Expected Impact:** Identify root cause (campaign changes, external factors, data issues).

**Action:** Check ad platform for campaign changes, budget shifts, or tracking issues in the forecast period.

---

### 29. [High] Widen prediction intervals for Email (H30)

**Category:** Model Calibration  
**Grain:** Email | **Horizon:** H30  
**Confidence:** High | **Effort:** Low (tune quantile parameters or switch to p5/p95)

**Description:** Coverage rate is only 39.3%. Model is overconfident.

**Expected Impact:** More reliable risk assessment. Fewer 'surprise' misses.

**Action:** Retrain with p5/p95 quantiles, or increase regularization to reduce overfitting.

---

### 30. [High] Investigate Email (H30) underperformance

**Category:** Investigation  
**Grain:** Email | **Horizon:** H30  
**Confidence:** High | **Effort:** Low (1–2 hours of ad platform review)

**Description:** Actual revenue (18,129) deviates 77% from forecast (78,107).

**Expected Impact:** Identify root cause (campaign changes, external factors, data issues).

**Action:** Check ad platform for campaign changes, budget shifts, or tracking issues in the forecast period.

---

### 31. [High] Widen prediction intervals for Email (H60)

**Category:** Model Calibration  
**Grain:** Email | **Horizon:** H60  
**Confidence:** High | **Effort:** Low (tune quantile parameters or switch to p5/p95)

**Description:** Coverage rate is only 0.0%. Model is overconfident.

**Expected Impact:** More reliable risk assessment. Fewer 'surprise' misses.

**Action:** Retrain with p5/p95 quantiles, or increase regularization to reduce overfitting.

---

### 32. [High] Investigate Email (H60) overperformance

**Category:** Investigation  
**Grain:** Email | **Horizon:** H60  
**Confidence:** High | **Effort:** Low (1–2 hours of ad platform review)

**Description:** Actual revenue (160,434) deviates 173% from forecast (58,837).

**Expected Impact:** Identify root cause (campaign changes, external factors, data issues).

**Action:** Check ad platform for campaign changes, budget shifts, or tracking issues in the forecast period.

---

### 33. [High] Widen prediction intervals for Email (H90)

**Category:** Model Calibration  
**Grain:** Email | **Horizon:** H90  
**Confidence:** High | **Effort:** Low (tune quantile parameters or switch to p5/p95)

**Description:** Coverage rate is only 46.4%. Model is overconfident.

**Expected Impact:** More reliable risk assessment. Fewer 'surprise' misses.

**Action:** Retrain with p5/p95 quantiles, or increase regularization to reduce overfitting.

---

### 34. [High] Investigate Email (H90) overperformance

**Category:** Investigation  
**Grain:** Email | **Horizon:** H90  
**Confidence:** High | **Effort:** Low (1–2 hours of ad platform review)

**Description:** Actual revenue (114,085) deviates 110% from forecast (54,274).

**Expected Impact:** Identify root cause (campaign changes, external factors, data issues).

**Action:** Check ad platform for campaign changes, budget shifts, or tracking issues in the forecast period.

---

### 35. [High] Investigate Google Ads (H30) underperformance

**Category:** Investigation  
**Grain:** Google Ads | **Horizon:** H30  
**Confidence:** High | **Effort:** Low (1–2 hours of ad platform review)

**Description:** Actual revenue (97,569) deviates 57% from forecast (224,412).

**Expected Impact:** Identify root cause (campaign changes, external factors, data issues).

**Action:** Check ad platform for campaign changes, budget shifts, or tracking issues in the forecast period.

---

### 36. [High] Widen prediction intervals for Google Ads (H60)

**Category:** Model Calibration  
**Grain:** Google Ads | **Horizon:** H60  
**Confidence:** High | **Effort:** Low (tune quantile parameters or switch to p5/p95)

**Description:** Coverage rate is only 0.0%. Model is overconfident.

**Expected Impact:** More reliable risk assessment. Fewer 'surprise' misses.

**Action:** Retrain with p5/p95 quantiles, or increase regularization to reduce overfitting.

---

### 37. [High] Investigate Google Ads (H60) overperformance

**Category:** Investigation  
**Grain:** Google Ads | **Horizon:** H60  
**Confidence:** High | **Effort:** Low (1–2 hours of ad platform review)

**Description:** Actual revenue (720,741) deviates 57% from forecast (458,924).

**Expected Impact:** Identify root cause (campaign changes, external factors, data issues).

**Action:** Check ad platform for campaign changes, budget shifts, or tracking issues in the forecast period.

---

### 38. [High] Widen prediction intervals for Google Ads (H90)

**Category:** Model Calibration  
**Grain:** Google Ads | **Horizon:** H90  
**Confidence:** High | **Effort:** Low (tune quantile parameters or switch to p5/p95)

**Description:** Coverage rate is only 0.0%. Model is overconfident.

**Expected Impact:** More reliable risk assessment. Fewer 'surprise' misses.

**Action:** Retrain with p5/p95 quantiles, or increase regularization to reduce overfitting.

---

### 39. [High] Investigate Meta Ads (H30) underperformance

**Category:** Investigation  
**Grain:** Meta Ads | **Horizon:** H30  
**Confidence:** High | **Effort:** Low (1–2 hours of ad platform review)

**Description:** Actual revenue (8,657) deviates 68% from forecast (26,953).

**Expected Impact:** Identify root cause (campaign changes, external factors, data issues).

**Action:** Check ad platform for campaign changes, budget shifts, or tracking issues in the forecast period.

---

### 40. [High] Widen prediction intervals for Meta Ads (H60)

**Category:** Model Calibration  
**Grain:** Meta Ads | **Horizon:** H60  
**Confidence:** High | **Effort:** Low (tune quantile parameters or switch to p5/p95)

**Description:** Coverage rate is only 0.0%. Model is overconfident.

**Expected Impact:** More reliable risk assessment. Fewer 'surprise' misses.

**Action:** Retrain with p5/p95 quantiles, or increase regularization to reduce overfitting.

---

### 41. [High] Investigate Meta Ads (H60) overperformance

**Category:** Investigation  
**Grain:** Meta Ads | **Horizon:** H60  
**Confidence:** High | **Effort:** Low (1–2 hours of ad platform review)

**Description:** Actual revenue (94,563) deviates 95% from forecast (48,397).

**Expected Impact:** Identify root cause (campaign changes, external factors, data issues).

**Action:** Check ad platform for campaign changes, budget shifts, or tracking issues in the forecast period.

---

### 42. [High] Widen prediction intervals for Meta Ads (H90)

**Category:** Model Calibration  
**Grain:** Meta Ads | **Horizon:** H90  
**Confidence:** High | **Effort:** Low (tune quantile parameters or switch to p5/p95)

**Description:** Coverage rate is only 28.6%. Model is overconfident.

**Expected Impact:** More reliable risk assessment. Fewer 'surprise' misses.

**Action:** Retrain with p5/p95 quantiles, or increase regularization to reduce overfitting.

---

### 43. [High] Investigate Meta Ads (H90) overperformance

**Category:** Investigation  
**Grain:** Meta Ads | **Horizon:** H90  
**Confidence:** High | **Effort:** Low (1–2 hours of ad platform review)

**Description:** Actual revenue (49,772) deviates 65% from forecast (30,179).

**Expected Impact:** Identify root cause (campaign changes, external factors, data issues).

**Action:** Check ad platform for campaign changes, budget shifts, or tracking issues in the forecast period.

---

### 44. [High] Widen prediction intervals for Organic/Direct (H30)

**Category:** Model Calibration  
**Grain:** Organic/Direct | **Horizon:** H30  
**Confidence:** High | **Effort:** Low (tune quantile parameters or switch to p5/p95)

**Description:** Coverage rate is only 46.4%. Model is overconfident.

**Expected Impact:** More reliable risk assessment. Fewer 'surprise' misses.

**Action:** Retrain with p5/p95 quantiles, or increase regularization to reduce overfitting.

---

### 45. [High] Investigate Organic/Direct (H30) underperformance

**Category:** Investigation  
**Grain:** Organic/Direct | **Horizon:** H30  
**Confidence:** High | **Effort:** Low (1–2 hours of ad platform review)

**Description:** Actual revenue (83,452) deviates 57% from forecast (192,849).

**Expected Impact:** Identify root cause (campaign changes, external factors, data issues).

**Action:** Check ad platform for campaign changes, budget shifts, or tracking issues in the forecast period.

---

### 46. [High] Widen prediction intervals for Organic/Direct (H60)

**Category:** Model Calibration  
**Grain:** Organic/Direct | **Horizon:** H60  
**Confidence:** High | **Effort:** Low (tune quantile parameters or switch to p5/p95)

**Description:** Coverage rate is only 0.0%. Model is overconfident.

**Expected Impact:** More reliable risk assessment. Fewer 'surprise' misses.

**Action:** Retrain with p5/p95 quantiles, or increase regularization to reduce overfitting.

---

### 47. [High] Investigate Organic/Direct (H60) overperformance

**Category:** Investigation  
**Grain:** Organic/Direct | **Horizon:** H60  
**Confidence:** High | **Effort:** Low (1–2 hours of ad platform review)

**Description:** Actual revenue (627,351) deviates 121% from forecast (283,493).

**Expected Impact:** Identify root cause (campaign changes, external factors, data issues).

**Action:** Check ad platform for campaign changes, budget shifts, or tracking issues in the forecast period.

---

### 48. [High] Widen prediction intervals for Organic_Search (H30)

**Category:** Model Calibration  
**Grain:** Organic_Search | **Horizon:** H30  
**Confidence:** High | **Effort:** Low (tune quantile parameters or switch to p5/p95)

**Description:** Coverage rate is only 32.1%. Model is overconfident.

**Expected Impact:** More reliable risk assessment. Fewer 'surprise' misses.

**Action:** Retrain with p5/p95 quantiles, or increase regularization to reduce overfitting.

---

### 49. [High] Widen prediction intervals for Organic_Search (H60)

**Category:** Model Calibration  
**Grain:** Organic_Search | **Horizon:** H60  
**Confidence:** High | **Effort:** Low (tune quantile parameters or switch to p5/p95)

**Description:** Coverage rate is only 0.0%. Model is overconfident.

**Expected Impact:** More reliable risk assessment. Fewer 'surprise' misses.

**Action:** Retrain with p5/p95 quantiles, or increase regularization to reduce overfitting.

---

### 50. [High] Investigate Organic_Search (H60) overperformance

**Category:** Investigation  
**Grain:** Organic_Search | **Horizon:** H60  
**Confidence:** High | **Effort:** Low (1–2 hours of ad platform review)

**Description:** Actual revenue (151,252) deviates 124% from forecast (67,509).

**Expected Impact:** Identify root cause (campaign changes, external factors, data issues).

**Action:** Check ad platform for campaign changes, budget shifts, or tracking issues in the forecast period.

---

### 51. [High] Investigate Organic_Search (H90) overperformance

**Category:** Investigation  
**Grain:** Organic_Search | **Horizon:** H90  
**Confidence:** High | **Effort:** Low (1–2 hours of ad platform review)

**Description:** Actual revenue (113,401) deviates 77% from forecast (63,950).

**Expected Impact:** Identify root cause (campaign changes, external factors, data issues).

**Action:** Check ad platform for campaign changes, budget shifts, or tracking issues in the forecast period.

---

### 52. [High] Widen prediction intervals for Organic_Search_Bing (H30)

**Category:** Model Calibration  
**Grain:** Organic_Search_Bing | **Horizon:** H30  
**Confidence:** High | **Effort:** Low (tune quantile parameters or switch to p5/p95)

**Description:** Coverage rate is only 42.9%. Model is overconfident.

**Expected Impact:** More reliable risk assessment. Fewer 'surprise' misses.

**Action:** Retrain with p5/p95 quantiles, or increase regularization to reduce overfitting.

---

### 53. [High] Investigate Organic_Search_Bing (H30) underperformance

**Category:** Investigation  
**Grain:** Organic_Search_Bing | **Horizon:** H30  
**Confidence:** High | **Effort:** Low (1–2 hours of ad platform review)

**Description:** Actual revenue (4,798) deviates 52% from forecast (10,003).

**Expected Impact:** Identify root cause (campaign changes, external factors, data issues).

**Action:** Check ad platform for campaign changes, budget shifts, or tracking issues in the forecast period.

---

### 54. [High] Widen prediction intervals for Organic_Search_Bing (H60)

**Category:** Model Calibration  
**Grain:** Organic_Search_Bing | **Horizon:** H60  
**Confidence:** High | **Effort:** Low (tune quantile parameters or switch to p5/p95)

**Description:** Coverage rate is only 0.0%. Model is overconfident.

**Expected Impact:** More reliable risk assessment. Fewer 'surprise' misses.

**Action:** Retrain with p5/p95 quantiles, or increase regularization to reduce overfitting.

---

### 55. [High] Investigate Organic_Search_Bing (H60) overperformance

**Category:** Investigation  
**Grain:** Organic_Search_Bing | **Horizon:** H60  
**Confidence:** High | **Effort:** Low (1–2 hours of ad platform review)

**Description:** Actual revenue (34,387) deviates 106% from forecast (16,723).

**Expected Impact:** Identify root cause (campaign changes, external factors, data issues).

**Action:** Check ad platform for campaign changes, budget shifts, or tracking issues in the forecast period.

---

### 56. [High] Widen prediction intervals for Organic_Search_Bing (H90)

**Category:** Model Calibration  
**Grain:** Organic_Search_Bing | **Horizon:** H90  
**Confidence:** High | **Effort:** Low (tune quantile parameters or switch to p5/p95)

**Description:** Coverage rate is only 42.9%. Model is overconfident.

**Expected Impact:** More reliable risk assessment. Fewer 'surprise' misses.

**Action:** Retrain with p5/p95 quantiles, or increase regularization to reduce overfitting.

---

### 57. [High] Investigate Organic_Search_Bing (H90) overperformance

**Category:** Investigation  
**Grain:** Organic_Search_Bing | **Horizon:** H90  
**Confidence:** High | **Effort:** Low (1–2 hours of ad platform review)

**Description:** Actual revenue (24,159) deviates 113% from forecast (11,344).

**Expected Impact:** Identify root cause (campaign changes, external factors, data issues).

**Action:** Check ad platform for campaign changes, budget shifts, or tracking issues in the forecast period.

---

### 58. [High] Widen prediction intervals for Organic_Social (H30)

**Category:** Model Calibration  
**Grain:** Organic_Social | **Horizon:** H30  
**Confidence:** High | **Effort:** Low (tune quantile parameters or switch to p5/p95)

**Description:** Coverage rate is only 39.3%. Model is overconfident.

**Expected Impact:** More reliable risk assessment. Fewer 'surprise' misses.

**Action:** Retrain with p5/p95 quantiles, or increase regularization to reduce overfitting.

---

### 59. [High] Investigate Organic_Social (H30) underperformance

**Category:** Investigation  
**Grain:** Organic_Social | **Horizon:** H30  
**Confidence:** High | **Effort:** Low (1–2 hours of ad platform review)

**Description:** Actual revenue (3,026) deviates 60% from forecast (7,590).

**Expected Impact:** Identify root cause (campaign changes, external factors, data issues).

**Action:** Check ad platform for campaign changes, budget shifts, or tracking issues in the forecast period.

---

### 60. [High] Widen prediction intervals for Organic_Social (H60)

**Category:** Model Calibration  
**Grain:** Organic_Social | **Horizon:** H60  
**Confidence:** High | **Effort:** Low (tune quantile parameters or switch to p5/p95)

**Description:** Coverage rate is only 0.0%. Model is overconfident.

**Expected Impact:** More reliable risk assessment. Fewer 'surprise' misses.

**Action:** Retrain with p5/p95 quantiles, or increase regularization to reduce overfitting.

---

### 61. [High] Investigate Organic_Social (H60) overperformance

**Category:** Investigation  
**Grain:** Organic_Social | **Horizon:** H60  
**Confidence:** High | **Effort:** Low (1–2 hours of ad platform review)

**Description:** Actual revenue (27,968) deviates 149% from forecast (11,222).

**Expected Impact:** Identify root cause (campaign changes, external factors, data issues).

**Action:** Check ad platform for campaign changes, budget shifts, or tracking issues in the forecast period.

---

### 62. [High] Widen prediction intervals for Organic_Social (H90)

**Category:** Model Calibration  
**Grain:** Organic_Social | **Horizon:** H90  
**Confidence:** High | **Effort:** Low (tune quantile parameters or switch to p5/p95)

**Description:** Coverage rate is only 42.9%. Model is overconfident.

**Expected Impact:** More reliable risk assessment. Fewer 'surprise' misses.

**Action:** Retrain with p5/p95 quantiles, or increase regularization to reduce overfitting.

---

### 63. [High] Investigate Organic_Social (H90) overperformance

**Category:** Investigation  
**Grain:** Organic_Social | **Horizon:** H90  
**Confidence:** High | **Effort:** Low (1–2 hours of ad platform review)

**Description:** Actual revenue (18,893) deviates 167% from forecast (7,070).

**Expected Impact:** Identify root cause (campaign changes, external factors, data issues).

**Action:** Check ad platform for campaign changes, budget shifts, or tracking issues in the forecast period.

---

### 64. [High] Widen prediction intervals for Pmax (H30)

**Category:** Model Calibration  
**Grain:** Pmax | **Horizon:** H30  
**Confidence:** High | **Effort:** Low (tune quantile parameters or switch to p5/p95)

**Description:** Coverage rate is only 35.7%. Model is overconfident.

**Expected Impact:** More reliable risk assessment. Fewer 'surprise' misses.

**Action:** Retrain with p5/p95 quantiles, or increase regularization to reduce overfitting.

---

### 65. [High] Widen prediction intervals for Pmax (H60)

**Category:** Model Calibration  
**Grain:** Pmax | **Horizon:** H60  
**Confidence:** High | **Effort:** Low (tune quantile parameters or switch to p5/p95)

**Description:** Coverage rate is only 7.1%. Model is overconfident.

**Expected Impact:** More reliable risk assessment. Fewer 'surprise' misses.

**Action:** Retrain with p5/p95 quantiles, or increase regularization to reduce overfitting.

---

### 66. [High] Widen prediction intervals for Pmax (H90)

**Category:** Model Calibration  
**Grain:** Pmax | **Horizon:** H90  
**Confidence:** High | **Effort:** Low (tune quantile parameters or switch to p5/p95)

**Description:** Coverage rate is only 46.4%. Model is overconfident.

**Expected Impact:** More reliable risk assessment. Fewer 'surprise' misses.

**Action:** Retrain with p5/p95 quantiles, or increase regularization to reduce overfitting.

---

### 67. [High] Widen prediction intervals for Remarketing_Brand (H60)

**Category:** Model Calibration  
**Grain:** Remarketing_Brand | **Horizon:** H60  
**Confidence:** High | **Effort:** Low (tune quantile parameters or switch to p5/p95)

**Description:** Coverage rate is only 7.1%. Model is overconfident.

**Expected Impact:** More reliable risk assessment. Fewer 'surprise' misses.

**Action:** Retrain with p5/p95 quantiles, or increase regularization to reduce overfitting.

---

### 68. [High] Investigate Remarketing_Brand (H60) overperformance

**Category:** Investigation  
**Grain:** Remarketing_Brand | **Horizon:** H60  
**Confidence:** High | **Effort:** Low (1–2 hours of ad platform review)

**Description:** Actual revenue (16,845) deviates 135% from forecast (7,172).

**Expected Impact:** Identify root cause (campaign changes, external factors, data issues).

**Action:** Check ad platform for campaign changes, budget shifts, or tracking issues in the forecast period.

---

### 69. [High] Widen prediction intervals for Remarketing_Brand (H90)

**Category:** Model Calibration  
**Grain:** Remarketing_Brand | **Horizon:** H90  
**Confidence:** High | **Effort:** Low (tune quantile parameters or switch to p5/p95)

**Description:** Coverage rate is only 32.1%. Model is overconfident.

**Expected Impact:** More reliable risk assessment. Fewer 'surprise' misses.

**Action:** Retrain with p5/p95 quantiles, or increase regularization to reduce overfitting.

---

### 70. [High] Investigate Remarketing_DPA (H30) underperformance

**Category:** Investigation  
**Grain:** Remarketing_DPA | **Horizon:** H30  
**Confidence:** High | **Effort:** Low (1–2 hours of ad platform review)

**Description:** Actual revenue (3,521) deviates 80% from forecast (17,882).

**Expected Impact:** Identify root cause (campaign changes, external factors, data issues).

**Action:** Check ad platform for campaign changes, budget shifts, or tracking issues in the forecast period.

---

### 71. [High] Widen prediction intervals for Remarketing_DPA (H60)

**Category:** Model Calibration  
**Grain:** Remarketing_DPA | **Horizon:** H60  
**Confidence:** High | **Effort:** Low (tune quantile parameters or switch to p5/p95)

**Description:** Coverage rate is only 0.0%. Model is overconfident.

**Expected Impact:** More reliable risk assessment. Fewer 'surprise' misses.

**Action:** Retrain with p5/p95 quantiles, or increase regularization to reduce overfitting.

---

### 72. [High] Investigate Remarketing_DPA (H60) overperformance

**Category:** Investigation  
**Grain:** Remarketing_DPA | **Horizon:** H60  
**Confidence:** High | **Effort:** Low (1–2 hours of ad platform review)

**Description:** Actual revenue (62,387) deviates 123% from forecast (27,970).

**Expected Impact:** Identify root cause (campaign changes, external factors, data issues).

**Action:** Check ad platform for campaign changes, budget shifts, or tracking issues in the forecast period.

---

### 73. [High] Widen prediction intervals for Remarketing_DPA (H90)

**Category:** Model Calibration  
**Grain:** Remarketing_DPA | **Horizon:** H90  
**Confidence:** High | **Effort:** Low (tune quantile parameters or switch to p5/p95)

**Description:** Coverage rate is only 0.0%. Model is overconfident.

**Expected Impact:** More reliable risk assessment. Fewer 'surprise' misses.

**Action:** Retrain with p5/p95 quantiles, or increase regularization to reduce overfitting.

---

### 74. [High] Investigate Remarketing_DPA (H90) overperformance

**Category:** Investigation  
**Grain:** Remarketing_DPA | **Horizon:** H90  
**Confidence:** High | **Effort:** Low (1–2 hours of ad platform review)

**Description:** Actual revenue (30,368) deviates 147% from forecast (12,271).

**Expected Impact:** Identify root cause (campaign changes, external factors, data issues).

**Action:** Check ad platform for campaign changes, budget shifts, or tracking issues in the forecast period.

---

### 75. [High] Investigate Search (H30) underperformance

**Category:** Investigation  
**Grain:** Search | **Horizon:** H30  
**Confidence:** High | **Effort:** Low (1–2 hours of ad platform review)

**Description:** Actual revenue (50,657) deviates 58% from forecast (119,340).

**Expected Impact:** Identify root cause (campaign changes, external factors, data issues).

**Action:** Check ad platform for campaign changes, budget shifts, or tracking issues in the forecast period.

---

### 76. [High] Widen prediction intervals for Search (H60)

**Category:** Model Calibration  
**Grain:** Search | **Horizon:** H60  
**Confidence:** High | **Effort:** Low (tune quantile parameters or switch to p5/p95)

**Description:** Coverage rate is only 0.0%. Model is overconfident.

**Expected Impact:** More reliable risk assessment. Fewer 'surprise' misses.

**Action:** Retrain with p5/p95 quantiles, or increase regularization to reduce overfitting.

---

### 77. [High] Investigate Search (H60) overperformance

**Category:** Investigation  
**Grain:** Search | **Horizon:** H60  
**Confidence:** High | **Effort:** Low (1–2 hours of ad platform review)

**Description:** Actual revenue (349,072) deviates 58% from forecast (220,645).

**Expected Impact:** Identify root cause (campaign changes, external factors, data issues).

**Action:** Check ad platform for campaign changes, budget shifts, or tracking issues in the forecast period.

---

### 78. [High] Widen prediction intervals for Search (H90)

**Category:** Model Calibration  
**Grain:** Search | **Horizon:** H90  
**Confidence:** High | **Effort:** Low (tune quantile parameters or switch to p5/p95)

**Description:** Coverage rate is only 7.1%. Model is overconfident.

**Expected Impact:** More reliable risk assessment. Fewer 'surprise' misses.

**Action:** Retrain with p5/p95 quantiles, or increase regularization to reduce overfitting.

---

### 79. [High] Investigate Search (H90) overperformance

**Category:** Investigation  
**Grain:** Search | **Horizon:** H90  
**Confidence:** High | **Effort:** Low (1–2 hours of ad platform review)

**Description:** Actual revenue (243,548) deviates 53% from forecast (158,876).

**Expected Impact:** Identify root cause (campaign changes, external factors, data issues).

**Action:** Check ad platform for campaign changes, budget shifts, or tracking issues in the forecast period.

---

### 80. [High] Investigate Shopping (H30) overperformance

**Category:** Investigation  
**Grain:** Shopping | **Horizon:** H30  
**Confidence:** High | **Effort:** Low (1–2 hours of ad platform review)

**Description:** Actual revenue (12,204) deviates 243% from forecast (3,560).

**Expected Impact:** Identify root cause (campaign changes, external factors, data issues).

**Action:** Check ad platform for campaign changes, budget shifts, or tracking issues in the forecast period.

---

### 81. [High] Widen prediction intervals for Shopping (H60)

**Category:** Model Calibration  
**Grain:** Shopping | **Horizon:** H60  
**Confidence:** High | **Effort:** Low (tune quantile parameters or switch to p5/p95)

**Description:** Coverage rate is only 0.0%. Model is overconfident.

**Expected Impact:** More reliable risk assessment. Fewer 'surprise' misses.

**Action:** Retrain with p5/p95 quantiles, or increase regularization to reduce overfitting.

---

### 82. [High] Investigate Shopping (H60) overperformance

**Category:** Investigation  
**Grain:** Shopping | **Horizon:** H60  
**Confidence:** High | **Effort:** Low (1–2 hours of ad platform review)

**Description:** Actual revenue (197,427) deviates 18754% from forecast (1,047).

**Expected Impact:** Identify root cause (campaign changes, external factors, data issues).

**Action:** Check ad platform for campaign changes, budget shifts, or tracking issues in the forecast period.

---

### 83. [High] Widen prediction intervals for Shopping (H90)

**Category:** Model Calibration  
**Grain:** Shopping | **Horizon:** H90  
**Confidence:** High | **Effort:** Low (tune quantile parameters or switch to p5/p95)

**Description:** Coverage rate is only 0.0%. Model is overconfident.

**Expected Impact:** More reliable risk assessment. Fewer 'surprise' misses.

**Action:** Retrain with p5/p95 quantiles, or increase regularization to reduce overfitting.

---

### 84. [Medium] Increase budget for Bing Ads (30d)

**Category:** Budget Optimization  
**Grain:** Bing Ads | **Horizon:** H30  
**Confidence:** Medium | **Effort:** Low (increase daily budget in ad platform)

**Description:** High ROAS (6.27x) with low daily spend (44 $/day). Underinvested channel.

**Expected Impact:** Revenue uplift: ~5.3x per dollar of incremental spend.

**Action:** Increase daily budget by 25–50% and monitor ROAS over next 14 days.

---

### 85. [Medium] Optimize or reduce spend for Google Ads (90d)

**Category:** Budget Optimization  
**Grain:** Google Ads | **Horizon:** H90  
**Confidence:** Medium | **Effort:** Medium (audience/targeting review + A/B test)

**Description:** Low ROAS (1.47x) with significant daily spend (2194 $/day). Diminishing returns.

**Expected Impact:** Cost savings of 20–40% with minimal revenue loss if spend is reallocated.

**Action:** Review audience targeting, pause underperforming ad groups, test new creatives. Consider 20% budget reduction.

---

### 86. [Medium] Increase budget for Meta Ads (30d)

**Category:** Budget Optimization  
**Grain:** Meta Ads | **Horizon:** H30  
**Confidence:** Medium | **Effort:** Low (increase daily budget in ad platform)

**Description:** High ROAS (5.02x) with low daily spend (221 $/day). Underinvested channel.

**Expected Impact:** Revenue uplift: ~4.0x per dollar of incremental spend.

**Action:** Increase daily budget by 25–50% and monitor ROAS over next 14 days.

---

### 87. [Medium] Optimize or reduce spend for Pmax (30d)

**Category:** Budget Optimization  
**Grain:** Pmax | **Horizon:** H30  
**Confidence:** Medium | **Effort:** Medium (audience/targeting review + A/B test)

**Description:** Low ROAS (1.26x) with significant daily spend (1456 $/day). Diminishing returns.

**Expected Impact:** Cost savings of 20–40% with minimal revenue loss if spend is reallocated.

**Action:** Review audience targeting, pause underperforming ad groups, test new creatives. Consider 20% budget reduction.

---

### 88. [Medium] Optimize or reduce spend for Pmax (60d)

**Category:** Budget Optimization  
**Grain:** Pmax | **Horizon:** H60  
**Confidence:** Medium | **Effort:** Medium (audience/targeting review + A/B test)

**Description:** Low ROAS (1.30x) with significant daily spend (1456 $/day). Diminishing returns.

**Expected Impact:** Cost savings of 20–40% with minimal revenue loss if spend is reallocated.

**Action:** Review audience targeting, pause underperforming ad groups, test new creatives. Consider 20% budget reduction.

---

### 89. [Medium] Optimize or reduce spend for Pmax (90d)

**Category:** Budget Optimization  
**Grain:** Pmax | **Horizon:** H90  
**Confidence:** Medium | **Effort:** Medium (audience/targeting review + A/B test)

**Description:** Low ROAS (1.01x) with significant daily spend (1456 $/day). Diminishing returns.

**Expected Impact:** Cost savings of 20–40% with minimal revenue loss if spend is reallocated.

**Action:** Review audience targeting, pause underperforming ad groups, test new creatives. Consider 20% budget reduction.

---

### 90. [Medium] Increase budget for Remarketing_Brand (30d)

**Category:** Budget Optimization  
**Grain:** Remarketing_Brand | **Horizon:** H30  
**Confidence:** Medium | **Effort:** Low (increase daily budget in ad platform)

**Description:** High ROAS (7.13x) with low daily spend (24 $/day). Underinvested channel.

**Expected Impact:** Revenue uplift: ~6.1x per dollar of incremental spend.

**Action:** Increase daily budget by 25–50% and monitor ROAS over next 14 days.

---

### 91. [Medium] Increase budget for Remarketing_DPA (30d)

**Category:** Budget Optimization  
**Grain:** Remarketing_DPA | **Horizon:** H30  
**Confidence:** Medium | **Effort:** Low (increase daily budget in ad platform)

**Description:** High ROAS (9.71x) with low daily spend (81 $/day). Underinvested channel.

**Expected Impact:** Revenue uplift: ~8.7x per dollar of incremental spend.

**Action:** Increase daily budget by 25–50% and monitor ROAS over next 14 days.

---

### 92. [Medium] Increase budget for Search (30d)

**Category:** Budget Optimization  
**Grain:** Search | **Horizon:** H30  
**Confidence:** Medium | **Effort:** Low (increase daily budget in ad platform)

**Description:** High ROAS (10.33x) with low daily spend (463 $/day). Underinvested channel.

**Expected Impact:** Revenue uplift: ~9.3x per dollar of incremental spend.

**Action:** Increase daily budget by 25–50% and monitor ROAS over next 14 days.

---

### 93. [Medium] Increase budget for Search (60d)

**Category:** Budget Optimization  
**Grain:** Search | **Horizon:** H60  
**Confidence:** Medium | **Effort:** Low (increase daily budget in ad platform)

**Description:** High ROAS (5.43x) with low daily spend (463 $/day). Underinvested channel.

**Expected Impact:** Revenue uplift: ~4.4x per dollar of incremental spend.

**Action:** Increase daily budget by 25–50% and monitor ROAS over next 14 days.

---

### 94. [Strategic] Optimize Search campaign spend level

**Category:** Strategic  
**Grain:** Search | **Horizon:** H30  
**Confidence:** Medium | **Effort:** Medium (run A/B budget tests at 0.8x, 1.0x, 1.2x multipliers)

**Description:** Search has highest ROAS (10.33x) but response curve shows steep diminishing returns. Find the sweet spot.

**Expected Impact:** Maximize incremental revenue without pushing into diminishing returns.

**Action:** Test budget multipliers between 0.8x and 1.2x over 2-week windows. Measure marginal ROAS at each level.

---

## Quick Reference Table

| # | Priority | Grain | Horizon | Category | Action |
|---|----------|-------|---------|----------|--------|
| 1 | Urgent | Direct | H60 | Model Risk | Collect post-Feb 2026 data, add regime indicator feature, re... |
| 2 | Urgent | Email | H60 | Model Risk | Collect post-Feb 2026 data, add regime indicator feature, re... |
| 3 | Urgent | Google Ads | H60 | Model Risk | Collect post-Feb 2026 data, add regime indicator feature, re... |
| 4 | Urgent | Meta Ads | H30 | Model Risk | Collect post-Feb 2026 data, add regime indicator feature, re... |
| 5 | Urgent | Meta Ads | H60 | Model Risk | Collect post-Feb 2026 data, add regime indicator feature, re... |
| 6 | Urgent | Organic/Direct | H60 | Model Risk | Collect post-Feb 2026 data, add regime indicator feature, re... |
| 7 | Urgent | Organic_Search | H60 | Model Risk | Collect post-Feb 2026 data, add regime indicator feature, re... |
| 8 | Urgent | Organic_Search_Bing | H60 | Model Risk | Collect post-Feb 2026 data, add regime indicator feature, re... |
| 9 | Urgent | Organic_Social | H60 | Model Risk | Collect post-Feb 2026 data, add regime indicator feature, re... |
| 10 | Urgent | Pmax | H60 | Urgent Alert | Pause campaign immediately. Audit landing pages, audience ta... |
| 11 | Urgent | Remarketing_Brand | H30 | Model Risk | Collect post-Feb 2026 data, add regime indicator feature, re... |
| 12 | Urgent | Remarketing_Brand | H60 | Model Risk | Collect post-Feb 2026 data, add regime indicator feature, re... |
| 13 | Urgent | Remarketing_DPA | H30 | Model Risk | Collect post-Feb 2026 data, add regime indicator feature, re... |
| 14 | Urgent | Remarketing_DPA | H60 | Model Risk | Collect post-Feb 2026 data, add regime indicator feature, re... |
| 15 | Urgent | Remarketing_DPA | H90 | Model Risk | Collect post-Feb 2026 data, add regime indicator feature, re... |
| 16 | Urgent | Search | H30 | Model Risk | Collect post-Feb 2026 data, add regime indicator feature, re... |
| 17 | Urgent | Search | H60 | Model Risk | Collect post-Feb 2026 data, add regime indicator feature, re... |
| 18 | Urgent | Shopping | H30 | Model Risk | Collect post-Feb 2026 data, add regime indicator feature, re... |
| 19 | Urgent | Shopping | H60 | Model Risk | Collect post-Feb 2026 data, add regime indicator feature, re... |
| 20 | Urgent | Shopping | H90 | Model Risk | Collect post-Feb 2026 data, add regime indicator feature, re... |
| 21 | High | Bing Ads | H60 | Model Calibration | Retrain with p5/p95 quantiles, or increase regularization to... |
| 22 | High | Bing Ads | H60 | Investigation | Check ad platform for campaign changes, budget shifts, or tr... |
| 23 | High | Bing Ads | H90 | Investigation | Check ad platform for campaign changes, budget shifts, or tr... |
| 24 | High | Direct | H30 | Model Calibration | Retrain with p5/p95 quantiles, or increase regularization to... |
| 25 | High | Direct | H30 | Investigation | Check ad platform for campaign changes, budget shifts, or tr... |
| 26 | High | Direct | H60 | Model Calibration | Retrain with p5/p95 quantiles, or increase regularization to... |
| 27 | High | Direct | H60 | Investigation | Check ad platform for campaign changes, budget shifts, or tr... |
| 28 | High | Direct | H90 | Investigation | Check ad platform for campaign changes, budget shifts, or tr... |
| 29 | High | Email | H30 | Model Calibration | Retrain with p5/p95 quantiles, or increase regularization to... |
| 30 | High | Email | H30 | Investigation | Check ad platform for campaign changes, budget shifts, or tr... |
| 31 | High | Email | H60 | Model Calibration | Retrain with p5/p95 quantiles, or increase regularization to... |
| 32 | High | Email | H60 | Investigation | Check ad platform for campaign changes, budget shifts, or tr... |
| 33 | High | Email | H90 | Model Calibration | Retrain with p5/p95 quantiles, or increase regularization to... |
| 34 | High | Email | H90 | Investigation | Check ad platform for campaign changes, budget shifts, or tr... |
| 35 | High | Google Ads | H30 | Investigation | Check ad platform for campaign changes, budget shifts, or tr... |
| 36 | High | Google Ads | H60 | Model Calibration | Retrain with p5/p95 quantiles, or increase regularization to... |
| 37 | High | Google Ads | H60 | Investigation | Check ad platform for campaign changes, budget shifts, or tr... |
| 38 | High | Google Ads | H90 | Model Calibration | Retrain with p5/p95 quantiles, or increase regularization to... |
| 39 | High | Meta Ads | H30 | Investigation | Check ad platform for campaign changes, budget shifts, or tr... |
| 40 | High | Meta Ads | H60 | Model Calibration | Retrain with p5/p95 quantiles, or increase regularization to... |
| 41 | High | Meta Ads | H60 | Investigation | Check ad platform for campaign changes, budget shifts, or tr... |
| 42 | High | Meta Ads | H90 | Model Calibration | Retrain with p5/p95 quantiles, or increase regularization to... |
| 43 | High | Meta Ads | H90 | Investigation | Check ad platform for campaign changes, budget shifts, or tr... |
| 44 | High | Organic/Direct | H30 | Model Calibration | Retrain with p5/p95 quantiles, or increase regularization to... |
| 45 | High | Organic/Direct | H30 | Investigation | Check ad platform for campaign changes, budget shifts, or tr... |
| 46 | High | Organic/Direct | H60 | Model Calibration | Retrain with p5/p95 quantiles, or increase regularization to... |
| 47 | High | Organic/Direct | H60 | Investigation | Check ad platform for campaign changes, budget shifts, or tr... |
| 48 | High | Organic_Search | H30 | Model Calibration | Retrain with p5/p95 quantiles, or increase regularization to... |
| 49 | High | Organic_Search | H60 | Model Calibration | Retrain with p5/p95 quantiles, or increase regularization to... |
| 50 | High | Organic_Search | H60 | Investigation | Check ad platform for campaign changes, budget shifts, or tr... |
| 51 | High | Organic_Search | H90 | Investigation | Check ad platform for campaign changes, budget shifts, or tr... |
| 52 | High | Organic_Search_Bing | H30 | Model Calibration | Retrain with p5/p95 quantiles, or increase regularization to... |
| 53 | High | Organic_Search_Bing | H30 | Investigation | Check ad platform for campaign changes, budget shifts, or tr... |
| 54 | High | Organic_Search_Bing | H60 | Model Calibration | Retrain with p5/p95 quantiles, or increase regularization to... |
| 55 | High | Organic_Search_Bing | H60 | Investigation | Check ad platform for campaign changes, budget shifts, or tr... |
| 56 | High | Organic_Search_Bing | H90 | Model Calibration | Retrain with p5/p95 quantiles, or increase regularization to... |
| 57 | High | Organic_Search_Bing | H90 | Investigation | Check ad platform for campaign changes, budget shifts, or tr... |
| 58 | High | Organic_Social | H30 | Model Calibration | Retrain with p5/p95 quantiles, or increase regularization to... |
| 59 | High | Organic_Social | H30 | Investigation | Check ad platform for campaign changes, budget shifts, or tr... |
| 60 | High | Organic_Social | H60 | Model Calibration | Retrain with p5/p95 quantiles, or increase regularization to... |
| 61 | High | Organic_Social | H60 | Investigation | Check ad platform for campaign changes, budget shifts, or tr... |
| 62 | High | Organic_Social | H90 | Model Calibration | Retrain with p5/p95 quantiles, or increase regularization to... |
| 63 | High | Organic_Social | H90 | Investigation | Check ad platform for campaign changes, budget shifts, or tr... |
| 64 | High | Pmax | H30 | Model Calibration | Retrain with p5/p95 quantiles, or increase regularization to... |
| 65 | High | Pmax | H60 | Model Calibration | Retrain with p5/p95 quantiles, or increase regularization to... |
| 66 | High | Pmax | H90 | Model Calibration | Retrain with p5/p95 quantiles, or increase regularization to... |
| 67 | High | Remarketing_Brand | H60 | Model Calibration | Retrain with p5/p95 quantiles, or increase regularization to... |
| 68 | High | Remarketing_Brand | H60 | Investigation | Check ad platform for campaign changes, budget shifts, or tr... |
| 69 | High | Remarketing_Brand | H90 | Model Calibration | Retrain with p5/p95 quantiles, or increase regularization to... |
| 70 | High | Remarketing_DPA | H30 | Investigation | Check ad platform for campaign changes, budget shifts, or tr... |
| 71 | High | Remarketing_DPA | H60 | Model Calibration | Retrain with p5/p95 quantiles, or increase regularization to... |
| 72 | High | Remarketing_DPA | H60 | Investigation | Check ad platform for campaign changes, budget shifts, or tr... |
| 73 | High | Remarketing_DPA | H90 | Model Calibration | Retrain with p5/p95 quantiles, or increase regularization to... |
| 74 | High | Remarketing_DPA | H90 | Investigation | Check ad platform for campaign changes, budget shifts, or tr... |
| 75 | High | Search | H30 | Investigation | Check ad platform for campaign changes, budget shifts, or tr... |
| 76 | High | Search | H60 | Model Calibration | Retrain with p5/p95 quantiles, or increase regularization to... |
| 77 | High | Search | H60 | Investigation | Check ad platform for campaign changes, budget shifts, or tr... |
| 78 | High | Search | H90 | Model Calibration | Retrain with p5/p95 quantiles, or increase regularization to... |
| 79 | High | Search | H90 | Investigation | Check ad platform for campaign changes, budget shifts, or tr... |
| 80 | High | Shopping | H30 | Investigation | Check ad platform for campaign changes, budget shifts, or tr... |
| 81 | High | Shopping | H60 | Model Calibration | Retrain with p5/p95 quantiles, or increase regularization to... |
| 82 | High | Shopping | H60 | Investigation | Check ad platform for campaign changes, budget shifts, or tr... |
| 83 | High | Shopping | H90 | Model Calibration | Retrain with p5/p95 quantiles, or increase regularization to... |
| 84 | Medium | Bing Ads | H30 | Budget Optimization | Increase daily budget by 25–50% and monitor ROAS over next 1... |
| 85 | Medium | Google Ads | H90 | Budget Optimization | Review audience targeting, pause underperforming ad groups, ... |
| 86 | Medium | Meta Ads | H30 | Budget Optimization | Increase daily budget by 25–50% and monitor ROAS over next 1... |
| 87 | Medium | Pmax | H30 | Budget Optimization | Review audience targeting, pause underperforming ad groups, ... |
| 88 | Medium | Pmax | H60 | Budget Optimization | Review audience targeting, pause underperforming ad groups, ... |
| 89 | Medium | Pmax | H90 | Budget Optimization | Review audience targeting, pause underperforming ad groups, ... |
| 90 | Medium | Remarketing_Brand | H30 | Budget Optimization | Increase daily budget by 25–50% and monitor ROAS over next 1... |
| 91 | Medium | Remarketing_DPA | H30 | Budget Optimization | Increase daily budget by 25–50% and monitor ROAS over next 1... |
| 92 | Medium | Search | H30 | Budget Optimization | Increase daily budget by 25–50% and monitor ROAS over next 1... |
| 93 | Medium | Search | H60 | Budget Optimization | Increase daily budget by 25–50% and monitor ROAS over next 1... |
| 94 | Strategic | Search | H30 | Strategic | Test budget multipliers between 0.8x and 1.2x over 2-week wi... |

