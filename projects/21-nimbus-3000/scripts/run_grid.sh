#!/bin/bash

# Run grid search for all optimizers
# This script executes the complete benchmark

set -e  # Exit on error

# Configuration
EPOCHS=50
BATCH_SIZE=64
SEEDS=(42 123 456 789 1024)
DATA_ROOT="../../20-is-it-you-harry/data"
LOG_DIR="runs/logs"
USE_SYNTHETIC=""  # Set to "--use-synthetic" to use synthetic data

# Optimizers to benchmark
OPTIMIZERS=("sgd" "adam" "adamw" "rmsprop" "adagrad" "adadelta" "adan")

# Number of configurations per optimizer
declare -A NUM_CONFIGS
NUM_CONFIGS["sgd"]=4
NUM_CONFIGS["adam"]=4
NUM_CONFIGS["adamw"]=4
NUM_CONFIGS["rmsprop"]=4
NUM_CONFIGS["adagrad"]=4
NUM_CONFIGS["adadelta"]=4
NUM_CONFIGS["adan"]=4

echo "======================================"
echo "OPTIMIZER BENCHMARK - NIMBUS 3000"
echo "======================================"
echo ""
echo "Configuration:"
echo "  Epochs: $EPOCHS"
echo "  Batch size: $BATCH_SIZE"
echo "  Seeds: ${SEEDS[*]}"
echo "  Optimizers: ${OPTIMIZERS[*]}"
echo "  Log directory: $LOG_DIR"
echo ""
echo "Starting benchmark..."
echo ""

# Create log directory
mkdir -p "$LOG_DIR"

# Total runs
TOTAL_RUNS=0
for opt in "${OPTIMIZERS[@]}"; do
    num_configs=${NUM_CONFIGS[$opt]}
    num_runs=$((num_configs * ${#SEEDS[@]}))
    TOTAL_RUNS=$((TOTAL_RUNS + num_runs))
done

echo "Total runs: $TOTAL_RUNS"
echo ""

CURRENT_RUN=0

# Run experiments
for optimizer in "${OPTIMIZERS[@]}"; do
    echo "======================================"
    echo "Running: $optimizer"
    echo "======================================"
    
    num_configs=${NUM_CONFIGS[$optimizer]}
    
    for config_id in $(seq 0 $((num_configs - 1))); do
        for seed in "${SEEDS[@]}"; do
            CURRENT_RUN=$((CURRENT_RUN + 1))
            
            echo ""
            echo "[$CURRENT_RUN/$TOTAL_RUNS] $optimizer - Config $config_id - Seed $seed"
            echo "--------------------------------------"
            
            # Run training
            python src/train.py \
                --optimizer "$optimizer" \
                --config-id "$config_id" \
                --epochs "$EPOCHS" \
                --batch-size "$BATCH_SIZE" \
                --seed "$seed" \
                --data-root "$DATA_ROOT" \
                --log-dir "$LOG_DIR" \
                $USE_SYNTHETIC
            
            echo ""
        done
    done
    
    echo ""
done

echo "======================================"
echo "Benchmark complete!"
echo "======================================"
echo ""
echo "Results saved to: $LOG_DIR"
echo ""
echo "Next steps:"
echo "  1. Aggregate results:"
echo "     python scripts/summarize.py --runs $LOG_DIR"
echo ""
echo "  2. Generate plots:"
echo "     python scripts/plot_curves.py --logs $LOG_DIR"
echo ""
