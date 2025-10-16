"""
Optimizer hyperparameter grids for benchmarking.
"""

import torch.optim as optim
try:
    from adan import Adan
    ADAN_AVAILABLE = True
except ImportError:
    ADAN_AVAILABLE = False
    print("Warning: Adan optimizer not available. Install with: pip install adan-pytorch")


# Hyperparameter grids for each optimizer
OPTIMIZER_GRIDS = {
    'sgd': [
        {'lr': 0.1, 'momentum': 0.0, 'nesterov': False, 'weight_decay': 0.0},
        {'lr': 0.1, 'momentum': 0.9, 'nesterov': False, 'weight_decay': 0.0},
        {'lr': 0.1, 'momentum': 0.9, 'nesterov': True, 'weight_decay': 0.0},
        {'lr': 0.01, 'momentum': 0.9, 'nesterov': False, 'weight_decay': 0.0},
    ],
    
    'adam': [
        {'lr': 1e-3, 'betas': (0.9, 0.999), 'weight_decay': 0.0},
        {'lr': 3e-4, 'betas': (0.9, 0.999), 'weight_decay': 0.0},
        {'lr': 1e-3, 'betas': (0.9, 0.95), 'weight_decay': 0.0},
        {'lr': 3e-4, 'betas': (0.9, 0.95), 'weight_decay': 0.0},
    ],
    
    'adamw': [
        {'lr': 1e-3, 'betas': (0.9, 0.999), 'weight_decay': 0.01},
        {'lr': 3e-4, 'betas': (0.9, 0.999), 'weight_decay': 0.01},
        {'lr': 1e-3, 'betas': (0.9, 0.999), 'weight_decay': 0.05},
        {'lr': 3e-4, 'betas': (0.9, 0.999), 'weight_decay': 0.05},
    ],
    
    'rmsprop': [
        {'lr': 1e-3, 'alpha': 0.9, 'centered': False, 'weight_decay': 0.0},
        {'lr': 3e-4, 'alpha': 0.9, 'centered': False, 'weight_decay': 0.0},
        {'lr': 1e-3, 'alpha': 0.95, 'centered': True, 'weight_decay': 0.0},
        {'lr': 3e-4, 'alpha': 0.95, 'centered': True, 'weight_decay': 0.0},
    ],
    
    'adagrad': [
        {'lr': 1e-2, 'initial_accumulator_value': 0.0, 'weight_decay': 0.0},
        {'lr': 1e-3, 'initial_accumulator_value': 0.0, 'weight_decay': 0.0},
        {'lr': 1e-2, 'initial_accumulator_value': 0.1, 'weight_decay': 0.0},
        {'lr': 1e-3, 'initial_accumulator_value': 0.1, 'weight_decay': 0.0},
    ],
    
    'adadelta': [
        {'lr': 1.0, 'rho': 0.9, 'weight_decay': 0.0},
        {'lr': 0.5, 'rho': 0.9, 'weight_decay': 0.0},
        {'lr': 1.0, 'rho': 0.95, 'weight_decay': 0.0},
        {'lr': 0.5, 'rho': 0.95, 'weight_decay': 0.0},
    ],
    
    'adan': [
        {'lr': 1e-3, 'betas': (0.98, 0.92, 0.99), 'weight_decay': 0.01},
        {'lr': 3e-4, 'betas': (0.98, 0.92, 0.99), 'weight_decay': 0.01},
        {'lr': 1e-3, 'betas': (0.98, 0.92, 0.99), 'weight_decay': 0.02},
        {'lr': 3e-4, 'betas': (0.98, 0.92, 0.99), 'weight_decay': 0.02},
    ],
}


def get_optimizer(optimizer_name, model_parameters, **kwargs):
    """
    Create an optimizer instance with given hyperparameters.
    
    Args:
        optimizer_name: Name of the optimizer (sgd, adam, adamw, etc.)
        model_parameters: Model parameters to optimize
        **kwargs: Optimizer-specific hyperparameters
    
    Returns:
        Optimizer instance
    """
    optimizer_name = optimizer_name.lower()
    
    if optimizer_name == 'sgd':
        return optim.SGD(model_parameters, **kwargs)
    
    elif optimizer_name == 'adam':
        return optim.Adam(model_parameters, **kwargs)
    
    elif optimizer_name == 'adamw':
        return optim.AdamW(model_parameters, **kwargs)
    
    elif optimizer_name == 'rmsprop':
        return optim.RMSprop(model_parameters, **kwargs)
    
    elif optimizer_name == 'adagrad':
        return optim.Adagrad(model_parameters, **kwargs)
    
    elif optimizer_name == 'adadelta':
        return optim.Adadelta(model_parameters, **kwargs)
    
    elif optimizer_name == 'adan':
        if not ADAN_AVAILABLE:
            raise ImportError("Adan optimizer not available. Install with: pip install adan-pytorch")
        return Adan(model_parameters, **kwargs)
    
    else:
        raise ValueError(f"Unknown optimizer: {optimizer_name}")


def get_optimizer_grid(optimizer_name):
    """
    Get the hyperparameter grid for a specific optimizer.
    
    Args:
        optimizer_name: Name of the optimizer
    
    Returns:
        List of hyperparameter configurations
    """
    optimizer_name = optimizer_name.lower()
    
    if optimizer_name not in OPTIMIZER_GRIDS:
        raise ValueError(f"No grid defined for optimizer: {optimizer_name}")
    
    return OPTIMIZER_GRIDS[optimizer_name]


def get_all_optimizers():
    """
    Get list of all available optimizers.
    
    Returns:
        List of optimizer names
    """
    optimizers = list(OPTIMIZER_GRIDS.keys())
    if not ADAN_AVAILABLE:
        optimizers.remove('adan')
    return optimizers


if __name__ == "__main__":
    print("Available optimizers:")
    for opt_name in get_all_optimizers():
        grid = get_optimizer_grid(opt_name)
        print(f"  - {opt_name}: {len(grid)} configurations")
    
    print(f"\nTotal configurations: {sum(len(get_optimizer_grid(opt)) for opt in get_all_optimizers())}")
