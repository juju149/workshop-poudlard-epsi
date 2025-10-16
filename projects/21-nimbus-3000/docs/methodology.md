# Notes de méthodologie - Nimbus 3000

## 📋 Vue d'ensemble

Ce document contient des notes sur la méthodologie, les choix de conception, et les meilleures pratiques pour le benchmark d'optimizers.

## 🎯 Objectifs du benchmark

1. **Comparer équitablement** 7 optimizers sur la même tâche
2. **Mesurer statistiquement** la performance avec plusieurs seeds
3. **Analyser** les trade-offs vitesse/précision
4. **Documenter** de manière reproductible

## 🔬 Protocole expérimental

### Pourquoi ces choix ?

**Epochs: 50**
- Suffisant pour la convergence sur ce dataset
- Early stopping évite le surapprentissage
- Compromis entre temps de calcul et résultats

**Batch size: 64**
- Standard pour CNNs de cette taille
- Compromis mémoire GPU / stabilité training
- Peut être réduit à 32 si problème de mémoire

**Seeds: 5 différents**
- Minimum pour statistiques robustes
- Permet de calculer moyenne ± écart-type
- Révèle la stabilité des optimizers

**Learning rate scheduler: Cosine Annealing**
- Améliore la convergence finale
- Réduit le LR progressivement
- Standard dans la littérature

**Gradient clipping: 1.0**
- Évite les explosions de gradients
- Particulièrement utile pour SGD
- Valeur standard

### Métriques choisies

**Accuracy**
- Métrique principale, facile à interpréter
- Suffit pour dataset équilibré

**F1-score (macro)**
- Sensible aux déséquilibres de classes
- Plus robuste que accuracy seule
- Standard pour classification multiclasse

**Loss (CrossEntropy)**
- Mesure directe de l'optimisation
- Indicateur de calibration du modèle

**Temps d'entraînement**
- Critique pour applications réelles
- Révèle l'efficacité computationnelle

## 🧪 Grilles d'hyperparamètres

### Philosophie

- **4 configs par optimizer**: compromis entre exploration et temps
- **Focus sur learning rate**: paramètre le plus impactant
- **Variations sur paramètres spécifiques**: momentum pour SGD, betas pour Adam, etc.

### SGD

```
Config 0: lr=0.1, momentum=0.0           # Baseline sans momentum
Config 1: lr=0.1, momentum=0.9           # Standard avec momentum
Config 2: lr=0.1, momentum=0.9, nesterov # Nesterov acceleration
Config 3: lr=0.01, momentum=0.9          # LR plus conservateur
```

**Rationale**: 
- SGD nécessite généralement LR plus élevé
- Momentum aide beaucoup à la convergence
- Nesterov peut améliorer légèrement

### Adam / AdamW

```
Config 0: lr=1e-3, standard betas        # Configuration classique
Config 1: lr=3e-4, standard betas        # LR recommandé par beaucoup
Config 2: lr=1e-3, beta2=0.95            # Beta2 plus bas (moins de smoothing)
Config 3: lr=3e-4, beta2=0.95            # Combinaison conservatrice
```

**Rationale**:
- 1e-3 est le défaut Adam mais peut être trop élevé
- 3e-4 souvent meilleur en pratique
- Beta2 = 0.95 peut aider pour datasets bruités

### RMSProp

```
Config 0: lr=1e-3, alpha=0.9             # Standard
Config 1: lr=3e-4, alpha=0.9             # LR plus bas
Config 2: lr=1e-3, alpha=0.95, centered  # Plus de smoothing + centered
Config 3: lr=3e-4, alpha=0.95, centered  # Version conservatrice
```

**Rationale**:
- Centered RMSProp peut améliorer la stabilité
- Alpha contrôle le smoothing (plus haut = plus smooth)

## 📊 Interprétation des résultats

### Ce qu'on cherche

**Meilleur optimizer pour accuracy**
- Qui atteint le plus haut score test ?
- Trade-off avec le temps ?

**Optimizer le plus stable**
- Qui a le plus faible écart-type entre seeds ?
- Important pour reproductibilité

**Optimizer le plus rapide**
- Temps total pour atteindre convergence
- Nombre d'epochs nécessaires

**Meilleur trade-off**
- Balance entre tous les critères
- Recommandation générale

### Analyse statistique

**Moyenne ± Écart-type**
- Écart-type < 1% : très stable
- Écart-type 1-3% : normal
- Écart-type > 5% : instable

**Comparaisons**
- Différence > 2% : probablement significative
- Différence < 0.5% : probablement négligeable
- Tests statistiques (t-test) pour confirmer

## 🎨 Visualisations

### Courbes d'entraînement

**Par optimizer**
- Montrer toutes les runs (transparence)
- Identifier convergence et stabilité
- Détecter overfitting

**Comparaison globale**
- Meilleure config par optimizer
- Facile de voir qui converge vite
- Qui atteint le meilleur score

