# 🧙‍♂️ Professeur Dumbledore - Reconnaissance Vocale de Formules Magiques

Système de reconnaissance vocale basé sur l'IA capable d'identifier au moins 8 formules magiques de l'univers Harry Potter (NLU/NLP).

## 🎯 Objectif

Créer une IA de reconnaissance vocale capable d'identifier 10 formules magiques différentes en utilisant des techniques de Natural Language Understanding (NLU) et de traitement audio avancé.

## ✨ Formules reconnues

1. **Expelliarmus** - Sortilège de désarmement
2. **Lumos** - Sortilège de lumière
3. **Nox** - Éteint la lumière
4. **Wingardium Leviosa** - Sortilège de lévitation
5. **Alohomora** - Sortilège d'ouverture
6. **Expecto Patronum** - Invoque un patronus
7. **Avada Kedavra** - Sort impardonnable
8. **Stupefix** - Sortilège de stupéfixion
9. **Protego** - Bouclier protecteur
10. **Accio** - Sortilège d'attraction

## 🏗️ Architecture

```
19-professeur-dumbledore/
├── README.md                       # Ce fichier
├── requirements.txt                # Dépendances Python
├── Dockerfile                      # Configuration Docker
├── docker-compose.snippet.yml      # Configuration Docker Compose
├── src/
│   ├── spell_recognition.ipynb    # Notebook principal d'entraînement
│   └── inference.py               # Script d'inférence
├── data/
│   ├── raw/                       # Données audio brutes
│   └── processed/                 # Données prétraitées
├── models/
│   └── spell-recognition-final/   # Modèle entraîné
├── docs/
│   ├── rendu.md                   # Document de rendu
│   ├── prompts_used.md            # Prompts IA utilisés
│   └── dataset_methodology.md     # Méthodologie du dataset
└── tests/
    └── test_smoke.sh              # Tests de validation
```

## 📋 Prérequis

- Python 3.8+
- CUDA (optionnel, pour GPU)
- Docker et Docker Compose (pour déploiement)

## 🚀 Installation

### Installation locale

```bash
# Clone le repository
cd projects/19-professeur-dumbledore

# Crée un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installe les dépendances
pip install -r requirements.txt

# Lance Jupyter
jupyter notebook src/spell_recognition.ipynb
```

### Installation avec Docker

```bash
docker compose -f docker-compose.snippet.yml up -d
```

Accédez à Jupyter Lab sur http://localhost:8888

## 🎓 Entraînement du modèle

Le notebook `src/spell_recognition.ipynb` contient tout le pipeline d'entraînement:

1. **Création du dataset** avec data augmentation
2. **Prétraitement** des données audio
3. **Définition du modèle** (Wav2Vec2 + fine-tuning)
4. **Entraînement** avec validation
5. **Évaluation** avec métriques détaillées
6. **Sauvegarde** du modèle

Exécutez toutes les cellules du notebook pour entraîner le modèle.

## 🧪 Utilisation

### Inférence avec le notebook

```python
from src.inference import predict_spell
import librosa

# Charge un fichier audio
audio, sr = librosa.load("path/to/spell.wav", sr=16000)

# Prédit la formule
spell, confidence = predict_spell(audio)
print(f"Formule prédite: {spell} (confiance: {confidence:.2%})")
```

### Inférence en ligne de commande

```bash
python src/inference.py --audio path/to/spell.wav
```

## 📊 Métriques du modèle

Le modèle est évalué sur plusieurs métriques:

- **Accuracy** : Précision globale
- **Precision** : Proportion de prédictions correctes
- **Recall** : Capacité à identifier toutes les occurrences
- **F1-Score** : Moyenne harmonique de precision et recall

Résultats disponibles dans:
- `models/classification_report.csv`
- `docs/confusion_matrix.png`
- `docs/metrics_by_spell.png`

## 🎨 Méthodologie du dataset

### Approches de création

1. **Synthèse vocale (TTS)**
   - Génération d'échantillons avec différentes voix
   - Services utilisables: Google TTS, Amazon Polly, gTTS

2. **Enregistrements multiples**
   - Différentes voix et intonations
   - Variations de prononciation et d'accent

3. **Data augmentation**
   - Ajout de bruit de fond
   - Modification du pitch (±2 semi-tons)
   - Time stretching (0.9x à 1.1x)

4. **Collecte de clips**
   - Extraction depuis films/séries Harry Potter
   - Utilisation avec respect du fair use éducatif

Pour plus de détails, consultez `docs/dataset_methodology.md`.

## 🛠️ Technologies utilisées

- **Transformers** (HuggingFace) : Wav2Vec2 pour l'extraction de features
- **PyTorch** : Framework de deep learning
- **Librosa** : Traitement audio
- **Scikit-learn** : Métriques et évaluation
- **Docker** : Containerisation

## 📦 Livrables

✅ **Notebook d'entraînement** (`src/spell_recognition.ipynb`)
- Pipeline complet de création à l'évaluation
- Code commenté et documenté
- Visualisations des résultats

✅ **Dataset et méthodologie** (`docs/dataset_methodology.md`)
- Processus de création détaillé
- Techniques d'augmentation
- Sources et références

✅ **Modèle entraîné** (`models/spell-recognition-final/`)
- Modèle Wav2Vec2 fine-tuné
- Configuration et poids
- Feature extractor

✅ **Métriques d'évaluation**
- Rapport de classification par formule
- Matrice de confusion
- Graphiques de performance

✅ **Documentation complète**
- README technique
- Document de rendu
- Guide d'utilisation

## 🧪 Tests

```bash
# Test de lancement
bash tests/test_smoke.sh

# Test d'inférence
python -m pytest tests/
```

## 🚧 Améliorations futures

- [ ] Augmenter la taille du dataset (100+ échantillons par formule)
- [ ] Utiliser des enregistrements réels de voix humaines
- [ ] Tester d'autres architectures (HuBERT, Whisper)
- [ ] Implémenter la détection en temps réel
- [ ] Ajouter plus de formules magiques
- [ ] Support multilingue (anglais, français)
- [ ] API REST pour l'inférence
- [ ] Application mobile/web

## 👥 Copilots

- 🧠 **AI Copilot** (lead) - Architecture du modèle et entraînement
- 📊 **Data Copilot** - Création et préparation du dataset

## ⏱️ Informations

- **Story Points**: 13
- **Deadline**: 16/10/2025
- **Challenge #19** - Professeur Dumbledore

## 📚 Documentation

- [Rendu complet](docs/rendu.md)
- [Méthodologie du dataset](docs/dataset_methodology.md)
- [Prompts IA utilisés](docs/prompts_used.md)

## 📄 Licence

Projet développé dans le cadre du Workshop "Poudlard à l'EPSI/WIS" 2025.

---

**Note importante**: Ce projet utilise des données audio synthétiques pour la démonstration. Pour une utilisation en production, il est recommandé d'utiliser des enregistrements réels de voix humaines.

✨ *"Les mots sont, à mon humble avis, notre plus inépuisable source de magie."* - Albus Dumbledore
