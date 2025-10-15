# 🧙‍♂️ IS IT YOU HARRY? - CNN Character Recognition

Réseau de neurones convolutif (CNN) pour reconnaître **10 personnages** d'Harry Potter à partir d'images.

## 🎯 Objectif

Créer un modèle de deep learning capable d'identifier automatiquement 10 personnages principaux de l'univers Harry Potter en utilisant des techniques de vision par ordinateur et de réseaux de neurones convolutifs.

**Objectif atteint**: ✅ Reconnaissance de 10 personnages différents

## ✨ Personnages reconnus

1. **Harry Potter** - Le survivant
2. **Hermione Granger** - La plus brillante sorcière de sa génération
3. **Ron Weasley** - Le meilleur ami
4. **Albus Dumbledore** - Le directeur de Poudlard
5. **Severus Snape** - Le maître des potions
6. **Voldemort** - Le seigneur des ténèbres
7. **Draco Malfoy** - Le rival de Serpentard
8. **Hagrid** - Le garde-chasse
9. **Minerva McGonagall** - Directrice adjointe
10. **Sirius Black** - Le parrain

## 🏗️ Architecture

```
20-is-it-you-harry/
├── README.md                       # Ce fichier
├── requirements.txt                # Dépendances Python
├── Dockerfile                      # Configuration Docker
├── docker-compose.snippet.yml      # Configuration Docker Compose
├── src/
│   └── character_recognition.ipynb # Notebook principal
├── data/
│   ├── train/                      # Données d'entraînement (70%)
│   ├── val/                        # Données de validation (15%)
│   └── test/                       # Données de test (15%)
├── models/
│   ├── best_model.h5              # Meilleur modèle durant l'entraînement
│   ├── character_recognition_final.h5  # Modèle final
│   ├── training_curves.png        # Courbes d'apprentissage
│   ├── confusion_matrix.png       # Matrice de confusion
│   ├── classification_report.csv  # Rapport détaillé
│   └── model_metadata.json        # Métadonnées du modèle
├── docs/
│   ├── rendu.md                   # Document de rendu final
│   ├── prompts_used.md            # Prompts IA utilisés
│   └── dataset_guide.md           # Guide pour créer le dataset
└── tests/
    └── test_smoke.sh              # Tests de validation
```

## 📋 Prérequis

- Python 3.10+
- TensorFlow 2.15+
- 4GB+ RAM (8GB+ recommandé)
- GPU optionnel (pour entraînement plus rapide)
- Docker et Docker Compose (pour déploiement)

## 🚀 Installation

### Installation locale

```bash
# Clone le repository
cd projects/20-is-it-you-harry

# Crée un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installe les dépendances
pip install -r requirements.txt

# Lance Jupyter
jupyter notebook src/character_recognition.ipynb
```

### Installation avec Docker

```bash
# Depuis le dossier du projet
docker compose -f docker-compose.snippet.yml up -d
```

Accédez à Jupyter Lab sur http://localhost:8888

## 📊 Dataset

### Structure recommandée

Le dataset doit être organisé comme suit:

```
data/
├── train/
│   ├── harry_potter/
│   │   ├── harry_001.jpg
│   │   ├── harry_002.jpg
│   │   └── ... (~140 images)
│   ├── hermione_granger/
│   └── ... (10 personnages)
├── val/
│   └── ... (~30 images par personnage)
└── test/
    └── ... (~30 images par personnage)
```

### Création du dataset

**Option 1**: Le notebook crée automatiquement un dataset de démonstration avec des images synthétiques pour tester le pipeline.

**Option 2**: Pour une vraie reconnaissance, collectez ~200 images par personnage:
- Utilisez des captures d'écran des films
- Téléchargez depuis des bases d'images (Google Images, Bing, etc.)
- Générez des images avec Stable Diffusion / DALL-E
- Utilisez des outils de web scraping (Pinterest, Flickr)

Voir `docs/dataset_guide.md` pour plus de détails.

## 🎓 Utilisation

### 1. Entraînement

Ouvrez le notebook `src/character_recognition.ipynb` et exécutez les cellules dans l'ordre:

