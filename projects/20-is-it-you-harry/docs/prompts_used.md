# 💬 Prompts IA utilisés – Défi 20: IS IT YOU HARRY?

Ce document liste tous les prompts utilisés avec des outils d'IA pour générer le code, la documentation et l'architecture de ce projet de reconnaissance de personnages Harry Potter par CNN.

---

## 🔹 Prompt 1 – Architecture globale du projet

**Date**: 2025-10-15  
**Outil**: GitHub Copilot  
**Objectif**: Définir la structure complète du projet

```
Crée la structure d'un projet de deep learning pour reconnaître 10 personnages 
d'Harry Potter avec un CNN. Le projet doit suivre la convention du workshop 
Poudlard EPSI:

- Structure: projects/20-is-it-you-harry/
- Inclure: src/, data/, models/, docs/, tests/
- Fichiers: Dockerfile, docker-compose.snippet.yml, requirements.txt
- Documentation: README.md, docs/rendu.md, docs/prompts_used.md
- Dataset organisé en train/val/test (70/15/15)
- Notebook Jupyter principal pour tout le pipeline
- Tests automatiques (test_smoke.sh)

Utiliser TensorFlow/Keras pour le modèle CNN.
```

---

## 🔹 Prompt 2 – Notebook Jupyter principal

**Date**: 2025-10-15  
**Outil**: GitHub Copilot  
**Objectif**: Créer le notebook complet avec pipeline ML

```
Crée un notebook Jupyter (character_recognition.ipynb) pour reconnaître 
10 personnages d'Harry Potter avec un CNN. Le notebook doit inclure:

1. Introduction et objectifs
2. Import des bibliothèques (TensorFlow, Keras, NumPy, Pandas, Matplotlib, etc.)
3. Configuration (chemins, hyperparamètres, liste des personnages)
4. Fonction pour créer un dataset de démonstration avec images synthétiques
5. Exploration du dataset (statistiques, visualisations)
6. Data augmentation avec ImageDataGenerator
7. Architecture CNN personnalisée:
   - 4 blocs convolutifs (32, 64, 128, 256 filtres)
   - BatchNormalization et Dropout
   - 2 couches fully connected (512, 256)
   - Sortie softmax (10 classes)
8. Callbacks: ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
9. Entraînement du modèle
10. Visualisation des courbes (accuracy, loss)
11. Évaluation sur test set
12. Matrice de confusion avec Seaborn
13. Rapport de classification détaillé
14. Sauvegarde du modèle et métadonnées
15. Analyse des erreurs
16. Résumé final avec statistiques

Personnages: Harry, Hermione, Ron, Dumbledore, Snape, Voldemort, Draco, 
Hagrid, McGonagall, Sirius Black

Utiliser des commentaires et markdown cells pour expliquer chaque étape.
```

---

## 🔹 Prompt 3 – README.md

**Date**: 2025-10-15  
**Outil**: GitHub Copilot  
**Objectif**: Créer la documentation principale du projet

```
Rédige un README.md complet pour le projet de reconnaissance de personnages 
Harry Potter par CNN. Inclure:

1. Titre avec emoji et description
2. Objectif du projet
3. Liste des 10 personnages reconnus
4. Architecture du projet (arborescence des fichiers)
5. Prérequis (Python, TensorFlow, Docker)
6. Installation (locale et Docker)
7. Structure du dataset recommandée
8. Guide d'utilisation (entraînement, évaluation, inférence)
9. Tests (commande pour test_smoke.sh)
10. Architecture du modèle CNN (détails techniques)
11. Technologies utilisées
12. Résultats attendus (précision, temps)
13. Hyperparamètres
14. Améliorations possibles
15. Problèmes connus
16. Documentation associée
17. Licence et auteurs
18. Citation Harry Potter en conclusion

Style: Clair, professionnel, avec emojis pour rendre attractif.
Format: Markdown avec code blocks, tableaux, listes.
```

---

## 🔹 Prompt 4 – Documentation rendu.md

**Date**: 2025-10-15  
**Outil**: GitHub Copilot  
**Objectif**: Créer le document de rendu pour le jury

