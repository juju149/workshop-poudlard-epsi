"""
Data loading and preprocessing utilities.
"""

import os
from pathlib import Path
import torch
from torch.utils.data import DataLoader, Dataset
from torchvision import datasets, transforms
from PIL import Image
import numpy as np


# Character class names
CHARACTER_CLASSES = [
    'albus_dumbledore',
    'draco_malfoy',
    'hagrid',
    'harry_potter',
    'hermione_granger',
    'minerva_mcgonagall',
    'ron_weasley',
    'severus_snape',
    'sirius_black',
    'voldemort'
]


def get_transforms(input_size=128, augment=True):
    """
    Get image transforms for training and validation.
    
    Args:
        input_size: Target image size
        augment: Whether to apply data augmentation
    
    Returns:
        Dictionary with 'train' and 'val' transforms
    """
    if augment:
        train_transform = transforms.Compose([
            transforms.Resize((input_size, input_size)),
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomRotation(15),
            transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])
    else:
        train_transform = transforms.Compose([
            transforms.Resize((input_size, input_size)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])
    
    val_transform = transforms.Compose([
        transforms.Resize((input_size, input_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                           std=[0.229, 0.224, 0.225])
    ])
    
    return {'train': train_transform, 'val': val_transform}


def get_dataloaders(data_root, batch_size=64, input_size=128, 
                   augment=True, num_workers=4):
    """
    Create train, validation, and test dataloaders.
    
    Args:
        data_root: Root directory containing train/val/test folders
        batch_size: Batch size for dataloaders
        input_size: Target image size
        augment: Whether to apply data augmentation to training set
        num_workers: Number of worker processes for data loading
    
    Returns:
        Dictionary with 'train', 'val', and 'test' dataloaders
    """
    data_root = Path(data_root)
    transforms_dict = get_transforms(input_size, augment)
    
    # Create datasets
    train_dataset = datasets.ImageFolder(
        data_root / 'train',
        transform=transforms_dict['train']
    )
    
    val_dataset = datasets.ImageFolder(
        data_root / 'val',
        transform=transforms_dict['val']
    )
    
    test_dataset = datasets.ImageFolder(
        data_root / 'test',
        transform=transforms_dict['val']
    )
    
    # Create dataloaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True
    )
    
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True
    )
    
    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True
    )
    
    dataloaders = {
        'train': train_loader,
        'val': val_loader,
        'test': test_loader
    }
    
    # Print dataset info
    print(f"Dataset loaded from: {data_root}")
    print(f"  Train: {len(train_dataset)} images")
    print(f"  Val:   {len(val_dataset)} images")
    print(f"  Test:  {len(test_dataset)} images")
    print(f"  Classes: {len(train_dataset.classes)}")
    
    return dataloaders, train_dataset.classes


class SyntheticDataset(Dataset):
    """
    Synthetic dataset for testing when real data is not available.
    Generates random images with labels.
    """
    
    def __init__(self, num_samples=1000, input_size=128, num_classes=10):
        self.num_samples = num_samples
        self.input_size = input_size
        self.num_classes = num_classes
        
    def __len__(self):
        return self.num_samples
    
    def __getitem__(self, idx):
        # Generate random image
        image = torch.randn(3, self.input_size, self.input_size)
        # Generate random label
        label = torch.randint(0, self.num_classes, (1,)).item()
        return image, label


def get_synthetic_dataloaders(batch_size=64, input_size=128, num_classes=10):
    """
    Create synthetic dataloaders for testing.
    
    Args:
        batch_size: Batch size for dataloaders
        input_size: Image size
        num_classes: Number of classes
    
    Returns:
        Dictionary with 'train', 'val', and 'test' dataloaders
    """
    train_dataset = SyntheticDataset(num_samples=1400, input_size=input_size, 
                                    num_classes=num_classes)
    val_dataset = SyntheticDataset(num_samples=300, input_size=input_size, 
                                  num_classes=num_classes)
    test_dataset = SyntheticDataset(num_samples=300, input_size=input_size, 
                                   num_classes=num_classes)
    
    dataloaders = {
        'train': DataLoader(train_dataset, batch_size=batch_size, shuffle=True),
        'val': DataLoader(val_dataset, batch_size=batch_size, shuffle=False),
        'test': DataLoader(test_dataset, batch_size=batch_size, shuffle=False),
    }
    
    print(f"Synthetic dataset created:")
    print(f"  Train: {len(train_dataset)} samples")
    print(f"  Val:   {len(val_dataset)} samples")
    print(f"  Test:  {len(test_dataset)} samples")
    
    return dataloaders, CHARACTER_CLASSES


if __name__ == "__main__":
    # Test synthetic dataloaders
    print("Testing synthetic dataloaders...")
    dataloaders, classes = get_synthetic_dataloaders(batch_size=32)
    
    for phase in ['train', 'val', 'test']:
        images, labels = next(iter(dataloaders[phase]))
        print(f"{phase.capitalize()}: batch shape = {images.shape}, labels shape = {labels.shape}")
    
    print("✓ Dataset loader test passed!")
