"""
Aggregate results from multiple experiment runs.
"""

import argparse
import json
from pathlib import Path
import pandas as pd
import numpy as np


def load_experiment_results(log_dir):
    """
    Load all experiment results from log directory.
    
    Args:
        log_dir: Directory containing experiment logs
    
    Returns:
        List of result dictionaries
    """
    log_dir = Path(log_dir)
    results = []
    
    for result_file in log_dir.glob('*_results.json'):
        with open(result_file, 'r') as f:
            result = json.load(f)
            results.append(result)
    
    return results


def aggregate_results(results):
    """
    Aggregate results by optimizer and configuration.
    
    Args:
        results: List of result dictionaries
    
    Returns:
        DataFrame with aggregated statistics
    """
    # Extract relevant information
    data = []
    
    for result in results:
        config = result['config']
        
        row = {
            'optimizer': config['optimizer'],
            'config_id': config['config_id'],
            'seed': config['seed'],
            'test_accuracy': result['test_accuracy'],
            'test_f1_macro': result['test_f1_macro'],
            'test_loss': result['test_loss'],
            'best_epoch': result['best_epoch'],
            'total_time': result['total_time'],
            'avg_epoch_time': result['avg_epoch_time'],
        }
        
        # Add optimizer-specific parameters
        for key, value in config['optimizer_params'].items():
            if isinstance(value, (int, float)):
                row[f'param_{key}'] = value
            else:
                row[f'param_{key}'] = str(value)
        
        data.append(row)
    
    df = pd.DataFrame(data)
    
    # Group by optimizer and config
    grouped = df.groupby(['optimizer', 'config_id'])
    
    # Compute statistics
    stats = []
    
    for (opt, cfg), group in grouped:
        stat = {
            'optimizer': opt,
            'config_id': cfg,
            'num_runs': len(group),
            'test_acc_mean': group['test_accuracy'].mean(),
            'test_acc_std': group['test_accuracy'].std(),
            'test_f1_mean': group['test_f1_macro'].mean(),
            'test_f1_std': group['test_f1_macro'].std(),
            'test_loss_mean': group['test_loss'].mean(),
            'test_loss_std': group['test_loss'].std(),
            'epochs_mean': group['best_epoch'].mean(),
            'epochs_std': group['best_epoch'].std(),
            'time_mean': group['total_time'].mean(),
            'time_std': group['total_time'].std(),
            'time_per_epoch_mean': group['avg_epoch_time'].mean(),
        }
        
        # Add parameter values (from first run)
        first_row = group.iloc[0]
        for col in group.columns:
            if col.startswith('param_'):
                stat[col] = first_row[col]
        
        stats.append(stat)
    
    stats_df = pd.DataFrame(stats)
    stats_df = stats_df.sort_values(['optimizer', 'test_acc_mean'], ascending=[True, False])
    
    return df, stats_df


def print_summary(stats_df):
    """Print a summary table of results."""
    print("\n" + "=" * 80)
    print("OPTIMIZER BENCHMARK SUMMARY")
    print("=" * 80)
    
    for optimizer in stats_df['optimizer'].unique():
        opt_data = stats_df[stats_df['optimizer'] == optimizer]
        
        print(f"\n{optimizer.upper()}")
        print("-" * 80)
        
        for _, row in opt_data.iterrows():
            print(f"  Config {int(row['config_id'])}: "
                  f"Acc={row['test_acc_mean']:.4f}±{row['test_acc_std']:.4f} | "
                  f"F1={row['test_f1_mean']:.4f}±{row['test_f1_std']:.4f} | "
                  f"Loss={row['test_loss_mean']:.4f}±{row['test_loss_std']:.4f} | "
                  f"Epochs={row['epochs_mean']:.1f}±{row['epochs_std']:.1f} | "
                  f"Time={row['time_mean']:.1f}s")
    
    print("\n" + "=" * 80)
    print("BEST CONFIGURATIONS (by test accuracy)")
    print("=" * 80)
    
    best_per_optimizer = stats_df.loc[stats_df.groupby('optimizer')['test_acc_mean'].idxmax()]
    best_per_optimizer = best_per_optimizer.sort_values('test_acc_mean', ascending=False)
    
    for _, row in best_per_optimizer.iterrows():
        print(f"{row['optimizer']:12s} | "
              f"Acc={row['test_acc_mean']:.4f}±{row['test_acc_std']:.4f} | "
              f"F1={row['test_f1_mean']:.4f}±{row['test_f1_std']:.4f} | "
              f"Time={row['time_mean']:.1f}s")
    
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(description='Aggregate experiment results')
    
    parser.add_argument('--runs', type=str, default='runs/logs',
                       help='Directory containing experiment logs')
    parser.add_argument('--out', type=str, default='reports/tables/summary.csv',
                       help='Output CSV file')
    parser.add_argument('--out-detailed', type=str, default='reports/tables/detailed.csv',
                       help='Detailed output CSV file')
    
    args = parser.parse_args()
    
    print(f"Loading results from: {args.runs}")
    results = load_experiment_results(args.runs)
    
    if not results:
        print("No results found!")
        return
    
    print(f"Found {len(results)} experiment results")
    
    # Aggregate
    detailed_df, summary_df = aggregate_results(results)
    
    # Save to CSV
    output_path = Path(args.out)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    summary_df.to_csv(output_path, index=False)
    print(f"Summary saved to: {output_path}")
    
    detailed_path = Path(args.out_detailed)
    detailed_path.parent.mkdir(parents=True, exist_ok=True)
    detailed_df.to_csv(detailed_path, index=False)
    print(f"Detailed results saved to: {detailed_path}")
    
    # Print summary
    print_summary(summary_df)


if __name__ == '__main__':
    main()