1. **Configuration** - Paramètres du modèle
2. **Dataset** - Création/chargement des données
3. **Exploration** - Visualisation du dataset
4. **Préparation** - Data augmentation
5. **Modèle** - Architecture CNN
6. **Entraînement** - Training loop
7. **Évaluation** - Métriques et visualisations
8. **Sauvegarde** - Export du modèle

### 2. Évaluation

Le notebook génère automatiquement:
- Courbes d'entraînement (précision/perte)
- Matrice de confusion
- Rapport de classification détaillé
- Analyse des erreurs

### 3. Inférence

```python
import numpy as np
from tensorflow import keras
from PIL import Image

# Charger le modèle
model = keras.models.load_model('models/character_recognition_final.h5')

# Charger une image
img = Image.open('path/to/image.jpg')
img = img.resize((128, 128))
img_array = np.array(img) / 255.0
img_array = np.expand_dims(img_array, axis=0)

# Prédiction
predictions = model.predict(img_array)
character_idx = np.argmax(predictions[0])

characters = ['harry_potter', 'hermione_granger', 'ron_weasley', 
              'albus_dumbledore', 'severus_snape', 'voldemort',
              'draco_malfoy', 'hagrid', 'minerva_mcgonagall', 'sirius_black']

print(f"Personnage prédit: {characters[character_idx]}")
print(f"Confiance: {predictions[0][character_idx] * 100:.2f}%")
```

## 🧪 Tests

```bash
# Exécuter les tests de validation
bash tests/test_smoke.sh
```

## 📈 Architecture du modèle

Le modèle CNN utilise:

- **4 blocs convolutifs** avec:
  - Convolution 2D (32, 64, 128, 256 filtres)
  - Batch Normalization
  - Max Pooling (2x2)
  - Dropout (0.25)

- **Couches fully connected**:
  - Dense 512 + BatchNorm + Dropout (0.5)
  - Dense 256 + BatchNorm + Dropout (0.5)
  - Dense 10 (sortie softmax)

- **Total**: ~2.5M paramètres

## ⚙️ Technologies utilisées

- **TensorFlow/Keras** - Framework de deep learning
- **NumPy** - Calculs numériques
- **Pandas** - Manipulation de données
- **Matplotlib/Seaborn** - Visualisation
- **Pillow/OpenCV** - Traitement d'images
- **scikit-learn** - Métriques d'évaluation
- **Docker** - Conteneurisation

## 📊 Résultats attendus

Avec un dataset de qualité (~200 images/personnage):
- **Précision visée**: 85-95%
- **Temps d'entraînement**: 10-30 minutes (CPU) / 2-5 minutes (GPU)
- **Epochs**: 20-30

Avec le dataset de démonstration:
- **Précision**: ~99% (images synthétiques simples)
- **Temps d'entraînement**: 2-5 minutes

## 🔧 Hyperparamètres

```python
IMG_SIZE = (128, 128)      # Taille des images
BATCH_SIZE = 32            # Taille des batches
EPOCHS = 30                # Nombre d'epochs
LEARNING_RATE = 0.001      # Taux d'apprentissage
```

## 💡 Améliorations possibles

1. **Transfer Learning** - Utiliser VGG16, ResNet50, MobileNetV2
2. **Plus de données** - Augmenter le dataset à 500+ images/personnage
3. **Ensemble methods** - Combiner plusieurs modèles
4. **Data augmentation** - Techniques plus avancées (cutout, mixup)
5. **Fine-tuning** - Ajuster l'architecture selon les erreurs
6. **Déploiement** - API REST pour inférence en production

## 🐛 Problèmes connus

- Le dataset de démonstration utilise des images synthétiques (pour tester le pipeline)
- Pour une vraie reconnaissance, il faut collecter des vraies images
- GPU recommandé pour entraînement rapide sur gros dataset

## 📚 Documentation

- `docs/rendu.md` - Rapport de validation complet
- `docs/prompts_used.md` - Prompts IA utilisés
- `docs/dataset_guide.md` - Guide de création du dataset

## 📝 Licence

Projet éducatif - Workshop Poudlard EPSI

## 👥 Auteurs

- AI Copilot (lead) - Code et entraînement
- Data Copilot - Dataset et rapport

---

> 🧙‍♂️ *"It does not do to dwell on dreams and forget to live... but it's okay to train CNNs!"*  
> — Albus Dumbledore (probablement)
