"""
Utility functions for training, evaluation, and logging.
"""

import os
import random
import time
import json
import yaml
from pathlib import Path
import numpy as np
import torch
from sklearn.metrics import accuracy_score, f1_score, classification_report
import matplotlib.pyplot as plt
import seaborn as sns


def set_seed(seed=42):
    """
    Set random seeds for reproducibility.
    
    Args:
        seed: Random seed value
    """
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    print(f"Random seed set to: {seed}")


def get_device():
    """
    Get the best available device (CUDA > MPS > CPU).
    
    Returns:
        torch.device
    """
    if torch.cuda.is_available():
        device = torch.device('cuda')
        print(f"Using CUDA: {torch.cuda.get_device_name(0)}")
    elif torch.backends.mps.is_available():
        device = torch.device('mps')
        print("Using MPS (Apple Silicon)")
    else:
        device = torch.device('cpu')
        print("Using CPU")
    return device


def count_parameters(model):
    """
    Count total and trainable parameters in a model.
    
    Args:
        model: PyTorch model
    
    Returns:
        Dictionary with parameter counts
    """
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    
    return {
        'total': total_params,
        'trainable': trainable_params,
        'non_trainable': total_params - trainable_params
    }


def save_config(config, path):
    """
    Save configuration to YAML file.
    
    Args:
        config: Configuration dictionary
        path: Output file path
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
    
    print(f"Configuration saved to: {path}")


def load_config(path):
    """
    Load configuration from YAML file.
    
    Args:
        path: Configuration file path
    
    Returns:
        Configuration dictionary
    """
    with open(path, 'r') as f:
        config = yaml.safe_load(f)
    return config


def compute_metrics(y_true, y_pred):
    """
    Compute classification metrics.
    
    Args:
        y_true: Ground truth labels
        y_pred: Predicted labels
    
    Returns:
        Dictionary with metrics
    """
    accuracy = accuracy_score(y_true, y_pred)
    f1_macro = f1_score(y_true, y_pred, average='macro')
    f1_weighted = f1_score(y_true, y_pred, average='weighted')
    
    return {
        'accuracy': accuracy,
        'f1_macro': f1_macro,
        'f1_weighted': f1_weighted
    }


class AverageMeter:
    """Computes and stores the average and current value."""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0
    
    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


class Timer:
    """Simple timer utility."""
    
    def __init__(self):
        self.start_time = None
        self.elapsed = 0
    
    def start(self):
        """Start the timer."""
        self.start_time = time.time()
    
    def stop(self):
        """Stop the timer and return elapsed time."""
        if self.start_time is not None:
            self.elapsed = time.time() - self.start_time
            self.start_time = None
        return self.elapsed
    
    def get_elapsed(self):
        """Get elapsed time without stopping."""
        if self.start_time is not None:
            return time.time() - self.start_time
        return self.elapsed


class EarlyStopping:
    """Early stopping utility to stop training when validation loss stops improving."""
    
    def __init__(self, patience=10, min_delta=0.0, mode='min'):
        """
        Args:
            patience: Number of epochs to wait before stopping
            min_delta: Minimum change to qualify as improvement
            mode: 'min' for loss, 'max' for accuracy
        """
        self.patience = patience
        self.min_delta = min_delta
        self.mode = mode
        self.counter = 0
        self.best_score = None
        self.early_stop = False
        
    def __call__(self, score):
        """
        Check if training should stop.
        
        Args:
            score: Current validation score
        
        Returns:
            True if training should stop, False otherwise
        """
        if self.best_score is None:
            self.best_score = score
            return False
        
        if self.mode == 'min':
            improved = score < (self.best_score - self.min_delta)
        else:
            improved = score > (self.best_score + self.min_delta)
        
        if improved:
            self.best_score = score
            self.counter = 0
        else:
            self.counter += 1
            if self.counter >= self.patience:
                self.early_stop = True
                return True
        
        return False


class MetricsLogger:
    """Logger for training metrics."""
    
    def __init__(self, log_dir, experiment_name):
        """
        Args:
            log_dir: Directory to save logs
            experiment_name: Name of the experiment
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.experiment_name = experiment_name
        self.log_file = self.log_dir / f"{experiment_name}.json"
        self.metrics = []
    
    def log(self, epoch, metrics):
        """
        Log metrics for an epoch.
        
        Args:
            epoch: Epoch number
            metrics: Dictionary of metrics
        """
        entry = {'epoch': epoch, **metrics}
        self.metrics.append(entry)
        
        # Save to file
        with open(self.log_file, 'w') as f:
            json.dump(self.metrics, f, indent=2)
    
    def get_metrics(self):
        """Get all logged metrics."""
        return self.metrics


def format_time(seconds):
    """
    Format seconds into human-readable time string.
    
    Args:
        seconds: Time in seconds
    
    Returns:
        Formatted time string
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"


if __name__ == "__main__":
    # Test utilities
    print("Testing utilities...")
    
    # Test seed setting
    set_seed(42)
    
    # Test device
    device = get_device()
    
    # Test timer
    timer = Timer()
    timer.start()
    time.sleep(0.1)
    elapsed = timer.stop()
    print(f"Timer test: {elapsed:.3f}s")
    
    # Test early stopping
    early_stop = EarlyStopping(patience=3)
    for i, loss in enumerate([1.0, 0.9, 0.8, 0.85, 0.84, 0.83, 0.82]):
        if early_stop(loss):
            print(f"Early stopping triggered at iteration {i}")
            break
    
    print("✓ Utilities test passed!")
