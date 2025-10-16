"""
Main training script for optimizer benchmarking.
"""

import argparse
import json
import time
from pathlib import Path
import torch
import torch.nn as nn
from torch.optim.lr_scheduler import CosineAnnealingLR

from models.net import get_model
from datasets.loader import get_dataloaders, get_synthetic_dataloaders
from optim_space import get_optimizer, get_optimizer_grid
from utils import (
    set_seed, get_device, count_parameters, save_config,
    AverageMeter, Timer, EarlyStopping, MetricsLogger,
    compute_metrics, format_time
)


def train_epoch(model, dataloader, criterion, optimizer, device, grad_clip=1.0):
    """Train for one epoch."""
    model.train()
    
    loss_meter = AverageMeter()
    acc_meter = AverageMeter()
    
    for images, labels in dataloader:
        images, labels = images.to(device), labels.to(device)
        
        # Forward pass
        outputs = model(images)
        loss = criterion(outputs, labels)
        
        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        
        # Gradient clipping
        if grad_clip > 0:
            torch.nn.utils.clip_grad_norm_(model.parameters(), grad_clip)
        
        optimizer.step()
        
        # Metrics
        _, preds = torch.max(outputs, 1)
        acc = (preds == labels).float().mean().item()
        
        loss_meter.update(loss.item(), images.size(0))
        acc_meter.update(acc, images.size(0))
    
    return {'loss': loss_meter.avg, 'accuracy': acc_meter.avg}


def validate(model, dataloader, criterion, device):
    """Validate the model."""
    model.eval()
    
    loss_meter = AverageMeter()
    all_preds = []
    all_labels = []
    
    with torch.no_grad():
        for images, labels in dataloader:
            images, labels = images.to(device), labels.to(device)
            
            # Forward pass
            outputs = model(images)
            loss = criterion(outputs, labels)
            
            # Predictions
            _, preds = torch.max(outputs, 1)
            
            loss_meter.update(loss.item(), images.size(0))
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
    
    # Compute metrics
    metrics = compute_metrics(all_labels, all_preds)
    metrics['loss'] = loss_meter.avg
    
    return metrics


def train(config):
    """Main training function."""
    
    # Set seed
    set_seed(config['seed'])
    
    # Device
    device = get_device()
    
    # Create dataloaders
    if config.get('use_synthetic', False):
        dataloaders, class_names = get_synthetic_dataloaders(
            batch_size=config['batch_size'],
            input_size=config['input_size'],
            num_classes=config['num_classes']
        )
    else:
        dataloaders, class_names = get_dataloaders(
            data_root=config['data_root'],
            batch_size=config['batch_size'],
            input_size=config['input_size'],
            augment=config.get('augment', True)
        )
    
    # Create model
    model = get_model(
        num_classes=config['num_classes'],
        input_size=config['input_size']
    )
    model = model.to(device)
    
    # Print model info
    params = count_parameters(model)
    print(f"Model parameters: {params['trainable']:,}")
    
    # Loss function
    criterion = nn.CrossEntropyLoss()
    
    # Optimizer
    optimizer = get_optimizer(
        config['optimizer'],
        model.parameters(),
        **config['optimizer_params']
    )
    
    # Learning rate scheduler
    if config.get('use_scheduler', True):
        scheduler = CosineAnnealingLR(
            optimizer,
            T_max=config['epochs'],
            eta_min=config.get('min_lr', 1e-6)
        )
    else:
        scheduler = None
    
    # Early stopping
    early_stopping = EarlyStopping(
        patience=config.get('patience', 10),
        mode='min'
    )
    
    # Metrics logger
    logger = MetricsLogger(
        log_dir=config['log_dir'],
        experiment_name=config['experiment_name']
    )
    
    # Training loop
    print(f"\nStarting training: {config['experiment_name']}")
    print(f"Optimizer: {config['optimizer']}")
    print(f"Parameters: {config['optimizer_params']}")
    print(f"Epochs: {config['epochs']}")
    print("-" * 60)
    
    best_val_loss = float('inf')
    best_epoch = 0
    total_timer = Timer()
    total_timer.start()
    
    for epoch in range(config['epochs']):
        epoch_timer = Timer()
        epoch_timer.start()
        
        # Train
        train_metrics = train_epoch(
            model, dataloaders['train'], criterion, optimizer, device,
            grad_clip=config.get('grad_clip', 1.0)
        )
        
        # Validate
        val_metrics = validate(model, dataloaders['val'], criterion, device)
        
        epoch_time = epoch_timer.stop()
        
        # Learning rate step
        if scheduler is not None:
            scheduler.step()
            current_lr = scheduler.get_last_lr()[0]
        else:
            current_lr = config['optimizer_params']['lr']
        
        # Log metrics
        metrics = {
            'train_loss': train_metrics['loss'],
            'train_acc': train_metrics['accuracy'],
            'val_loss': val_metrics['loss'],
            'val_acc': val_metrics['accuracy'],
            'val_f1_macro': val_metrics['f1_macro'],
            'lr': current_lr,
            'epoch_time': epoch_time
        }
        logger.log(epoch + 1, metrics)
        
        # Print progress
        print(f"Epoch {epoch+1:3d}/{config['epochs']} | "
              f"Train Loss: {train_metrics['loss']:.4f} | "
              f"Train Acc: {train_metrics['accuracy']:.4f} | "
              f"Val Loss: {val_metrics['loss']:.4f} | "
              f"Val Acc: {val_metrics['accuracy']:.4f} | "
              f"Val F1: {val_metrics['f1_macro']:.4f} | "
              f"Time: {format_time(epoch_time)}")
        
        # Save best model
        if val_metrics['loss'] < best_val_loss:
            best_val_loss = val_metrics['loss']
            best_epoch = epoch + 1
            
            checkpoint_path = Path(config['log_dir']) / f"{config['experiment_name']}_best.pth"
            torch.save({
                'epoch': epoch + 1,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'val_loss': val_metrics['loss'],
                'val_acc': val_metrics['accuracy'],
                'config': config
            }, checkpoint_path)
        
        # Early stopping
        if early_stopping(val_metrics['loss']):
            print(f"\nEarly stopping triggered at epoch {epoch+1}")
            break
    
    total_time = total_timer.stop()
    
    # Final evaluation on test set
    print("\n" + "=" * 60)
    print("Evaluating on test set...")
    
    # Load best model
    checkpoint_path = Path(config['log_dir']) / f"{config['experiment_name']}_best.pth"
    checkpoint = torch.load(checkpoint_path)
    model.load_state_dict(checkpoint['model_state_dict'])
    
    test_metrics = validate(model, dataloaders['test'], criterion, device)
    
    print(f"Test Loss: {test_metrics['loss']:.4f}")
    print(f"Test Accuracy: {test_metrics['accuracy']:.4f}")
    print(f"Test F1 (macro): {test_metrics['f1_macro']:.4f}")
    
    # Save final results
    final_results = {
        'config': config,
        'best_epoch': best_epoch,
        'best_val_loss': best_val_loss,
        'test_loss': test_metrics['loss'],
        'test_accuracy': test_metrics['accuracy'],
        'test_f1_macro': test_metrics['f1_macro'],
        'test_f1_weighted': test_metrics['f1_weighted'],
        'total_time': total_time,
        'avg_epoch_time': total_time / (epoch + 1)
    }
    
    results_path = Path(config['log_dir']) / f"{config['experiment_name']}_results.json"
    with open(results_path, 'w') as f:
        json.dump(final_results, f, indent=2)
    
    print(f"\nTotal training time: {format_time(total_time)}")
    print(f"Average epoch time: {format_time(total_time / (epoch + 1))}")
    print(f"Best epoch: {best_epoch}")
    print(f"Results saved to: {results_path}")
    print("=" * 60)
    
    return final_results


