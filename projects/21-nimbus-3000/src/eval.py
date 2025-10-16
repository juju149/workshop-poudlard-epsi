"""
Evaluate trained models and aggregate results.
"""

import argparse
import json
from pathlib import Path
import torch
import torch.nn as nn
from models.net import get_model
from datasets.loader import get_dataloaders, get_synthetic_dataloaders
from utils import set_seed, get_device, compute_metrics


def evaluate_model(checkpoint_path, data_root, use_synthetic=False, batch_size=64):
    """
    Evaluate a trained model on test set.
    
    Args:
        checkpoint_path: Path to model checkpoint
        data_root: Path to dataset
        use_synthetic: Whether to use synthetic data
        batch_size: Batch size for evaluation
    
    Returns:
        Dictionary with evaluation metrics
    """
    # Load checkpoint
    checkpoint = torch.load(checkpoint_path, map_location='cpu')
    config = checkpoint['config']
    
    # Set seed
    set_seed(config['seed'])
    
    # Device
    device = get_device()
    
    # Create dataloaders
    if use_synthetic or config.get('use_synthetic', False):
        dataloaders, _ = get_synthetic_dataloaders(
            batch_size=batch_size,
            input_size=config['input_size'],
            num_classes=config['num_classes']
        )
    else:
        dataloaders, _ = get_dataloaders(
            data_root=data_root,
            batch_size=batch_size,
            input_size=config['input_size'],
            augment=False
        )
    
    # Create model
    model = get_model(
        num_classes=config['num_classes'],
        input_size=config['input_size']
    )
    model.load_state_dict(checkpoint['model_state_dict'])
    model = model.to(device)
    model.eval()
    
    # Evaluate
    criterion = nn.CrossEntropyLoss()
    all_preds = []
    all_labels = []
    total_loss = 0
    
    with torch.no_grad():
        for images, labels in dataloaders['test']:
            images, labels = images.to(device), labels.to(device)
            
            outputs = model(images)
            loss = criterion(outputs, labels)
            
            _, preds = torch.max(outputs, 1)
            
            total_loss += loss.item() * images.size(0)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
    
    # Compute metrics
    metrics = compute_metrics(all_labels, all_preds)
    metrics['loss'] = total_loss / len(dataloaders['test'].dataset)
    
    return metrics


def main():
    parser = argparse.ArgumentParser(description='Evaluate trained model')
    
    parser.add_argument('--checkpoint', type=str, required=True,
                       help='Path to model checkpoint')
    parser.add_argument('--data-root', type=str, default='../../20-is-it-you-harry/data',
                       help='Path to dataset root')
    parser.add_argument('--use-synthetic', action='store_true',
                       help='Use synthetic data')
    parser.add_argument('--batch-size', type=int, default=64,
                       help='Batch size for evaluation')
    
    args = parser.parse_args()
    
    print(f"Evaluating model: {args.checkpoint}")
    
    metrics = evaluate_model(
        checkpoint_path=args.checkpoint,
        data_root=args.data_root,
        use_synthetic=args.use_synthetic,
        batch_size=args.batch_size
    )
    
    print("\nEvaluation Results:")
    print(f"  Loss: {metrics['loss']:.4f}")
    print(f"  Accuracy: {metrics['accuracy']:.4f}")
    print(f"  F1 (macro): {metrics['f1_macro']:.4f}")
    print(f"  F1 (weighted): {metrics['f1_weighted']:.4f}")


if __name__ == '__main__':
    main()
