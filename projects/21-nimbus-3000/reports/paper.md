# Comparative Benchmark of Optimization Algorithms for Deep Learning: A Case Study on Character Recognition

## Abstract

This paper presents a rigorous benchmark of seven popular optimization algorithms (SGD, Adam, AdamW, RMSProp, Adagrad, Adadelta, and Adan) applied to a Convolutional Neural Network (CNN) for character recognition. We evaluate each optimizer across multiple hyperparameter configurations and random seeds to ensure statistical robustness. Our experimental protocol maintains consistency across all optimizers in terms of model architecture, data preprocessing, training schedule, and regularization. We measure convergence speed, final performance (accuracy and F1-score), training stability, and computational cost. Results indicate that [TO BE FILLED] achieves the best trade-off between accuracy and training time, while [TO BE FILLED] demonstrates superior stability across random initializations. This work provides practical insights for practitioners selecting optimizers for computer vision tasks and establishes a reproducible methodology for future optimizer benchmarking studies.

**Keywords**: Deep Learning, Optimization Algorithms, Convolutional Neural Networks, Benchmark Study, Reproducibility

---

## 1. Introduction

### 1.1 Context and Motivation

The choice of optimization algorithm is a critical decision in training deep neural networks. While Stochastic Gradient Descent (SGD) has been the workhorse of deep learning for decades, adaptive learning rate methods like Adam, RMSProp, and their variants have gained popularity due to their ease of use and fast convergence. However, the relative performance of these optimizers can vary significantly depending on the task, model architecture, and hyperparameter settings.

Despite numerous empirical studies, there is no consensus on which optimizer performs best across different scenarios. Moreover, many comparisons lack rigorous experimental protocols, making it difficult to draw reliable conclusions. This study addresses this gap by conducting a systematic benchmark of seven optimization algorithms on a well-defined computer vision task.

### 1.2 Contributions

Our main contributions are:

1. **Rigorous experimental protocol**: We ensure fair comparison by controlling for all confounding factors (architecture, data splits, initialization, regularization, etc.).

2. **Statistical robustness**: We run each configuration with 5 different random seeds and report mean and standard deviation.

3. **Comprehensive evaluation**: We measure not only final accuracy but also convergence speed, stability, and computational cost.

4. **Reproducibility**: We provide complete source code and detailed documentation to enable replication of our results.

5. **Practical insights**: We offer recommendations for practitioners based on different use cases (speed vs. accuracy, stability requirements, etc.).

### 1.3 Paper Organization

The remainder of this paper is organized as follows: Section 2 reviews related work on optimizer comparisons. Section 3 describes our methodology, including the model architecture, dataset, and experimental protocol. Section 4 presents our results with detailed analysis. Section 5 discusses limitations and future work. Section 6 concludes with practical recommendations.

---

## 2. Related Work

### 2.1 Optimization Algorithms Overview

**Stochastic Gradient Descent (SGD)**: The foundational algorithm for neural network training. With momentum and Nesterov acceleration, SGD can achieve state-of-the-art results but requires careful learning rate tuning.

**Adagrad**: Adapts learning rates per parameter based on historical gradients. Effective for sparse gradients but can suffer from aggressive learning rate decay.

**Adadelta**: Addresses Adagrad's aggressive decay by using a moving window of gradients. Eliminates the need for manual learning rate tuning.

**RMSProp**: Proposed by Hinton, it uses exponentially decaying average of squared gradients. Popular for recurrent neural networks.

**Adam**: Combines ideas from momentum and RMSProp. Computes adaptive learning rates using first and second moments of gradients. Widely adopted due to good default hyperparameters.

**AdamW**: Decouples weight decay from gradient updates, fixing a known issue with L2 regularization in Adam. Often outperforms Adam on tasks requiring strong regularization.

**Adan**: A recent optimizer that incorporates Nesterov momentum and adaptive learning rates. Claims to achieve better convergence than Adam on various tasks.

### 2.2 Previous Benchmark Studies

[TO BE FILLED: Discuss relevant prior work on optimizer comparisons, their methodologies, and findings]

---

## 3. Methodology

### 3.1 Task and Dataset

We use the Harry Potter character recognition dataset, which consists of images of 10 characters:
- Harry Potter
- Hermione Granger
- Ron Weasley
- Albus Dumbledore
- Severus Snape
- Voldemort
- Draco Malfoy
- Hagrid
- Minerva McGonagall
- Sirius Black

**Dataset statistics**:
- Training set: ~1,400 images (70%)
- Validation set: ~300 images (15%)
- Test set: ~300 images (15%)
- Image resolution: 128×128 pixels
- Color channels: RGB (3 channels)

### 3.2 Model Architecture

We employ a Convolutional Neural Network (CNN) with the following architecture:

