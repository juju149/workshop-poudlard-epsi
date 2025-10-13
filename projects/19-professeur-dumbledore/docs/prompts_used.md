# 💬 Prompts IA utilisés – Défi 19: Professeur Dumbledore

Ce document archive tous les prompts utilisés pour générer le code, la documentation et les ressources de ce projet.

---

## 🔹 Prompt 1 – Architecture globale du projet

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Définir l'architecture du projet de reconnaissance vocale

```
Crée l'architecture complète d'un projet de reconnaissance vocale pour identifier 
au moins 8 formules magiques Harry Potter. Le projet doit inclure:

1. Un notebook Jupyter pour l'entraînement
2. Un modèle basé sur Wav2Vec2 ou similaire
3. Un pipeline de data augmentation
4. Des métriques d'évaluation complètes
5. Un script d'inférence
6. Une configuration Docker

Structure le projet selon les standards définis dans agents/AGENTS.md avec:
- README.md
- requirements.txt
- Dockerfile
- docker-compose.snippet.yml
- docs/rendu.md
- docs/prompts_used.md
- tests/test_smoke.sh
```

---

## 🔹 Prompt 2 – Notebook d'entraînement Jupyter

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Créer le notebook principal d'entraînement

```
Crée un notebook Jupyter complet pour l'entraînement d'un modèle de reconnaissance 
vocale de formules magiques Harry Potter. Le notebook doit inclure:

1. Introduction et objectifs
2. Installation des dépendances
3. Création du dataset (avec méthodologie pour générer des échantillons synthétiques 
   ou utiliser des TTS)
4. Data augmentation (pitch shifting, time stretching, ajout de bruit)
5. Prétraitement des données audio
6. Architecture du modèle (Wav2Vec2 + classification head)
7. Entraînement avec validation
8. Évaluation complète avec:
   - Accuracy, Precision, Recall, F1-Score
   - Matrice de confusion
   - Rapport de classification par formule
9. Visualisations (graphiques des métriques)
10. Sauvegarde du modèle
11. Tests d'inférence

Formules à reconnaître (minimum 8, objectif 10):
- Expelliarmus, Lumos, Nox, Wingardium Leviosa, Alohomora, 
  Expecto Patronum, Avada Kedavra, Stupefix, Protego, Accio

Utilise des bibliothèques modernes: transformers, librosa, torch, scikit-learn
Code bien commenté et structuré avec des markdown cells explicatives.
```

---

## 🔹 Prompt 3 – Script d'inférence Python

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Créer un script CLI pour l'inférence

```
Crée un script Python d'inférence pour la reconnaissance de formules magiques.
Le script doit:

1. Charger un modèle Wav2Vec2 entraîné depuis un dossier
2. Charger les configurations (formules, sample rate, etc.) depuis un JSON
3. Prétraiter un fichier audio (padding, normalisation)
4. Faire une prédiction avec probabilités
5. Afficher les résultats formatés

Interface en ligne de commande:
```bash
python inference.py --audio path/to/spell.wav --model models/spell-recognition-final
```

Affichage:
- Formule prédite avec confiance
- Top-3 des prédictions avec barres de progression
- Format agréable et lisible

Inclus aussi une classe SpellRecognizer réutilisable pour l'intégration.
```

---

## 🔹 Prompt 4 – Dockerfile et Docker Compose

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Configuration Docker pour reproductibilité

```
Crée un Dockerfile et docker-compose.yml pour un projet de machine learning audio.

Dockerfile:
- Base image: python:3.9-slim
- Installer les dépendances système: libsndfile1, ffmpeg, build-essential
- Installer les dépendances Python depuis requirements.txt
- Copier le code source (src/, data/, models/)
- Exposer le port 8888 pour Jupyter Lab
- CMD: lancer Jupyter Lab sans token

docker-compose.snippet.yml:
- Service: spell-recognition
- Build depuis Dockerfile local
- Port mapping: 8888:8888
- Volumes: src/, data/, models/, docs/
- Network: poudlard-network
- Restart policy: unless-stopped

Optimisé pour le développement et l'entraînement de modèles.
```

---

## 🔹 Prompt 5 – Documentation README.md

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Créer le README principal du projet

```
Crée un README.md professionnel et complet pour un projet de reconnaissance 
vocale de formules magiques Harry Potter.

Sections:
1. Titre et description
2. Objectif (identifier 10 formules magiques)
3. Liste des formules reconnues
4. Architecture du projet (arborescence)
5. Prérequis
6. Installation (locale et Docker)
7. Entraînement du modèle
8. Utilisation (inférence)
9. Métriques du modèle
10. Méthodologie du dataset
11. Technologies utilisées
12. Livrables
13. Tests
14. Améliorations futures
15. Copilots recommandés
16. Informations (story points, deadline)

Style:
- Emojis pour les sections
- Code blocks formatés
- Liens vers la documentation
- Citations Harry Potter
- Professionnel mais accessible
```

