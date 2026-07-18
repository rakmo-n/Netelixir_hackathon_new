# NETelixir Hackathon Submission

Probabilistic revenue/ROAS forecasting for ad-spend campaigns, using
quantile HistGradientBoostingRegressor models (p10/p50/p90) trained per
platform and per campaign type, over 30/60/90-day horizons.

Python version: 3.11 (see `requirements.txt` for pinned library versions).

## Run it

```bash
./run.sh ./data ./pickle/model.pkl ./output/predictions.csv
```

or with no arguments (uses the same defaults):

```bash
./run.sh
```

This does two things, in order:
1. `src/generate_features.py` builds the feature matrix the model needs from whatever CSVs are in `data/`.
2. `src/predict.py` loads the already-trained `pickle/model.pkl` and writes predictions — **no retraining happens here.**

## Repository layout

```
run.sh                  # entry point (see above)
requirements.txt        # pinned dependencies
data/                   # sample input data (overwritten with held-out test data at grading time)
pickle/model.pkl        # trained model bundle (126 quantile models — see below)
src/
  generate_features.py  # step (a): raw data -> features.parquet
  model_common.py        # shared feature-matrix logic used by training AND prediction
  predict.py             # step (b): features.parquet + model.pkl -> predictions.csv
  train_model.py          # OFFLINE ONLY — regenerates pickle/model.pkl. Not called by run.sh.
project/                 # original 9-stage analysis (EDA, baselines, budget sim, dashboard,
                          # explanation layer, report, recommendations) — supplementary,
                          # not part of the graded pipeline.
```

## Input data schema

`data/` is scanned for `*.csv` files and each is classified by its columns
(not its filename), so the grader can drop in differently-named files with
the same schema:

- **Ad-spend file** — must have `date` and `spend` columns. Also expected:
  `platform`, `channel_grouping`.
- **Orders/revenue file** — must have `order_date` and `revenue` columns.
  Also expected: `platform`, `channel_grouping`.

Both categories are required; multiple files of the same category are
concatenated. A grain (platform or campaign type) needs at least ~200 days
of daily history for the model to produce any forecasts for it — this
mirrors the minimum used during training.

## Output format

`output/predictions.csv`, one row per (grain, forecast date, horizon):

| column | meaning |
|---|---|
| `grain_type` | `platform` or `campaign_type` |
| `grain` | e.g. `Google Ads`, `Search`, `Pmax` |
| `forecast_origin_date` | the date the forecast is made *from* |
| `horizon_days` | 30, 60, or 90 |
| `planned_spend` | cumulative spend over the horizon (observed, from the data provided) |
| `p10_revenue` / `p50_revenue` / `p90_revenue` | forecast revenue quantiles |
| `p10_roas` / `p50_roas` / `p90_roas` | derived: revenue quantile / planned_spend |
| `actual_revenue` | observed revenue over the horizon, if fully contained in the data provided (for scoring/sanity-check only — never used as a model input) |

> **This output format is my best-effort reconstruction from the original
> analysis notebook's own schema (`project/stage4_probabilistic_forecasting`),
> since the exact column contract announced at launch wasn't available when
> this was packaged.** Confirm against the organizers' announced format and
> adjust `src/predict.py`'s output columns if they differ — the row-level
> grain/date/horizon structure should still hold.

## Regenerating the model

`pickle/model.pkl` is already trained and committed. If you get new
training data and want to retrain:

```bash
python src/generate_features.py --data-dir ./data --out features.parquet
python src/train_model.py --features features.parquet --out pickle/model.pkl
```

`train_model.py` is **not** part of `run.sh` and will not run during
grading — the contract is "load the trained model," not "train it."

## Known caveats / things to double check before submitting

- **`pickle/model.pkl` is ~70MB.** That's under GitHub's 100MB hard limit,
  so a plain `git add`/`git push` will work, but confirm it isn't silently
  excluded by a `.gitignore` rule and doesn't need Git LFS (the grading
  pipeline does a plain `git clone` and cannot pull LFS objects unless
  they explicitly support it — confirm with organizers if unsure).
- The model was trained and pickled with scikit-learn `1.8.0`, pandas
  `3.0.2`, numpy `2.4.4` (pinned in `requirements.txt`). Unpickling under
  different versions is the most common cause of submission failures —
  don't change these versions without retraining.
- No internet access is required or used at run time.
- Every random process (model training) is seeded (`random_state=42`).