**Convolutional Blocks** (4 blocks):
- Block 1: Conv(3→32) + BatchNorm + ReLU + MaxPool(2×2) + Dropout(0.25)
- Block 2: Conv(32→64) + BatchNorm + ReLU + MaxPool(2×2) + Dropout(0.25)
- Block 3: Conv(64→128) + BatchNorm + ReLU + MaxPool(2×2) + Dropout(0.25)
- Block 4: Conv(128→256) + BatchNorm + ReLU + MaxPool(2×2) + Dropout(0.25)

**Fully Connected Layers**:
- FC1: 16384→512 + BatchNorm + ReLU + Dropout(0.5)
- FC2: 512→256 + BatchNorm + ReLU + Dropout(0.5)
- Output: 256→10 (softmax)

**Total parameters**: ~2.5M trainable parameters

### 3.3 Data Preprocessing and Augmentation

**Training set augmentation**:
- Random horizontal flip (p=0.5)
- Random rotation (±15 degrees)
- Color jitter (brightness, contrast, saturation: ±20%)
- Normalization: mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]

**Validation/Test set**:
- Resize to 128×128
- Normalization only (no augmentation)

### 3.4 Experimental Protocol

To ensure fair comparison, we maintain the following settings constant across all experiments:

**Training configuration**:
- Epochs: 50 (with early stopping patience=10)
- Batch size: 64
- Loss function: Cross-Entropy
- Learning rate scheduler: Cosine Annealing (min_lr=1e-6)
- Gradient clipping: max_norm=1.0
- Random seeds: [42, 123, 456, 789, 1024] (5 runs per configuration)

**Model initialization**:
- Convolutional layers: Kaiming initialization
- Fully connected layers: Xavier initialization
- Fixed seed for reproducibility

**Hardware**:
- [TO BE FILLED: GPU model, CUDA version, PyTorch version]

### 3.5 Optimizer Hyperparameter Grids

For each optimizer, we evaluate 4 configurations selected to cover a reasonable range of hyperparameters:

**SGD**:
1. lr=0.1, momentum=0.0
2. lr=0.1, momentum=0.9
3. lr=0.1, momentum=0.9, nesterov=True
4. lr=0.01, momentum=0.9

**Adam**:
1. lr=1e-3, β=(0.9, 0.999)
2. lr=3e-4, β=(0.9, 0.999)
3. lr=1e-3, β=(0.9, 0.95)
4. lr=3e-4, β=(0.9, 0.95)

**AdamW**:
1. lr=1e-3, weight_decay=0.01
2. lr=3e-4, weight_decay=0.01
3. lr=1e-3, weight_decay=0.05
4. lr=3e-4, weight_decay=0.05

**RMSProp**:
1. lr=1e-3, α=0.9
2. lr=3e-4, α=0.9
3. lr=1e-3, α=0.95, centered=True
4. lr=3e-4, α=0.95, centered=True

**Adagrad**:
1. lr=1e-2, initial_accumulator=0.0
2. lr=1e-3, initial_accumulator=0.0
3. lr=1e-2, initial_accumulator=0.1
4. lr=1e-3, initial_accumulator=0.1

**Adadelta**:
1. lr=1.0, ρ=0.9
2. lr=0.5, ρ=0.9
3. lr=1.0, ρ=0.95
4. lr=0.5, ρ=0.95

**Adan**:
1. lr=1e-3, weight_decay=0.01
2. lr=3e-4, weight_decay=0.01
3. lr=1e-3, weight_decay=0.02
4. lr=3e-4, weight_decay=0.02

### 3.6 Evaluation Metrics

**Performance metrics**:
- **Accuracy**: Overall classification accuracy
- **F1-score (macro)**: Macro-averaged F1 across all classes
- **F1-score (weighted)**: Weighted F1 by class support
- **Loss**: Cross-entropy loss

**Convergence metrics**:
- **Best epoch**: Epoch at which validation loss is minimized
- **Convergence speed**: Number of epochs to reach 90% of final accuracy

**Computational metrics**:
- **Total training time**: Wall-clock time for complete training
- **Time per epoch**: Average time per epoch
- **GPU memory usage**: Peak memory consumption

**Stability metrics**:
- **Standard deviation**: Across 5 random seeds for each metric

---

## 4. Results

### 4.1 Overall Performance Comparison

