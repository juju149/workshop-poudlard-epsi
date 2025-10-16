# 🧾 Rendu – LE PROCÈS DE J.K. ROWLING (Défi 22)

## 🎯 Objectif

Créer une pipeline NLP neuronal complète pour analyser les 7 livres Harry Potter et extraire automatiquement des événements, statistiques et insights narratifs, en remplaçant l'approche regex par des techniques modernes de traitement du langage naturel (spaCy, deep learning).

---

## 🧩 Architecture

### Modules principaux

1. **Ingestion et nettoyage** (`01_ingest_clean.ipynb`)
   - Chargement des textes bruts
   - Segmentation en phrases
   - Nettoyage et normalisation

2. **Pipeline NLP** (`02_nlp_pipeline.ipynb`)
   - Tokenisation avec spaCy
   - POS tagging (Part-of-Speech)
   - Named Entity Recognition (NER)
   - Extraction de dépendances syntaxiques

3. **Extraction d'événements** (`03_events_extraction.ipynb`)
   - Détection de sorts magiques
   - Identification de dialogues
   - Extraction de batailles et duels
   - Reconnaissance d'événements scolaires

4. **Agrégation et visualisation** (`04_aggregation_viz.ipynb`)
   - Statistiques par livre
   - Évolution temporelle des événements
   - Graphiques interactifs
   - Heatmaps et comparaisons

5. **Génération de rapport** (`05_methods_report.ipynb`)
   - Rapport méthodologique HTML automatique
   - Export JSON/CSV des résultats
   - Résumé exécutif

### Structure de données

```
Data Flow:
Textes bruts → sentences.parquet → nlp_processed.parquet → events.parquet → Agrégations finales
                                  ↓
                        entities_index.parquet
```

### Fichiers de sortie

- `agg_by_book.csv` / `.json` : statistiques agrégées par livre
- `methodology_report.html` : rapport complet avec méthodologie
- `summary.md` : résumé textuel des résultats
- Graphiques PNG : évolutions, comparaisons, heatmaps

---

## ⚙️ Technologies utilisées

### Core
- **Python 3.10+**
- **Jupyter Notebooks** : reproductibilité et documentation interactive

### NLP & ML
- **spaCy 3.7+** : pipeline NLP (tokenisation, POS, NER)
- **spaCy Transformers** : modèles avancés (optionnel)
- **en_core_web_sm/lg** : modèles pré-entraînés anglais

### Data Processing
- **Pandas** : manipulation de données
- **Polars** : alternative haute performance (optionnel)
- **PyArrow** : format Parquet pour stockage efficace

### Visualisation
- **Matplotlib** : graphiques statiques
- **Seaborn** : visualisations statistiques
- **Plotly** : graphiques interactifs (optionnel)

### Automation
- **Makefile** : commandes automatisées
- **pytest** : tests unitaires (optionnel)

---

## 🚀 Lancement rapide

### Installation

```bash
# Cloner et naviguer vers le projet
cd projects/22-proces-jk-rowling/hp_nlp

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate   # Windows

# Installer les dépendances
pip install -r requirements.txt

# Télécharger le modèle spaCy
python -m spacy download en_core_web_sm
```

### Exécution via Makefile

```bash
# Option 1 : Exécuter toute la pipeline
make all

# Option 2 : Exécuter étape par étape
make ingest        # Étape 1 : Ingestion
make nlp           # Étape 2 : Pipeline NLP
make events        # Étape 3 : Extraction événements
make viz           # Étape 4 : Visualisations
make report        # Étape 5 : Génération rapport

# Nettoyage
make clean         # Supprime les données intermédiaires
make clean-all     # Reset complet
```

### Exécution manuelle (Jupyter)

```bash
# Lancer Jupyter
jupyter notebook

# Exécuter les notebooks dans l'ordre :
# 1. notebooks/01_ingest_clean.ipynb
# 2. notebooks/02_nlp_pipeline.ipynb
# 3. notebooks/03_events_extraction.ipynb
# 4. notebooks/04_aggregation_viz.ipynb
# 5. notebooks/05_methods_report.ipynb
```

---

## 🧪 Tests

### Test smoke (vérification basique)

```bash
bash tests/test_smoke.sh
```

Vérifie :
- ✅ Structure des dossiers
- ✅ Présence des notebooks
- ✅ Installation des dépendances
- ✅ Accessibilité des modèles spaCy

### Test d'intégration

```bash
bash tests/test_integration.sh
```

Vérifie :
- ✅ Exécution complète de la pipeline
- ✅ Génération des fichiers de sortie
- ✅ Validité des formats (Parquet, JSON, CSV)
- ✅ Cohérence des statistiques

### Tests unitaires (optionnel)

```bash
pytest tests/
```

---

## 📊 Résultats attendus

### Métriques extraites par livre

- **Nombre total de phrases**
- **Événements magiques** : sorts lancés, potions, créatures
- **Dialogues** : nombre et longueur moyenne
- **Entités nommées** : personnages, lieux, organisations
- **Batailles et duels** : fréquence et intensité
- **Événements scolaires** : cours, examens, fêtes

### Visualisations générées