---

## 🔹 Prompt 6 – Document de rendu (docs/rendu.md)

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Créer le document de rendu officiel pour le jury

```
Crée un document de rendu complet selon le template des agents/AGENTS.md.

Structure obligatoire:
1. 🎯 Objectif
2. 🧩 Architecture (composants, diagrammes)
3. ⚙️ Technologies utilisées
4. 🚀 Lancement rapide
5. 🧪 Tests
6. 📊 Métriques et performances (avec tableaux de résultats)
7. 📦 Dataset - Méthodologie de création (détaillée)
8. 💾 Modèle entraîné
9. 🔧 Détails techniques (hyperparamètres, preprocessing)
10. 🧠 Notes & Retours (points forts, limitations, améliorations)
11. 📈 Évolution du projet
12. 👥 Équipe et rôles
13. 📚 Références
14. 📝 Checklist de livraison

Inclus des diagrammes ASCII pour l'architecture du modèle et le pipeline.
Très détaillé et technique, adapté pour un jury d'experts.
```

---

## 🔹 Prompt 7 – Méthodologie du dataset (docs/dataset_methodology.md)

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Documenter la création du dataset

```
Crée un document exhaustif sur la méthodologie de création d'un dataset audio 
pour la reconnaissance de formules magiques.

Sections:
1. Objectif et formules cibles
2. Approches de collecte:
   - Synthèse vocale (TTS) avec exemples de code
   - Enregistrements humains (protocole détaillé)
   - Extraction de médias (avec considérations légales)
3. Data augmentation:
   - Techniques (bruit, pitch, time stretch, réverb, volume)
   - Exemples de code pour chaque technique
   - Pipeline d'augmentation complet
4. Prétraitement (normalisation, resampling, padding, filtrage)
5. Structure finale du dataset
6. Statistiques recommandées (tableaux)
7. Checklist de qualité
8. Pipeline automatisé
9. Ressources et outils
10. Conseils pratiques

Inclus beaucoup d'exemples de code Python fonctionnels.
Approche académique et professionnelle.
```

---

## 🔹 Prompt 8 – Script de test (tests/test_smoke.sh)

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Créer un test de validation basique

```
Crée un script bash de test smoke pour valider le projet de reconnaissance vocale.

Le script doit:
1. Vérifier l'installation de Python et pip
2. Vérifier la présence de requirements.txt
3. Installer les dépendances dans un venv temporaire
4. Tester l'import des bibliothèques principales
5. Vérifier la présence du notebook et des fichiers clés
6. Optionnel: tester le chargement du modèle si présent
7. Afficher un rapport de réussite/échec

Format:
- Utilise des couleurs (vert pour succès, rouge pour erreur)
- Emojis pour les étapes
- Messages clairs
- Exit code approprié (0 si succès, 1 si échec)

Compatible Linux et macOS.
```

---

## 🔹 Prompt 9 – requirements.txt

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Lister toutes les dépendances Python

```
Crée un fichier requirements.txt complet pour un projet de reconnaissance vocale.

Dépendances nécessaires:
- transformers (HuggingFace)
- datasets
- torch et torchaudio
- librosa (traitement audio)
- soundfile
- numpy, pandas
- scikit-learn (métriques)
- matplotlib, seaborn (visualisation)
- tqdm (barres de progression)
- jupyter (notebook)

Spécifie des versions minimales compatibles.
Ajoute des commentaires pour les groupes de dépendances.
```

---

## 🔹 Prompt 10 – Visualisations et métriques

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Créer des visualisations dans le notebook

```
Ajoute au notebook Jupyter des cellules pour créer des visualisations complètes:

1. Matrice de confusion (heatmap avec seaborn)
   - Axes: formules magiques
   - Annotations avec valeurs
   - Couleurs: Blues
   - Sauvegarde en PNG haute résolution

2. Graphiques de métriques par formule (3 subplots):
   - Precision par formule (bar chart)
   - Recall par formule (bar chart)
   - F1-Score par formule (bar chart)
   - Rotation des labels à 45°
   
3. Rapport de classification (tableau pandas)
   - Sauvegarde en CSV

Tous les graphiques doivent:
- Avoir des titres clairs
- Être sauvegardés dans docs/
- Avoir une résolution de 300 DPI
- Utiliser un style professionnel
```

---

## 🔹 Prompt 11 – Configuration du modèle JSON

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Sauvegarder la configuration du modèle

```
Dans le notebook, ajoute une cellule pour sauvegarder la configuration complète 
du modèle entraîné dans un fichier config.json:

Contenu:
- Liste des formules magiques
- Mapping spell_to_id et id_to_spell
- Sample rate et durée max
- Nom du modèle de base utilisé
- Métriques finales (accuracy, precision, recall, f1)

Format JSON avec indentation propre.
Sauvegarde dans models/spell-recognition-final/config.json
```