[TO BE FILLED: Table showing mean ± std for each optimizer's best configuration]

| Optimizer | Test Accuracy | Test F1 (macro) | Test Loss | Training Time (s) | Best Epoch |
|-----------|--------------|-----------------|-----------|-------------------|------------|
| SGD       | X.XX ± X.XX  | X.XX ± X.XX    | X.XX ± X.XX | XXX ± XX       | XX ± X     |
| Adam      | X.XX ± X.XX  | X.XX ± X.XX    | X.XX ± X.XX | XXX ± XX       | XX ± X     |
| AdamW     | X.XX ± X.XX  | X.XX ± X.XX    | X.XX ± X.XX | XXX ± XX       | XX ± X     |
| RMSProp   | X.XX ± X.XX  | X.XX ± X.XX    | X.XX ± X.XX | XXX ± XX       | XX ± X     |
| Adagrad   | X.XX ± X.XX  | X.XX ± X.XX    | X.XX ± X.XX | XXX ± XX       | XX ± X     |
| Adadelta  | X.XX ± X.XX  | X.XX ± X.XX    | X.XX ± X.XX | XXX ± XX       | XX ± X     |
| Adan      | X.XX ± X.XX  | X.XX ± X.XX    | X.XX ± X.XX | XXX ± XX       | XX ± X     |

### 4.2 Convergence Analysis

[TO BE FILLED: Include training curves showing loss/accuracy vs epoch for each optimizer]

**Key observations**:
- [Optimizer X] converges fastest, reaching plateau after Y epochs
- [Optimizer Y] shows most stable training (lowest variance)
- [Optimizer Z] exhibits initial rapid improvement but slower final convergence

### 4.3 Hyperparameter Sensitivity

[TO BE FILLED: Analysis of how sensitive each optimizer is to its hyperparameters]

### 4.4 Statistical Significance

[TO BE FILLED: Statistical tests (t-test, ANOVA) comparing top performers]

---

## 5. Analysis and Discussion

### 5.1 Speed vs. Accuracy Trade-off

[TO BE FILLED: Analysis of which optimizers offer best trade-offs]

### 5.2 Stability Across Random Seeds

[TO BE FILLED: Discussion of variance in results]

### 5.3 Practical Recommendations

Based on our results, we offer the following recommendations:

**For maximum accuracy**: Use [Optimizer X] with [hyperparameters]

**For fastest convergence**: Use [Optimizer Y] with [hyperparameters]

**For best stability**: Use [Optimizer Z] with [hyperparameters]

**For limited computational budget**: Use [Optimizer W] with early stopping

### 5.4 Comparison with Literature

[TO BE FILLED: How do our findings align with or differ from previous studies?]

---

## 6. Limitations and Future Work

### 6.1 Limitations

1. **Single task evaluation**: Results are specific to image classification on this dataset
2. **Limited architecture**: Only tested on one CNN architecture
3. **Computational constraints**: Limited grid search due to computational budget
4. **Dataset size**: Relatively small dataset (~2000 images)

### 6.2 Future Work

1. **Extended evaluation**: Test on multiple datasets and architectures
2. **Larger grid search**: More extensive hyperparameter exploration
3. **Second-order methods**: Include optimizers like L-BFGS, K-FAC
4. **Modern variants**: Test newer variants (AdaBelief, Lamb, etc.)
5. **Transfer learning**: Evaluate on fine-tuning scenarios
6. **Different domains**: Extend to NLP and other domains

---

## 7. Conclusion

This study provides a comprehensive benchmark of seven optimization algorithms for deep learning, following a rigorous and reproducible methodology. Our results show that [TO BE FILLED with main findings]. The choice of optimizer involves trade-offs between convergence speed, final accuracy, and stability. We provide practical recommendations based on different use cases and make our code publicly available to facilitate future research.

---

## Acknowledgments

This work was conducted as part of the Workshop Poudlard EPSI project. We thank the AI Copilot and Data Copilot teams for their contributions.

---

## References

1. Kingma, D. P., & Ba, J. (2014). Adam: A method for stochastic optimization. arXiv preprint arXiv:1412.6980.

2. Loshchilov, I., & Hutter, F. (2017). Decoupled weight decay regularization. arXiv preprint arXiv:1711.05101.

3. Duchi, J., Hazan, E., & Singer, Y. (2011). Adaptive subgradient methods for online learning and stochastic optimization. JMLR.

4. Zeiler, M. D. (2012). ADADELTA: an adaptive learning rate method. arXiv preprint arXiv:1212.5701.

5. Tieleman, T., & Hinton, G. (2012). Lecture 6.5-rmsprop: Divide the gradient by a running average of its recent magnitude. COURSERA: Neural networks for machine learning.

6. Xie, X., Zhou, P., Li, H., Lin, Z., & Yan, S. (2022). Adan: Adaptive nesterov momentum algorithm for faster optimizing deep models. arXiv preprint arXiv:2208.06677.

---

## Appendix A: Detailed Configuration

### A.1 Software Versions

- Python: 3.10+
- PyTorch: 2.1.0
- CUDA: [TO BE FILLED]
- cuDNN: [TO BE FILLED]

### A.2 Complete Hyperparameter Tables

[TO BE FILLED: Detailed tables with all configurations tested]

### A.3 Reproduction Instructions

```bash
# Clone repository
git clone [repository-url]
cd projects/21-nimbus-3000

# Install dependencies
pip install -r requirements.txt

# Run complete benchmark
bash scripts/run_grid.sh

# Aggregate results
python scripts/summarize.py --runs runs/logs

# Generate plots
python scripts/plot_curves.py --logs runs/logs
```

---

## Appendix B: Additional Results

[TO BE FILLED: Per-class accuracy, confusion matrices, additional plots]
