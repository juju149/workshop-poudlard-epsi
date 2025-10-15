# 🚀 Quick Start - IS IT YOU HARRY?

Guide rapide pour démarrer avec le projet de reconnaissance de personnages Harry Potter.

## ⚡ Lancement rapide (3 étapes)

### Option 1: Avec Docker (recommandé)

```bash
# 1. Lancer le container
docker compose -f docker-compose.snippet.yml up -d

# 2. Accéder à Jupyter
# Ouvrir http://localhost:8888 dans votre navigateur

# 3. Exécuter le notebook
# Ouvrir src/character_recognition.ipynb
# Exécuter toutes les cellules (Cell > Run All)
```

### Option 2: Installation locale

```bash
# 1. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate sur Windows

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer Jupyter
jupyter notebook src/character_recognition.ipynb
```

## 📊 Ce que fait le notebook

1. **Crée un dataset de démonstration** - Images synthétiques pour tester
2. **Entraîne un modèle CNN** - Architecture simple mais efficace
3. **Évalue les performances** - Précision, matrice de confusion
4. **Sauvegarde le modèle** - Pour réutilisation future

## 🎯 Résultats attendus

- ✅ Dataset créé: 2000 images (10 personnages × 200 images)
- ✅ Modèle entraîné: ~2.5M paramètres
- ✅ Précision: ~99% (dataset démo) / 85-95% (dataset réel)
- ✅ Durée: 2-5 minutes (CPU)

## 📁 Fichiers générés

```
models/
├── best_model.h5                    # Meilleur modèle
├── character_recognition_final.h5   # Modèle final
├── training_curves.png              # Graphiques d'entraînement
├── confusion_matrix.png             # Matrice de confusion
├── classification_report.csv        # Rapport détaillé
└── model_metadata.json              # Métadonnées
```

## 🔧 Personnalisation

Pour utiliser un **vrai dataset** au lieu du dataset de démonstration:

1. Collectez ~200 images par personnage (voir `docs/dataset_guide.md`)
2. Organisez-les dans `data/train/`, `data/val/`, `data/test/`
3. Commentez la cellule de création du dataset démo
4. Exécutez le notebook normalement

## 🧪 Tests

```bash
# Vérifier que tout est en place
bash tests/test_smoke.sh
```

## 📚 Documentation complète

- **README.md** - Documentation principale
- **docs/rendu.md** - Rapport de validation complet
- **docs/prompts_used.md** - Prompts IA utilisés
- **docs/dataset_guide.md** - Guide de création du dataset

## 🆘 Aide

**Problème: Modules Python manquants**
```bash
pip install -r requirements.txt
```

**Problème: Docker ne démarre pas**
```bash
docker compose -f docker-compose.snippet.yml down
docker compose -f docker-compose.snippet.yml up -d --build
```

**Problème: Jupyter ne s'ouvre pas**
- Vérifier que le port 8888 n'est pas déjà utilisé
- Essayer: `jupyter notebook --port 8889`

---

> 🧙‍♂️ *Prêt à reconnaître Harry et ses amis? Lancez le notebook!*
