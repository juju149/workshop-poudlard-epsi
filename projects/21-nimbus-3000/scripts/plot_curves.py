"""
Generate plots and visualizations from benchmark results.
"""

import argparse
import json
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# Set style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10


def plot_training_curves(log_dir, output_dir):
    """
    Plot training curves for all experiments.
    
    Args:
        log_dir: Directory containing experiment logs
        output_dir: Directory to save plots
    """
    log_dir = Path(log_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Group by optimizer
    optimizer_logs = {}
    
    for log_file in log_dir.glob('*.json'):
        if '_results' in log_file.name:
            continue
        
        with open(log_file, 'r') as f:
            data = json.load(f)
        
        # Extract optimizer name from filename
        parts = log_file.stem.split('_')
        optimizer = parts[0]
        
        if optimizer not in optimizer_logs:
            optimizer_logs[optimizer] = []
        
        optimizer_logs[optimizer].append({
            'name': log_file.stem,
            'data': pd.DataFrame(data)
        })
    
    # Plot for each optimizer
    for optimizer, logs in optimizer_logs.items():
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle(f'{optimizer.upper()} - Training Curves', fontsize=16)
        
        # Plot training loss
        ax = axes[0, 0]
        for log in logs:
            df = log['data']
            ax.plot(df['epoch'], df['train_loss'], alpha=0.3, label=log['name'])
        ax.set_xlabel('Epoch')
        ax.set_ylabel('Training Loss')
        ax.set_title('Training Loss')
        ax.legend().set_visible(False)
        
        # Plot validation loss
        ax = axes[0, 1]
        for log in logs:
            df = log['data']
            ax.plot(df['epoch'], df['val_loss'], alpha=0.3)
        ax.set_xlabel('Epoch')
        ax.set_ylabel('Validation Loss')
        ax.set_title('Validation Loss')
        
        # Plot validation accuracy
        ax = axes[1, 0]
        for log in logs:
            df = log['data']
            ax.plot(df['epoch'], df['val_acc'], alpha=0.3)
        ax.set_xlabel('Epoch')
        ax.set_ylabel('Validation Accuracy')
        ax.set_title('Validation Accuracy')
        
        # Plot validation F1
        ax = axes[1, 1]
        for log in logs:
            df = log['data']
            ax.plot(df['epoch'], df['val_f1_macro'], alpha=0.3)
        ax.set_xlabel('Epoch')
        ax.set_ylabel('Validation F1 (macro)')
        ax.set_title('Validation F1 (macro)')
        
        plt.tight_layout()
        plt.savefig(output_dir / f'{optimizer}_training_curves.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    print(f"Training curves saved to: {output_dir}")


def plot_comparison(summary_csv, output_dir):
    """
    Create comparison plots across optimizers.
    
    Args:
        summary_csv: Path to summary CSV file
        output_dir: Directory to save plots
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    df = pd.read_csv(summary_csv)
    
    # Get best config per optimizer
    best_configs = df.loc[df.groupby('optimizer')['test_acc_mean'].idxmax()]
    best_configs = best_configs.sort_values('test_acc_mean', ascending=False)
    
    # 1. Accuracy comparison
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x = np.arange(len(best_configs))
    bars = ax.bar(x, best_configs['test_acc_mean'], yerr=best_configs['test_acc_std'],
                  capsize=5, alpha=0.7)
    
    # Color bars
    colors = plt.cm.viridis(np.linspace(0, 1, len(best_configs)))
    for bar, color in zip(bars, colors):
        bar.set_color(color)
    
    ax.set_xlabel('Optimizer', fontsize=12)
    ax.set_ylabel('Test Accuracy', fontsize=12)
    ax.set_title('Optimizer Comparison - Test Accuracy', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(best_configs['optimizer'], rotation=45, ha='right')
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'accuracy_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. F1 Score comparison
    fig, ax = plt.subplots(figsize=(12, 6))
    
    bars = ax.bar(x, best_configs['test_f1_mean'], yerr=best_configs['test_f1_std'],
                  capsize=5, alpha=0.7)
    
    for bar, color in zip(bars, colors):
        bar.set_color(color)
    
    ax.set_xlabel('Optimizer', fontsize=12)
    ax.set_ylabel('Test F1 (macro)', fontsize=12)
    ax.set_title('Optimizer Comparison - F1 Score', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(best_configs['optimizer'], rotation=45, ha='right')
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'f1_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Training time comparison
    fig, ax = plt.subplots(figsize=(12, 6))
    
    bars = ax.bar(x, best_configs['time_mean'], yerr=best_configs['time_std'],
                  capsize=5, alpha=0.7)
    
    for bar, color in zip(bars, colors):
        bar.set_color(color)
    
    ax.set_xlabel('Optimizer', fontsize=12)
    ax.set_ylabel('Training Time (s)', fontsize=12)
    ax.set_title('Optimizer Comparison - Training Time', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(best_configs['optimizer'], rotation=45, ha='right')
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'time_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 4. Accuracy vs Time scatter
    fig, ax = plt.subplots(figsize=(10, 8))
    
    for i, row in best_configs.iterrows():
        ax.scatter(row['time_mean'], row['test_acc_mean'], 
                  s=200, alpha=0.7, label=row['optimizer'])
        ax.errorbar(row['time_mean'], row['test_acc_mean'],
                   xerr=row['time_std'], yerr=row['test_acc_std'],
                   fmt='none', alpha=0.3)
    
    ax.set_xlabel('Training Time (s)', fontsize=12)
    ax.set_ylabel('Test Accuracy', fontsize=12)
    ax.set_title('Accuracy vs Training Time Trade-off', fontsize=14)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'accuracy_vs_time.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 5. Heatmap of all configurations
    pivot = df.pivot_table(
        values='test_acc_mean',
        index='optimizer',
        columns='config_id',
        aggfunc='mean'
    )
    
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(pivot, annot=True, fmt='.4f', cmap='YlGnBu', ax=ax, cbar_kws={'label': 'Test Accuracy'})
    ax.set_title('Test Accuracy Heatmap - All Configurations', fontsize=14)
    ax.set_xlabel('Configuration ID', fontsize=12)
    ax.set_ylabel('Optimizer', fontsize=12)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'accuracy_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Comparison plots saved to: {output_dir}")


def main():
    parser = argparse.ArgumentParser(description='Generate plots from benchmark results')
    
    parser.add_argument('--logs', type=str, default='runs/logs',
                       help='Directory containing experiment logs')
    parser.add_argument('--summary', type=str, default='reports/tables/summary.csv',
                       help='Path to summary CSV file')
    parser.add_argument('--out', type=str, default='reports/figures',
                       help='Output directory for plots')
    
    args = parser.parse_args()
    
    print("Generating plots...")
    
    # Training curves
    if Path(args.logs).exists():
        print("Creating training curves...")
        plot_training_curves(args.logs, args.out)
    
    # Comparison plots
    if Path(args.summary).exists():
        print("Creating comparison plots...")
        plot_comparison(args.summary, args.out)
    else:
        print(f"Summary file not found: {args.summary}")
        print("Run summarize.py first to generate the summary.")
    
    print("Done!")


if __name__ == '__main__':
    main()
