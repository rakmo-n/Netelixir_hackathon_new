#!/usr/bin/env bash
set -euo pipefail

# Accept arguments, fall back to defaults for local runs
DATA_DIR="${1:-./data}"
MODEL_PATH="${2:-./pickle/model.pkl}"
OUTPUT_PATH="${3:-./output/predictions.csv}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
mkdir -p "$(dirname "$OUTPUT_PATH")"

# 1. Generate the features the model expects from whatever is in DATA_DIR
python3 "$SCRIPT_DIR/src/generate_features.py" \
    --data-dir "$DATA_DIR" \
    --out "$SCRIPT_DIR/features.parquet"

# 2. Load the pickled model (already trained — not retrained here) and predict
python3 "$SCRIPT_DIR/src/predict.py" \
    --features "$SCRIPT_DIR/features.parquet" \
    --model "$MODEL_PATH" \
    --output "$OUTPUT_PATH"

echo "Done. Predictions written to $OUTPUT_PATH"