1. **Évolution des événements** : courbe temporelle sur les 7 livres
2. **Statistiques normalisées** : comparaison équitable (par 1000 phrases)
3. **Heatmap des événements** : concentration par livre et type
4. **Comparaison des dialogues** : distribution et évolution

### Rapport méthodologique

Document HTML complet incluant :
- Méthodologie détaillée
- Résultats chiffrés
- Graphiques interactifs
- Limites et perspectives

---

## 💾 PRA / Backup

### Stratégie de sauvegarde

1. **Données sources** : textes bruts versionnés (Git LFS recommandé)
2. **Données intermédiaires** : Parquet files (`.gitignore` mais sauvegarde locale)
3. **Résultats finaux** : commits réguliers dans `outputs/`
4. **Notebooks** : versionnés avec Git

### Reprise après incident

```bash
# Restaurer l'environnement
make setup

# Relancer depuis une étape spécifique
make nlp     # Si ingestion OK mais NLP échoué
make viz     # Si événements OK mais visualisations manquantes

# Vérifier l'intégrité des données
make validate
```

### Checkpoints

La pipeline crée des checkpoints automatiques :
- Après chaque notebook → fichier `.parquet` correspondant
- Métadonnées dans `data/book_metadata.json`
- Logs d'exécution dans `notebooks/.logs/` (optionnel)

---

## 🧠 Notes & Retours

### ✅ Points forts

1. **Approche neuronal** : remplacement réussi des regex par spaCy NER
2. **Reproductibilité** : notebooks Jupyter + Makefile = pipeline claire
3. **Performance** : format Parquet pour données volumineuses
4. **Visualisations** : insights narratifs exploitables
5. **Documentation** : méthodologie transparente et traçable

### ⚠️ Limites identifiées

1. **Modèle générique** : spaCy `en_core_web_sm` pas spécialisé HP
   - **Amélioration possible** : fine-tuning sur corpus Harry Potter
2. **Contexte narratif** : détection d'événements simple
   - **Amélioration possible** : analyse de coréférence, graphes de connaissances
3. **Temps d'exécution** : ~15-30 min pour les 7 livres
   - **Amélioration possible** : parallélisation, cache intelligent

### 🚀 Perspectives d'amélioration

#### Court terme
- [ ] Ajouter détection de sentiments (sentiment analysis)
- [ ] Créer timeline interactive des événements
- [ ] Export en base de données (SQLite/PostgreSQL)

#### Moyen terme
- [ ] Fine-tuner un modèle spaCy sur corpus HP
- [ ] Ajouter analyse de network des personnages
- [ ] Créer API REST pour requêtes en temps réel

#### Long terme
- [ ] Migration vers Transformers (BERT, RoBERTa)
- [ ] Génération de résumés automatiques par chapitre
- [ ] Chatbot Q&A sur l'univers Harry Potter

### 📝 Retours pédagogiques

**Ce qui a bien fonctionné :**
- Structure modulaire en notebooks facilitant le debug
- Documentation inline dans les notebooks
- Approche itérative : test rapide → optimisation

**Ce qui pourrait être amélioré :**
- Plus de tests unitaires sur les fonctions d'extraction
- Dashboard interactif (Streamlit/Dash)
- Containerisation Docker pour isoler l'environnement

---

## 📚 Références

### Documentation technique
- [spaCy Documentation](https://spacy.io/api/doc)
- [Named Entity Recognition Guide](https://spacy.io/usage/linguistic-features#named-entities)
- [Parquet Format Specification](https://parquet.apache.org/docs/)

### Ressources académiques
- Manning, C. D., & Schütze, H. (1999). *Foundations of Statistical Natural Language Processing*
- Jurafsky, D., & Martin, J. H. (2023). *Speech and Language Processing* (3rd ed.)

### Projets similaires
- [Harry Potter Corpus Analysis](https://github.com/efekarakus/potter-corpus)
- [Narrative Analysis with NLP](https://github.com/dhalperi/narrative-nlp)

---

## 🎓 Critères d'acceptation

| Critère | Statut | Notes |
|---------|--------|-------|
| Pipeline complète exécutable | ✅ | Makefile + notebooks |
| Extraction d'au moins 4 types d'événements | ✅ | Sorts, dialogues, batailles, scolaire |
| Visualisations claires et exploitables | ✅ | 4+ graphiques générés |
| Rapport méthodologique automatique | ✅ | HTML + summary.md |
| Documentation complète | ✅ | README + ce rendu |
| Tests automatisés | ✅ | Smoke + integration |
| Code reproductible | ✅ | requirements.txt + setup |

---

## 📞 Contact & Support

**Projet :** LE PROCÈS DE J.K. ROWLING  
**Défi :** #22 - Workshop Poudlard EPSI  
**Date :** Octobre 2025  

Pour toute question :
1. Consulter `README.md` et `QUICKSTART.md`
2. Vérifier `METHODOLOGY.md` pour détails techniques
3. Consulter `docs/prompts_used.md` pour historique IA

---

> 🧙‍♂️ *"Les données ne mentent jamais, mais il faut savoir les interroger avec les bons sorts."*  
> — Hermione Granger, experte en NLP magique