---

## 🔹 Prompt 12 – Gitignore pour le projet

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Créer un .gitignore approprié

```
Crée un fichier .gitignore pour un projet de machine learning Python.

Ignorer:
- Environnements virtuels (venv/, env/, .venv/)
- Cache Python (__pycache__/, *.pyc, *.pyo)
- Jupyter checkpoints (.ipynb_checkpoints/)
- Fichiers volumineux de modèles (*.bin, *.pt, *.pth) sauf si nécessaire
- Données audio brutes (data/raw/) sauf échantillons
- Logs et tensorboard (logs/, runs/)
- IDE (VSCode, PyCharm, etc.)
- OS (.DS_Store, Thumbs.db)

Garde:
- Structure des dossiers (avec .gitkeep si vides)
- Documentation
- Configuration
```

---

## 🔹 Prompt 13 – Amélioration de la documentation inline

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Ajouter des commentaires dans le code

```
Révise le code Python et ajoute:
1. Docstrings pour toutes les fonctions (format Google)
2. Commentaires inline pour la logique complexe
3. Type hints pour les paramètres et retours
4. Exemples d'utilisation dans les docstrings

Exemple de docstring:
```python
def predict_spell(audio_path: str) -> Tuple[str, float]:
    """
    Prédit la formule magique à partir d'un fichier audio.
    
    Args:
        audio_path: Chemin vers le fichier audio WAV
        
    Returns:
        Tuple contenant:
            - str: Nom de la formule prédite
            - float: Confiance de la prédiction (0-1)
            
    Example:
        >>> spell, confidence = predict_spell("lumos.wav")
        >>> print(f"{spell}: {confidence:.2%}")
        lumos: 95.34%
    """
```

Style professionnel et académique.
```

---

## 📊 Statistiques des prompts

| Catégorie | Nombre de prompts | Description |
|-----------|-------------------|-------------|
| Architecture & Structure | 2 | Structure du projet, organisation |
| Code (Notebook, Scripts) | 3 | Notebook d'entraînement, inférence |
| Documentation | 4 | README, rendu, méthodologie, prompts |
| Configuration | 3 | Docker, requirements, gitignore |
| Tests & Validation | 1 | Tests automatisés |
| Visualisation | 1 | Graphiques et métriques |
| Qualité du code | 1 | Documentation inline |

**Total**: 13 prompts principaux

---

## 💡 Notes sur l'utilisation des prompts

### Stratégie de prompting

1. **Prompts structurés**: Chaque prompt inclut des sections claires (objectif, contenu, format)
2. **Exemples concrets**: Fournis pour guider la génération
3. **Contraintes explicites**: Technologies, format, style spécifiés
4. **Itération**: Certains prompts sont des révisions/améliorations de sorties précédentes

### Bonne pratiques appliquées

✅ **Spécificité**: Prompts précis avec des exigences claires
✅ **Contexte**: Référence aux standards du projet (AGENTS.md)
✅ **Format**: Structure de sortie attendue spécifiée
✅ **Exemples**: Code examples fournis quand pertinent
✅ **Contraintes**: Bibliothèques, versions, compatibilité mentionnées

### Révisions et itérations

Certains outputs ont nécessité des ajustements:
- Ajout de commentaires supplémentaires dans le code
- Amélioration de la structure des visualisations
- Clarification de la méthodologie du dataset
- Optimisation de la configuration Docker

---

## 🎓 Apprentissages

### Ce qui a bien fonctionné

1. **Prompts détaillés**: Plus le prompt est détaillé, meilleure est la sortie
2. **Référence aux standards**: Mentionner AGENTS.md aide à la cohérence
3. **Exemples de code**: Très utiles pour le format attendu
4. **Structure en sections**: Aide l'IA à organiser la réponse

### Points d'amélioration

1. Certains prompts auraient pu être plus spécifiques sur les hyperparamètres
2. La méthodologie de dataset aurait pu être développée en plusieurs prompts
3. Plus d'itérations sur les visualisations pour perfectionner le style

---

## 📝 Méthodologie de documentation des prompts

Chaque prompt documenté inclut:
- **Date**: Quand le prompt a été utilisé
- **Outil**: Quel outil IA (GitHub Copilot, ChatGPT, etc.)
- **Objectif**: But du prompt
- **Contenu**: Le prompt complet
- **Résultat**: Fichier(s) généré(s) (mentionné implicitement)

---

✨ *"Les prompts sont les incantations du développeur moderne."*

---

**Note**: Ce document est un livrable obligatoire selon le standard défini dans `agents/AGENTS.md`. Il démontre l'utilisation intelligente des outils IA et assure la traçabilité du processus de création.
