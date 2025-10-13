# 📘 Pipeline NLP Neuronal - Analyse Harry Potter

> Migration du système d'analyse regex vers une pipeline NLP moderne utilisant des techniques de deep learning et de traitement du langage naturel.

## 🎯 Vue d'ensemble

Ce projet implémente une pipeline d'analyse complète des 7 livres Harry Potter utilisant :
- **spaCy** pour le traitement NLP de base (tokenisation, POS, NER)
- **Patterns avancés** pour l'extraction d'événements spécifiques
- **Jupyter notebooks** pour la reproductibilité et la documentation
- **Visualisations interactives** pour l'exploration des résultats

## 📁 Structure du Projet

```
hp_nlp/
├── notebooks/              # Notebooks Jupyter (pipeline en 5 étapes)
│   ├── 01_ingest_clean.ipynb          # Ingestion et nettoyage
│   ├── 02_nlp_pipeline.ipynb          # Pipeline NLP complet
│   ├── 03_events_extraction.ipynb     # Extraction d'événements
│   ├── 04_aggregation_viz.ipynb       # Agrégations et visualisations
│   └── 05_methods_report.ipynb        # Génération rapport automatique
│
├── data/                   # Données générées (gitignored)
│   ├── sentences.parquet              # Corpus segmenté
│   ├── nlp_processed.parquet          # Annotations NLP
│   ├── events.parquet                 # Événements détectés
│   ├── entities_index.parquet         # Index des entités
│   └── book_metadata.json             # Métadonnées
│
├── outputs/                # Résultats finaux (gitignored)
│   ├── agg_by_book.csv                # Statistiques agrégées
│   ├── agg_by_book.json               # Version JSON
│   ├── methodology_report.html        # Rapport complet
│   ├── events_evolution.png           # Graphiques
│   ├── normalized_stats.png
│   ├── heatmap_events.png
│   ├── dialogues_comparison.png
│   └── summary.md                     # Résumé textuel
│
├── models/                 # Modèles pré-entraînés (optionnel)
├── scripts/                # Scripts utilitaires
├── requirements.txt        # Dépendances Python
├── Makefile               # Automatisation
└── README.md              # Ce fichier
```

## 🚀 Installation Rapide

### Prérequis

- Python 3.11+ (testé avec 3.12)
- 4GB RAM minimum
- 2GB espace disque
- Les livres Harry Potter en PDF dans `../../context/books/`

### Installation

```bash
# Cloner et naviguer
cd hp_nlp/

# Installation automatique (recommandé)
make setup

# OU installation manuelle
pip install -r requirements.txt
python -m spacy download fr_core_news_lg
```

## 📊 Utilisation

### Exécution Complète

```bash
# Exécuter tout le pipeline (5 notebooks)
make run

# Les résultats seront dans outputs/
# Le rapport HTML sera généré automatiquement
```

### Exécution par Étapes

```bash
# Étape 1: Ingestion et nettoyage
make run-nb1

# Étape 2: Pipeline NLP
make run-nb2

# Étape 3: Extraction d'événements
make run-nb3

# Étape 4: Agrégation et visualisations
make run-nb4

# Étape 5: Génération du rapport
make run-nb5
```

### Développement Interactif

```bash
# Lancer Jupyter Lab
make jupyter

# Puis ouvrir les notebooks dans l'interface
```

### Commandes Utiles

```bash
make help              # Afficher toutes les commandes
make test              # Vérifier l'installation
make stats             # Statistiques du projet
make report            # Générer uniquement le rapport
make open-report       # Ouvrir le rapport dans le navigateur
make clean             # Nettoyer tous les fichiers générés
make clean-outputs     # Nettoyer uniquement les outputs
```

## 📖 Pipeline Détaillé

### Notebook 1 - Ingestion et Nettoyage (01_ingest_clean.ipynb)

**Objectif :** Extraire et préparer le texte des PDFs.

**Sorties :**
- `data/sentences.parquet` : Corpus segmenté par phrases
- `data/book_metadata.json` : Métadonnées des livres

**Fonctionnalités :**
- Extraction PDF avec PyPDF2
- Nettoyage et normalisation du texte
- Segmentation en phrases
- Validation des données

