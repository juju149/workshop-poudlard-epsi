#!/bin/bash

# Smoke test - Quick validation that the benchmark system works
# Runs 1 epoch with synthetic data for each optimizer

set -e

echo "======================================"
echo "SMOKE TEST - Nimbus 3000 Benchmark"
echo "======================================"
echo ""

cd "$(dirname "$0")/.."

# Test parameters
EPOCHS=2
BATCH_SIZE=32
SEED=42

echo "Testing optimizer configurations..."
echo ""

# Test each optimizer with config 0 and synthetic data
for optimizer in sgd adam adamw rmsprop adagrad adadelta; do
    echo "Testing: $optimizer"
    python src/train.py \
        --optimizer "$optimizer" \
        --config-id 0 \
        --epochs "$EPOCHS" \
        --batch-size "$BATCH_SIZE" \
        --seed "$SEED" \
        --use-synthetic \
        --log-dir runs/smoke_test \
        --experiment-name "smoke_${optimizer}" \
        > /dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        echo "  ✓ $optimizer passed"
    else
        echo "  ✗ $optimizer failed"
        exit 1
    fi
done

# Test Adan separately (might not be installed)
echo "Testing: adan"
python src/train.py \
    --optimizer adan \
    --config-id 0 \
    --epochs "$EPOCHS" \
    --batch-size "$BATCH_SIZE" \
    --seed "$SEED" \
    --use-synthetic \
    --log-dir runs/smoke_test \
    --experiment-name "smoke_adan" \
    > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "  ✓ adan passed"
else
    echo "  ⚠ adan failed (might not be installed)"
fi

echo ""
echo "Testing aggregation..."
python scripts/summarize.py \
    --runs runs/smoke_test \
    --out runs/smoke_test/summary.csv \
    --out-detailed runs/smoke_test/detailed.csv \
    > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "  ✓ Aggregation passed"
else
    echo "  ✗ Aggregation failed"
    exit 1
fi

echo ""
echo "Testing plotting..."
python scripts/plot_curves.py \
    --logs runs/smoke_test \
    --summary runs/smoke_test/summary.csv \
    --out runs/smoke_test/figures \
    > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "  ✓ Plotting passed"
else
    echo "  ✗ Plotting failed"
    exit 1
fi

echo ""
echo "======================================"
echo "✓ All smoke tests passed!"
echo "======================================"
echo ""
echo "Cleaning up..."
rm -rf runs/smoke_test

echo "Done!"