```
Rédige un document de rendu complet (docs/rendu.md) pour le défi 20 
"IS IT YOU HARRY?" selon le template standard du workshop Poudlard.

Sections obligatoires:
1. 🎯 Objectif - Description claire de l'objectif atteint
2. 🧩 Architecture - Composants, pipeline, architecture CNN détaillée en ASCII
3. ⚙️ Technologies utilisées - Liste complète avec versions
4. 🚀 Lancement rapide - Commandes Docker et local
5. 📊 Dataset - Structure, personnages, création, data augmentation
6. 🎓 Entraînement - Hyperparamètres, callbacks, optimiseur, durée
7. 📈 Résultats - Métriques, visualisations, fichiers générés
8. 🧪 Tests - Script de validation
9. 🔍 Analyse des erreurs - Erreurs typiques et pistes d'amélioration
10. 💾 Modèle entraîné - Chargement et inférence
11. 🐛 Limitations - Problèmes connus
12. 📚 Documentation complémentaire
13. 🎯 Checklist de validation
14. 🏆 Conclusion - Points forts et prochaines étapes

Inclure des tableaux, des diagrammes ASCII, et des exemples de code.
Style: Professionnel mais accessible, avec emojis.
```

---

## 🔹 Prompt 5 – Dataset guide

**Date**: 2025-10-15  
**Outil**: GitHub Copilot  
**Objectif**: Guide pour créer le dataset réel

```
Crée un guide pratique (docs/dataset_guide.md) pour collecter et organiser 
un dataset d'images de personnages Harry Potter. Inclure:

1. Introduction - Pourquoi un bon dataset est crucial
2. Méthodes de collecte:
   - Web scraping (Google Images, Bing, Pinterest)
   - Captures d'écran des films
   - Génération IA (Stable Diffusion, DALL-E)
   - Datasets existants (Kaggle, etc.)
3. Recommandations:
   - Nombre d'images par personnage (200+)
   - Variété (angles, expressions, scènes)
   - Qualité (résolution, netteté)
   - Équilibre entre classes
4. Organisation:
   - Structure des dossiers
   - Nommage des fichiers
   - Split train/val/test
5. Nettoyage:
   - Supprimer duplicatas
   - Vérifier la qualité
   - Labellisation correcte
6. Preprocessing:
   - Redimensionnement
   - Normalisation
   - Data augmentation
7. Outils recommandés (Python scripts, libraries)
8. Checklist de qualité du dataset
9. Exemples de commandes

Style: Pédagogique, avec exemples concrets.
```

---

## 🔹 Prompt 6 – Dockerfile et docker-compose

**Date**: 2025-10-15  
**Outil**: GitHub Copilot  
**Objectif**: Containerisation du projet

```
Crée un Dockerfile et docker-compose.snippet.yml pour le projet de 
reconnaissance de personnages Harry Potter. 

Dockerfile:
- Base: python:3.10-slim
- Installer dépendances système (libgl1-mesa-glx, libglib2.0-0)
- Copier requirements.txt et installer dépendances Python
- Copier src/, data/, models/
- Exposer port 8888 (Jupyter)
- CMD: lancer Jupyter sans token

docker-compose.snippet.yml:
- Service: character-recognition
- Ports: 8888:8888
- Volumes: src, data, models, output
- Network: poudlard-network
- Restart: unless-stopped
- Environment: PYTHONUNBUFFERED=1

Optimiser pour layer caching et build rapide.
```

---

## 🔹 Prompt 7 – requirements.txt

**Date**: 2025-10-15  
**Outil**: GitHub Copilot  
**Objectif**: Lister les dépendances Python

```
Génère un requirements.txt pour un projet de CNN avec TensorFlow/Keras. Inclure:

Core ML/DL:
- tensorflow==2.15.0
- keras==2.15.0
- numpy==1.24.3
- pandas==2.1.1
- scikit-learn==1.3.1

Image processing:
- pillow==10.1.0
- opencv-python==4.8.1.78

Visualization:
- matplotlib==3.8.0
- seaborn==0.13.0

Jupyter:
- jupyter==1.0.0
- ipykernel==6.26.0
- notebook==7.0.6

Utilities:
- tqdm==4.66.1
- pyyaml==6.0.1

Organiser par catégories avec commentaires.
```

---

## 🔹 Prompt 8 – Script de test (test_smoke.sh)

**Date**: 2025-10-15  
**Outil**: GitHub Copilot  
**Objectif**: Créer le script de validation automatique

```
Crée un script bash test_smoke.sh qui vérifie:

1. Structure du projet (src/, docs/, tests/, data/, models/)
2. Présence des fichiers essentiels:
   - README.md
   - requirements.txt
   - Dockerfile
   - docker-compose.snippet.yml
   - src/character_recognition.ipynb
   - docs/rendu.md
   - docs/prompts_used.md
3. Syntaxe Python du notebook (nbconvert --to script)
4. Installation de Python et modules clés (tensorflow, keras, numpy)
5. Création des répertoires data/train, data/val, data/test
6. Docker installé (optionnel)
7. Permissions des fichiers

Utiliser des couleurs (GREEN, RED, YELLOW) et des emojis.
Afficher des messages clairs pour chaque vérification.
Retourner exit code approprié (0 = succès, 1 = échec).
Instructions finales: comment lancer le notebook.

Style: Robuste avec set -e et gestion d'erreurs.
```