def main():
    parser = argparse.ArgumentParser(description='Train model with specified optimizer')
    
    # Optimizer selection
    parser.add_argument('--optimizer', type=str, required=True,
                       choices=['sgd', 'adam', 'adamw', 'rmsprop', 'adagrad', 'adadelta', 'adan'],
                       help='Optimizer to use')
    parser.add_argument('--config-id', type=int, default=0,
                       help='Configuration ID from optimizer grid (0-3)')
    
    # Training parameters
    parser.add_argument('--epochs', type=int, default=50,
                       help='Number of epochs')
    parser.add_argument('--batch-size', type=int, default=64,
                       help='Batch size')
    parser.add_argument('--seed', type=int, default=42,
                       help='Random seed')
    
    # Data parameters
    parser.add_argument('--data-root', type=str, default='../../20-is-it-you-harry/data',
                       help='Path to dataset root')
    parser.add_argument('--use-synthetic', action='store_true',
                       help='Use synthetic data for testing')
    parser.add_argument('--input-size', type=int, default=128,
                       help='Input image size')
    parser.add_argument('--num-classes', type=int, default=10,
                       help='Number of classes')
    
    # Training options
    parser.add_argument('--no-augment', action='store_true',
                       help='Disable data augmentation')
    parser.add_argument('--no-scheduler', action='store_true',
                       help='Disable learning rate scheduler')
    parser.add_argument('--patience', type=int, default=10,
                       help='Early stopping patience')
    parser.add_argument('--grad-clip', type=float, default=1.0,
                       help='Gradient clipping value (0 to disable)')
    
    # Logging
    parser.add_argument('--log-dir', type=str, default='runs/logs',
                       help='Directory for logs')
    parser.add_argument('--experiment-name', type=str, default=None,
                       help='Experiment name (auto-generated if not provided)')
    
    args = parser.parse_args()
    
    # Get optimizer configuration
    optimizer_grid = get_optimizer_grid(args.optimizer)
    if args.config_id >= len(optimizer_grid):
        raise ValueError(f"Config ID {args.config_id} out of range for {args.optimizer} "
                        f"(max: {len(optimizer_grid)-1})")
    
    optimizer_params = optimizer_grid[args.config_id]
    
    # Generate experiment name if not provided
    if args.experiment_name is None:
        param_str = "_".join([f"{k}={v}" for k, v in optimizer_params.items()])
        args.experiment_name = f"{args.optimizer}_cfg{args.config_id}_seed{args.seed}"
    
    # Create configuration
    config = {
        'optimizer': args.optimizer,
        'optimizer_params': optimizer_params,
        'config_id': args.config_id,
        'epochs': args.epochs,
        'batch_size': args.batch_size,
        'seed': args.seed,
        'data_root': args.data_root,
        'use_synthetic': args.use_synthetic,
        'input_size': args.input_size,
        'num_classes': args.num_classes,
        'augment': not args.no_augment,
        'use_scheduler': not args.no_scheduler,
        'patience': args.patience,
        'grad_clip': args.grad_clip,
        'log_dir': args.log_dir,
        'experiment_name': args.experiment_name
    }
    
    # Save configuration
    save_config(config, Path(args.log_dir) / f"{args.experiment_name}_config.yaml")
    
    # Train
    results = train(config)
    
    return results


if __name__ == '__main__':
    main()