### Graphiques de comparaison

**Barres d'accuracy**
- Avec barres d'erreur (±std)
- Trié par performance
- Couleurs distinctes

**Scatter accuracy vs temps**
- Trade-off visualisé
- Pareto frontier
- Guide le choix selon contraintes

**Heatmap**
- Toutes les configs visualisées
- Patterns dans hyperparams
- Sensibilité révélée

## 🐛 Problèmes courants

### CUDA Out of Memory

**Solutions**:
1. Réduire batch size: `--batch-size 32`
2. Réduire input size: `--input-size 96`
3. Utiliser gradient accumulation
4. Tester avec CPU d'abord: `CUDA_VISIBLE_DEVICES="" python ...`

### Convergence lente

**Causes possibles**:
- Learning rate trop bas ou trop haut
- Data augmentation trop agressive
- Architecture mal initialisée

**Debug**:
- Visualiser les courbes de loss
- Vérifier les gradients (pas NaN)
- Tester sans data augmentation

### Variance élevée entre seeds

**Normal si**:
- Dataset petit
- Model complexe
- Task difficile

**Anormal si**:
- Variance > 10%
- Patterns erratiques
- Peut indiquer bug

## 📝 Bonnes pratiques

### Avant de lancer le benchmark complet

1. **Smoke test**: Vérifier que tout marche
2. **Test 1 epoch**: Vérifier temps estimé
3. **Test 1 optimizer complet**: Vérifier workflow
4. **Puis lancer full grid**

### Pendant l'exécution

1. **Monitorer**: Vérifier logs régulièrement
2. **Checkpoints**: S'assurer qu'ils sont sauvés
3. **Disk space**: Vérifier l'espace disque
4. **Tuer jobs bloqués**: Si timeout

### Après l'exécution

1. **Vérifier tous les runs**: Pas d'erreurs
2. **Agréger immédiatement**: Avant de perdre les logs
3. **Backup**: Copier runs/ ailleurs
4. **Documenter**: Notes sur anomalies

## 🎓 Pour le rapport académique

### Structure à respecter

1. **Résumé** (150-200 mots)
   - Contexte, méthode, résultats clés
   
2. **Introduction** (1-2 pages)
   - Motivation
   - Contributions
   - Plan du papier

3. **Related Work** (0.5-1 page)
   - Autres benchmarks d'optimizers
   - Citer papiers originaux

4. **Méthodologie** (2-3 pages)
   - Dataset, modèle, protocole
   - Justifier les choix
   - Reproductibilité

5. **Résultats** (2-3 pages)
   - Tables, figures
   - Observations factuelles
   - Pas d'interprétation encore

6. **Discussion** (1-2 pages)
   - Interprétation
   - Comparaison littérature
   - Recommandations

7. **Conclusion** (0.5-1 page)
   - Résumé contributions
   - Limitations
   - Future work

### Figures de qualité

- **DPI minimum**: 300 pour publication
- **Labels**: Lisibles, taille police >= 10
- **Légendes**: Complètes et informatives
- **Couleurs**: Colorblind-friendly
- **Captions**: Décrivent ce qu'on voit

### Tables

- **Alignement**: Nombres alignés à droite
- **Précision**: 4 décimales pour métriques
- **Bold**: Meilleurs résultats en gras
- **Légende**: Explique abbréviations

## 🚀 Extensions possibles

### Court terme

1. **Plus de seeds**: 10 au lieu de 5
2. **Plus d'epochs**: 100 au lieu de 50
3. **Cross-validation**: K-fold
4. **Ensemble**: Moyenne de plusieurs runs

### Moyen terme

1. **Autres architectures**: ResNet, ViT
2. **Autres datasets**: CIFAR, ImageNet
3. **Transfer learning**: Fine-tuning
4. **Mixed precision**: AMP

### Long terme

1. **AutoML**: Optimisation automatique hyperparams
2. **Neural Architecture Search**: Chercher architecture
3. **Multi-task**: Plusieurs tâches ensemble
4. **Distributed**: Training multi-GPU

## 📚 Références utiles

### Papers

- Adam: Kingma & Ba (2014)
- AdamW: Loshchilov & Hutter (2017)
- Adan: Xie et al. (2022)
- SGD momentum: Sutskever et al. (2013)

### Ressources

- PyTorch optimizers doc
- Papers With Code (benchmarks)
- Sebastian Ruder's optimization overview
- Distill.pub (visualizations)

## ✨ Conseils finaux

1. **Patience**: Benchmark prend du temps
2. **Rigueur**: Suivre protocole strictement
3. **Documentation**: Noter tout
4. **Backup**: Sauvegarder résultats
5. **Visualisation**: Explorer les données
6. **Interprétation**: Réfléchir aux résultats
7. **Communication**: Rapport clair

Bon benchmark ! 🧙‍♂️✨