---

## 🔹 Prompt 9 – .gitignore

**Date**: 2025-10-15  
**Outil**: GitHub Copilot  
**Objectif**: Exclure fichiers non nécessaires du repo

```
Génère un .gitignore pour un projet Python de deep learning. Exclure:

Python:
- __pycache__/, *.pyc, *.pyo, *.so
- venv/, env/, .venv/
- *.egg-info/, build/, dist/

Jupyter:
- .ipynb_checkpoints/

IDE:
- .vscode/, .idea/

Machine Learning:
- *.h5, *.hdf5 (sauf modèles finaux)
- models/checkpoints/
- logs/, runs/, mlruns/

Data:
- data/train/**/*.jpg
- data/val/**/*.jpg
- data/test/**/*.jpg
(garder structure avec .gitkeep)

OS:
- .DS_Store, Thumbs.db, *.swp

Docker:
- docker-compose.override.yml

Archives:
- *.zip, *.tar.gz

Garder: .gitkeep pour préserver structure des dossiers
```

---

## 🔹 Prompt 10 – Guide dataset (dataset_guide.md)

**Date**: 2025-10-15  
**Outil**: GitHub Copilot  
**Objectif**: Guide pratique de collecte de données

```
Rédige un guide complet (docs/dataset_guide.md) pour créer un dataset 
d'images de personnages Harry Potter. Sections:

1. Introduction - Importance du dataset
2. Objectif - 10 personnages, 200 images chacun
3. Sources de données:
   - Google Images (avec filtres)
   - Bing Images
   - Pinterest
   - Captures d'écran films/séries
   - Kaggle datasets
   - Génération IA (Stable Diffusion, DALL-E)
4. Méthodes de collecte:
   - Web scraping (BeautifulSoup, Selenium)
   - Download managers
   - Scripts Python automatisés
5. Organisation:
   - Structure folders (train/val/test)
   - Naming convention
   - Split ratio (70/15/15)
6. Critères de qualité:
   - Résolution minimum (128x128)
   - Netteté, éclairage
   - Variété (angles, expressions)
   - Pas de watermarks
7. Nettoyage:
   - Supprimer duplicatas (imagehash)
   - Vérifier labels
   - Filtrer basse qualité
8. Preprocessing:
   - Redimensionnement uniforme
   - Augmentation (rotation, flip, crop)
9. Validation:
   - Vérifier distribution
   - Tester avec modèle simple
10. Outils recommandés:
    - Python libraries (requests, PIL, opencv)
    - Scripts fournis
11. Exemples de code
12. Checklist finale

Style: Tutoriel pratique avec code et commandes.
```

---

## 📊 Résumé de l'usage IA

| Composant | Prompt utilisé | Outil IA | Génération |
|-----------|---------------|----------|------------|
| Architecture projet | Prompt 1 | GitHub Copilot | Structure complète |
| Notebook Jupyter | Prompt 2 | GitHub Copilot | Code et cellules |
| README.md | Prompt 3 | GitHub Copilot | Documentation |
| docs/rendu.md | Prompt 4 | GitHub Copilot | Rapport final |
| Dataset guide | Prompt 5, 10 | GitHub Copilot | Guide pratique |
| Dockerfile | Prompt 6 | GitHub Copilot | Configuration |
| docker-compose | Prompt 6 | GitHub Copilot | Orchestration |
| requirements.txt | Prompt 7 | GitHub Copilot | Dépendances |
| test_smoke.sh | Prompt 8 | GitHub Copilot | Tests |
| .gitignore | Prompt 9 | GitHub Copilot | Exclusions |

---

## 🎯 Méthodologie d'utilisation de l'IA

1. **Planification** - Définir structure et objectifs avant génération
2. **Prompts détaillés** - Spécifier tous les détails attendus
3. **Itération** - Affiner les prompts selon résultats
4. **Validation** - Vérifier le code généré, tester
5. **Personnalisation** - Adapter aux besoins spécifiques du projet
6. **Documentation** - Archiver tous les prompts utilisés

---

## 💡 Bonnes pratiques identifiées

✅ **Prompts structurés** - Utiliser listes numérotées pour clarté  
✅ **Contexte explicite** - Mentionner framework, versions, conventions  
✅ **Exemples concrets** - Donner des exemples de sortie attendue  
✅ **Style défini** - Spécifier ton, format, emojis  
✅ **Contraintes claires** - Préciser limites et exigences  
✅ **Validation humaine** - Toujours vérifier et tester le code généré  

---

> 🤖 *"Intelligence Artificielle, c'est bien. Intelligence Humaine + IA, c'est magique!"*
