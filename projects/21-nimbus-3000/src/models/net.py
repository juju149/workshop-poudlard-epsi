"""
CNN Model for Harry Potter Character Recognition
Adapted from the 'Is it you Harry' project for optimizer benchmarking.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class CharacterCNN(nn.Module):
    """
    Convolutional Neural Network for character recognition.
    
    Architecture:
    - 4 convolutional blocks (32, 64, 128, 256 filters)
    - Batch normalization after each conv
    - Max pooling (2x2)
    - Dropout (0.25 after conv, 0.5 after dense)
    - 2 fully connected layers (512, 256)
    - Output: 10 classes (characters)
    
    Total parameters: ~2.5M
    """
    
    def __init__(self, num_classes=10, input_size=128, dropout_conv=0.25, dropout_fc=0.5):
        super(CharacterCNN, self).__init__()
        
        # Convolutional Block 1: 3 -> 32
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(32)
        self.pool1 = nn.MaxPool2d(2, 2)  # 128 -> 64
        self.dropout1 = nn.Dropout2d(dropout_conv)
        
        # Convolutional Block 2: 32 -> 64
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(64)
        self.pool2 = nn.MaxPool2d(2, 2)  # 64 -> 32
        self.dropout2 = nn.Dropout2d(dropout_conv)
        
        # Convolutional Block 3: 64 -> 128
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm2d(128)
        self.pool3 = nn.MaxPool2d(2, 2)  # 32 -> 16
        self.dropout3 = nn.Dropout2d(dropout_conv)
        
        # Convolutional Block 4: 128 -> 256
        self.conv4 = nn.Conv2d(128, 256, kernel_size=3, padding=1)
        self.bn4 = nn.BatchNorm2d(256)
        self.pool4 = nn.MaxPool2d(2, 2)  # 16 -> 8
        self.dropout4 = nn.Dropout2d(dropout_conv)
        
        # Calculate flattened size: 8x8x256 = 16384
        self.flatten_size = (input_size // 16) ** 2 * 256
        
        # Fully Connected Layers
        self.fc1 = nn.Linear(self.flatten_size, 512)
        self.bn5 = nn.BatchNorm1d(512)
        self.dropout5 = nn.Dropout(dropout_fc)
        
        self.fc2 = nn.Linear(512, 256)
        self.bn6 = nn.BatchNorm1d(256)
        self.dropout6 = nn.Dropout(dropout_fc)
        
        self.fc3 = nn.Linear(256, num_classes)
        
    def forward(self, x):
        # Block 1
        x = self.conv1(x)
        x = self.bn1(x)
        x = F.relu(x)
        x = self.pool1(x)
        x = self.dropout1(x)
        
        # Block 2
        x = self.conv2(x)
        x = self.bn2(x)
        x = F.relu(x)
        x = self.pool2(x)
        x = self.dropout2(x)
        
        # Block 3
        x = self.conv3(x)
        x = self.bn3(x)
        x = F.relu(x)
        x = self.pool3(x)
        x = self.dropout3(x)
        
        # Block 4
        x = self.conv4(x)
        x = self.bn4(x)
        x = F.relu(x)
        x = self.pool4(x)
        x = self.dropout4(x)
        
        # Flatten
        x = x.view(x.size(0), -1)
        
        # FC layers
        x = self.fc1(x)
        x = self.bn5(x)
        x = F.relu(x)
        x = self.dropout5(x)
        
        x = self.fc2(x)
        x = self.bn6(x)
        x = F.relu(x)
        x = self.dropout6(x)
        
        x = self.fc3(x)
        
        return x
    
    def get_num_params(self):
        """Returns the total number of trainable parameters."""
        return sum(p.numel() for p in self.parameters() if p.requires_grad)


def get_model(num_classes=10, input_size=128, dropout_conv=0.25, dropout_fc=0.5):
    """
    Factory function to create a CharacterCNN model.
    
    Args:
        num_classes: Number of output classes
        input_size: Input image size (assumed square)
        dropout_conv: Dropout rate after convolutional layers
        dropout_fc: Dropout rate after fully connected layers
    
    Returns:
        CharacterCNN model instance
    """
    model = CharacterCNN(
        num_classes=num_classes,
        input_size=input_size,
        dropout_conv=dropout_conv,
        dropout_fc=dropout_fc
    )
    return model


if __name__ == "__main__":
    # Test the model
    model = get_model()
    print(f"Model created with {model.get_num_params():,} parameters")
    
    # Test forward pass
    dummy_input = torch.randn(4, 3, 128, 128)
    output = model(dummy_input)
    print(f"Input shape: {dummy_input.shape}")
    print(f"Output shape: {output.shape}")
    assert output.shape == (4, 10), "Output shape mismatch!"
    print("✓ Model test passed!")
