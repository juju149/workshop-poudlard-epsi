# 🚀 LE NIMBUS 3000 - Optimizer Benchmark

Benchmark rigoureux des principaux optimizers sur un modèle CNN de reconnaissance de personnages Harry Potter.

## 🎯 Objectif

Comparer systématiquement les performances de 8 optimizers différents:
- **SGD** (avec/sans momentum, Nesterov)
- **Adam**
- **AdamW** 
- **RMSProp**
- **Adagrad**
- **Adadelta**
- **Adan**

## 📦 Livrables

- 📘 **Rapport académique** (PDF) dans `reports/paper.pdf`
- 🧪 **Scripts de reproduction** dans `scripts/`
- 📊 **Résultats et figures** dans `reports/figures/`

## 🏗️ Architecture

```
21-nimbus-3000/
├── data/
│   ├── raw/              # Dataset brut
│   └── processed/        # Données prétraitées
├── src/
│   ├── models/
│   │   └── net.py        # Architecture CNN
│   ├── datasets/
│   │   └── loader.py     # DataLoaders
│   ├── train.py          # Script d'entraînement
│   ├── eval.py           # Évaluation
│   ├── utils.py          # Utilitaires
│   └── optim_space.py    # Grilles d'hyperparamètres
├── runs/
│   └── logs/             # Logs d'entraînement
├── reports/
│   ├── figures/          # Graphiques
│   ├── tables/           # Tableaux de résultats
│   └── paper.md          # Rapport en Markdown
├── scripts/
│   ├── run_grid.sh       # Lance tous les benchmarks
│   ├── summarize.py      # Agrège les résultats
│   └── plot_curves.py    # Génère les figures
├── tests/
│   └── smoke_test.sh     # Test de fumée
├── requirements.txt
└── README.md
```

## 📋 Prérequis

- Python 3.10+
- PyTorch 2.1+
- 8GB+ RAM
- GPU recommandé (CUDA 11.8+)

## 🚀 Installation

```bash
cd projects/21-nimbus-3000

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac

# Installer les dépendances
pip install -r requirements.txt
```

## 📊 Dataset

Le benchmark utilise le dataset du défi "Is it you Harry" (10 personnages, ~2000 images).

Structure:
```
data/
├── raw/
│   ├── train/
│   ├── val/
│   └── test/
```

## 🎓 Utilisation

### 1. Lancer un entraînement unique

```bash
python src/train.py \
  --optimizer adamw \
  --lr 0.001 \
  --epochs 50 \
  --seed 42 \
  --batch-size 64
```

### 2. Lancer tous les benchmarks

```bash
bash scripts/run_grid.sh
```

Cela exécute:
- Tous les optimizers avec leurs grilles d'hyperparamètres
- 5 seeds différents par configuration
- Logging automatique dans `runs/logs/`

### 3. Agréger les résultats

```bash
python scripts/summarize.py \
  --runs runs/logs \
  --out reports/tables/summary.csv
```

### 4. Générer les figures

```bash
python scripts/plot_curves.py \
  --in reports/tables/summary.csv \
  --out reports/figures
```

## 📈 Métriques mesurées

- **Accuracy** (train/val/test)
- **F1-Score** (macro)
- **Loss** (CrossEntropy)
- **Temps par epoch**
- **Temps total d'entraînement**
- **Utilisation mémoire GPU**

## ⚙️ Configuration expérimentale

### Protocole commun à tous les optimizers

- **Epochs**: 50 (early stopping patience=10)
- **Batch size**: 64
- **Image size**: 128x128
- **Data augmentation**: rotation, flip, crop
- **Split**: 70/15/15 (train/val/test)
- **Seeds**: [42, 123, 456, 789, 1024]
- **Scheduler**: CosineAnnealingLR
- **Weight decay**: variable selon optimizer
- **Gradient clipping**: 1.0

### Grilles d'hyperparamètres

Voir `src/optim_space.py` pour les détails.

Exemples:
- **SGD**: lr ∈ {0.1, 0.01}, momentum ∈ {0, 0.9}
- **Adam**: lr ∈ {1e-3, 3e-4}, betas ∈ {(0.9,0.999), (0.9,0.95)}
- **AdamW**: lr ∈ {1e-3, 3e-4}, weight_decay ∈ {0.01, 0.05}

## 🧪 Tests

```bash
# Test de fumée (1 epoch, petit subset)
bash tests/smoke_test.sh
```

## 📚 Rapport académique

Structure du rapport (`reports/paper.md`):

1. Résumé
2. Introduction
3. Travaux connexes
4. Méthodologie
5. Résultats
6. Analyse
7. Limites
8. Conclusion
9. Annexes

## 🔧 Technologies utilisées

- **PyTorch** - Framework deep learning
- **torchvision** - Vision utilities
- **adan-pytorch** - Adan optimizer
- **matplotlib/seaborn** - Visualisations
- **pandas** - Manipulation de données
- **wandb** - Tracking expérimental (optionnel)

## 📊 Résultats attendus

Les résultats complets sont dans `reports/`:
- Tableaux comparatifs (moyenne ± écart-type)
- Courbes de convergence
- Tests statistiques (t-test, ANOVA)
- Analyse coût/performance

## 💡 Reproductibilité

- Seeds fixés: [42, 123, 456, 789, 1024]
- Versions documentées (PyTorch, CUDA, cuDNN)
- Configs sauvegardées dans `runs/logs/config_*.yaml`
- Logs détaillés par epoch

## 👥 Copilots

- 🧠 **AI Copilot** (lead) - Architecture et code
- 📊 **Data Copilot** - Analyse et rapport

## 📝 Licence

Projet éducatif - Workshop Poudlard EPSI

---

> 🧹 *"The Nimbus 3000 may be fast, but which optimizer is faster?"*