### Notebook 2 - Pipeline NLP (02_nlp_pipeline.ipynb)

**Objectif :** Appliquer les techniques NLP avancées.

**Sorties :**
- `data/nlp_processed.parquet` : Corpus avec annotations NLP
- `data/entities_index.parquet` : Index des entités nommées

**Fonctionnalités :**
- Named Entity Recognition (NER) avec spaCy
- Détection et attribution de locuteur (dialogues)
- Normalisation des noms de personnages
- Index des mentions de personnages

**Taux de succès :**
- Attribution de locuteur : ~75-85% sur dialogues détectés
- Reconnaissance d'entités : dépend du modèle spaCy utilisé

### Notebook 3 - Extraction d'Événements (03_events_extraction.ipynb)

**Objectif :** Détecter les événements spécifiques.

**Sorties :**
- `data/events.parquet` : Corpus avec événements détectés
- `data/events_summary.parquet` : Résumé des événements

**Événements détectés :**

1. **Cicatrice de Harry** 🔥
   - Détection : patterns de toucher/sensation de cicatrice
   - Critères : mention de Harry + cicatrice + action/sensation

2. **Hermione dit "Mais"** 💬
   - Détection : comptage dans dialogues attribués à Hermione
   - Critères : dialogue + locuteur Hermione + mot "Mais"

3. **Interventions Dumbledore** 🧙
   - Détection : moments décisifs changeant le cours de l'histoire
   - Types : décisions, exceptions, révélations, points

4. **Rogue mystérieux** 🖤
   - Détection : descriptions sombres/mystérieuses
   - Sentiments : menaçant, froid, cruel, suspicieux

5. **Actes répréhensibles** ⚖️
   - Classification multi-catégories
   - Catégories : mensonge, vol, violation de règles, violence, intrusion

### Notebook 4 - Agrégation et Visualisations (04_aggregation_viz.ipynb)

**Objectif :** Agréger les résultats et créer des visualisations.

**Sorties :**
- `outputs/agg_by_book.csv` : Statistiques agrégées par livre
- `outputs/agg_by_book.json` : Version JSON
- `outputs/*.png` : 4 graphiques de qualité

**Analyses :**
- Statistiques brutes par livre
- Normalisation par 100 pages
- Normalisation par 10k mots
- Comparaison des prises de parole (Harry, Hermione, Ron)
- Heatmap complète des événements

**Visualisations générées :**
1. `events_evolution.png` : Évolution des 5 types d'événements + dialogues
2. `normalized_stats.png` : Statistiques normalisées (4 métriques)
3. `heatmap_events.png` : Heatmap des événements par livre
4. `dialogues_comparison.png` : Comparaison totale des dialogues

### Notebook 5 - Rapport Méthodologique (05_methods_report.ipynb)

**Objectif :** Générer un rapport complet automatiquement.

**Sorties :**
- `outputs/methodology_report.html` : Rapport autonome complet
- `outputs/methodology_report.pdf` : Version PDF (optionnel)

**Contenu du rapport :**
- Résumé exécutif avec métriques globales
- Méthodologie détaillée (pipeline, technologies, algorithmes)
- Résultats avec toutes les visualisations
- Limites et considérations méthodologiques
- Instructions de reproductibilité

## 📈 Résultats Attendus

Après exécution complète, vous obtiendrez :

### Métriques Globales
- ~50,000+ phrases analysées (varie selon les livres disponibles)
- ~1,000,000+ mots traités
- ~3,500+ pages

### Événements (estimations sur échantillon)
- Cicatrice de Harry : 150-200 occurrences
- Hermione dit "Mais" : 80-120 occurrences
- Interventions Dumbledore : 200-300 occurrences
- Rogue mystérieux : 150-250 occurrences
- Actes répréhensibles : 1,000-1,500 occurrences

### Dialogues
- Harry : ~800-1,000 prises de parole
- Hermione : ~700-900 prises de parole
- Ron : ~600-800 prises de parole

## 🔬 Méthodologie

### Technologies NLP

