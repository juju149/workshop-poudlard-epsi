# 🚀 QUICKSTART - Nimbus 3000

Quick guide to get started with the optimizer benchmark.

## Prerequisites

- Python 3.10+
- 8GB RAM (16GB recommended)
- GPU with CUDA (recommended but not required)

## Installation

```bash
# Navigate to project directory
cd projects/21-nimbus-3000

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Quick Test (5 minutes)

Run a smoke test to verify everything works:

```bash
bash tests/smoke_test.sh
```

This will:
- Train each optimizer for 2 epochs with synthetic data
- Verify all scripts work correctly
- Clean up temporary files

## Single Experiment (10 minutes)

Train with one optimizer:

```bash
python src/train.py \
  --optimizer adam \
  --config-id 0 \
  --epochs 10 \
  --use-synthetic \
  --seed 42
```

Results will be saved to `runs/logs/`.

## Full Benchmark (several hours)

⚠️ **Warning**: This runs 140 experiments (7 optimizers × 4 configs × 5 seeds)

### Option 1: With real data

First, ensure you have the dataset from project 20:

```bash
# Check if data exists
ls ../../20-is-it-you-harry/data/train/

# Run benchmark
bash scripts/run_grid.sh
```

### Option 2: With synthetic data (for testing)

```bash
# Edit run_grid.sh and set:
USE_SYNTHETIC="--use-synthetic"

# Run benchmark
bash scripts/run_grid.sh
```

## Analyze Results

After running experiments:

```bash
# 1. Aggregate results
python scripts/summarize.py \
  --runs runs/logs \
  --out reports/tables/summary.csv

# 2. Generate plots
python scripts/plot_curves.py \
  --logs runs/logs \
  --summary reports/tables/summary.csv \
  --out reports/figures
```

## View Results

- **Summary table**: `reports/tables/summary.csv`
- **Detailed results**: `reports/tables/detailed.csv`
- **Plots**: `reports/figures/*.png`
- **Individual logs**: `runs/logs/*.json`

## Customization

### Change number of epochs

```bash
python src/train.py --optimizer adam --epochs 100 ...
```

### Use different batch size

```bash
python src/train.py --optimizer adam --batch-size 128 ...
```

### Disable data augmentation

```bash
python src/train.py --optimizer adam --no-augment ...
```

### Change early stopping patience

```bash
python src/train.py --optimizer adam --patience 15 ...
```

## Troubleshooting

### CUDA out of memory

Reduce batch size:
```bash
python src/train.py --batch-size 32 ...
```

### Adan optimizer not found

Install it:
```bash
pip install adan-pytorch
```

Or skip it by removing from `run_grid.sh`.

### Dataset not found

Either:
1. Use synthetic data: `--use-synthetic`
2. Download/create the dataset in `../../20-is-it-you-harry/data/`

## Next Steps

1. Review the paper template: `reports/paper.md`
2. Fill in your experimental results
3. Generate PDF: Use pandoc or your favorite Markdown to PDF converter

## Support

For issues, check:
- Project README: `README.md`
- Paper methodology: `reports/paper.md`
- Source code documentation: `src/*.py`
