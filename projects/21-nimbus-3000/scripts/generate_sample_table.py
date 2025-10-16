"""
Generate sample results table for the paper.
This helps visualize what the final results table will look like.
"""

import pandas as pd
import numpy as np


def generate_sample_results():
    """Generate realistic sample results for demonstration."""
    
    # Sample data (these would be filled with real results after running experiments)
    optimizers = ['SGD', 'Adam', 'AdamW', 'RMSProp', 'Adagrad', 'Adadelta', 'Adan']
    
    # Simulate results (these are placeholders)
    np.random.seed(42)
    
    data = []
    for i, opt in enumerate(optimizers):
        # Simulate some variation in results
        base_acc = 0.85 + np.random.randn() * 0.05
        base_f1 = base_acc - 0.02
        base_loss = 0.4 + np.random.randn() * 0.1
        base_time = 200 + np.random.randn() * 50
        base_epoch = 25 + np.random.randint(-5, 10)
        
        data.append({
            'Optimizer': opt,
            'Test Accuracy': f"{base_acc:.4f} ± {0.01 + np.random.rand() * 0.01:.4f}",
            'Test F1 (macro)': f"{base_f1:.4f} ± {0.01 + np.random.rand() * 0.01:.4f}",
            'Test Loss': f"{base_loss:.4f} ± {0.05 + np.random.rand() * 0.05:.4f}",
            'Training Time (s)': f"{base_time:.0f} ± {20 + np.random.rand() * 10:.0f}",
            'Best Epoch': f"{base_epoch:.0f} ± {3 + np.random.rand() * 2:.0f}"
        })
    
    df = pd.DataFrame(data)
    return df


def print_markdown_table(df):
    """Print DataFrame as Markdown table."""
    print("\n## Sample Results Table (for paper)\n")
    print("Replace these values with actual results after running experiments.\n")
    print(df.to_markdown(index=False))
    print("\n")


def print_latex_table(df):
    """Print DataFrame as LaTeX table."""
    print("\n## LaTeX version (for academic papers)\n")
    latex_str = df.to_latex(index=False, escape=False)
    print(latex_str)
    print("\n")


def main():
    print("=" * 80)
    print("SAMPLE RESULTS TABLE GENERATOR")
    print("=" * 80)
    
    df = generate_sample_results()
    
    print_markdown_table(df)
    
    print("\nTo generate the actual results table:")
    print("1. Run the full benchmark: bash scripts/run_grid.sh")
    print("2. Aggregate results: python scripts/summarize.py")
    print("3. The summary.csv will contain the real data")
    print("4. Copy the best configurations to the paper")
    
    print("\n" + "=" * 80)


if __name__ == '__main__':
    main()