**spaCy fr_core_news_lg**
- Tokenisation et segmentation
- Part-of-Speech (POS) tagging
- Named Entity Recognition (NER)
- Lemmatisation

**Patterns et Heuristiques**
- Regex avancées pour dialogues français
- Normalisation d'entités vers personnages canoniques
- Détection d'événements par combinaison de patterns

**Normalisation**
- Par 100 pages : permet comparaison entre livres
- Par 10k mots : métrique alternative plus précise

### Limites Connues

1. **Attribution de locuteur**
   - Dialogues ambigus (15-25% d'erreur estimée)
   - Dialogues sans attribution explicite
   - Pronoms non résolus (il/elle)

2. **Détection d'événements**
   - Patterns basés sur heuristiques (pas de ML supervisé)
   - Contexte implicite difficile à capturer
   - Ironie non détectée

3. **Traduction française**
   - Patterns peuvent différer de l'original anglais
   - Guillemets français (« ») vs anglais (" ")

4. **Extraction PDF**
   - Erreurs d'encodage possibles
   - Mise en page complexe

### Améliorations Futures

- [ ] Résolution de coréférence (coreferee/fastcoref)
- [ ] Modèles Transformers pour attribution de locuteur
- [ ] Zero-shot NLI pour classification sémantique
- [ ] Fine-tuning sur corpus Harry Potter
- [ ] Annotation manuelle pour validation
- [ ] Support multilingue (anglais original)

## 🧪 Tests et Validation

### Tests Automatiques

```bash
# Vérifier l'environnement
make test

# Devrait afficher :
# ✅ pandas
# ✅ spaCy
# ✅ Modèle français chargé
# ✅ matplotlib
# ✅ jupyter
```

### Validation Manuelle

1. **Smoke Test**
   ```bash
   make run-nb1  # Doit créer data/sentences.parquet
   ```

2. **Test Complet sur 1 Livre**
   - Modifier `SAMPLE_SIZE` dans les notebooks
   - Exécuter `make run`
   - Vérifier les sorties dans `outputs/`

3. **Validation des Résultats**
   - Ouvrir le rapport HTML
   - Vérifier la cohérence des statistiques
   - Examiner les graphiques

## 🔧 Dépannage

### Problème : Modèle spaCy non trouvé

```bash
# Solution
python -m spacy download fr_core_news_lg
# OU
python -m spacy download fr_core_news_sm
```

### Problème : Mémoire insuffisante

```python
# Dans les notebooks, réduire SAMPLE_SIZE
SAMPLE_SIZE = 1000  # Au lieu de 5000
```

### Problème : PDF non trouvés

```bash
# Vérifier le chemin
ls ../../context/books/*.pdf

# Ajuster BOOKS_DIR dans les notebooks si nécessaire
```

### Problème : Jupyter ne démarre pas

```bash
# Réinstaller jupyter
pip install --upgrade jupyter notebook
```

## 📚 Documentation Complémentaire

### Ressources

- [spaCy Documentation](https://spacy.io/usage)
- [Pandas User Guide](https://pandas.pydata.org/docs/)
- [Jupyter Notebook Docs](https://jupyter-notebook.readthedocs.io/)
- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/)

### Papiers et Références

- spaCy: Industrial-strength NLP (Honnibal & Montani, 2017)
- Named Entity Recognition: A Survey (Yadav & Bethard, 2019)

## 🤝 Contribution

Ce projet fait partie du Workshop Poudlard EPSI. Pour contribuer :

1. Créer une branche feature
2. Implémenter les améliorations
3. Tester avec `make test` et `make run`
4. Soumettre une pull request

## 📄 Licence

Projet éducatif - EPSI Workshop Poudlard

---

## ✨ Quick Start Résumé

```bash
# 1. Installer
make setup

# 2. Exécuter
make run

# 3. Voir les résultats
make open-report

# C'est tout ! 🎉
```

**Temps d'exécution estimé :** 10-30 minutes selon le matériel et le nombre de livres.

**Résultats :** Rapport HTML complet avec toutes les analyses et visualisations.

---

*Généré avec 🧙‍♂️ pour l'analyse de la saga Harry Potter*
