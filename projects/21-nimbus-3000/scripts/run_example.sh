#!/bin/bash

# Example: Quick benchmark with synthetic data
# This demonstrates the benchmark workflow with a small subset of experiments

set -e

echo "======================================"
echo "EXAMPLE BENCHMARK - Quick Demo"
echo "======================================"
echo ""
echo "This script runs a minimal benchmark to demonstrate the workflow:"
echo "  - 3 optimizers (SGD, Adam, AdamW)"
echo "  - 1 config per optimizer"
echo "  - 2 seeds"
echo "  - 10 epochs"
echo "  - Synthetic data"
echo ""
echo "Total time: ~5-10 minutes"
echo ""

cd "$(dirname "$0")/.."

# Configuration
EPOCHS=10
BATCH_SIZE=64
SEEDS=(42 123)
LOG_DIR="runs/example"
OPTIMIZERS=("sgd" "adam" "adamw")

# Clean previous runs
if [ -d "$LOG_DIR" ]; then
    echo "Cleaning previous example runs..."
    rm -rf "$LOG_DIR"
fi

mkdir -p "$LOG_DIR"

echo "Starting experiments..."
echo ""

# Run experiments
for optimizer in "${OPTIMIZERS[@]}"; do
    echo "Running: $optimizer"
    
    for seed in "${SEEDS[@]}"; do
        echo "  Seed: $seed"
        
        python src/train.py \
            --optimizer "$optimizer" \
            --config-id 0 \
            --epochs "$EPOCHS" \
            --batch-size "$BATCH_SIZE" \
            --seed "$seed" \
            --use-synthetic \
            --log-dir "$LOG_DIR" \
            --experiment-name "example_${optimizer}_seed${seed}"
        
        echo ""
    done
done

echo "======================================"
echo "Aggregating results..."
echo "======================================"
echo ""

python scripts/summarize.py \
    --runs "$LOG_DIR" \
    --out "${LOG_DIR}/summary.csv" \
    --out-detailed "${LOG_DIR}/detailed.csv"

echo ""
echo "======================================"
echo "Generating plots..."
echo "======================================"
echo ""

python scripts/plot_curves.py \
    --logs "$LOG_DIR" \
    --summary "${LOG_DIR}/summary.csv" \
    --out "${LOG_DIR}/figures"

echo ""
echo "======================================"
echo "Example benchmark complete!"
echo "======================================"
echo ""
echo "Results saved to: $LOG_DIR"
echo ""
echo "View results:"
echo "  - Summary:  cat ${LOG_DIR}/summary.csv"
echo "  - Detailed: cat ${LOG_DIR}/detailed.csv"
echo "  - Plots:    ls ${LOG_DIR}/figures/"
echo ""
echo "Next steps:"
echo "  1. Review the plots in ${LOG_DIR}/figures/"
echo "  2. Check the summary table: ${LOG_DIR}/summary.csv"
echo "  3. Run the full benchmark: bash scripts/run_grid.sh"
echo ""
