# 🚀 Guide de Démarrage Rapide - Pipeline NLP Harry Potter

Ce guide vous permet de démarrer en moins de 5 minutes.

## ⚡ Installation Ultra-Rapide

```bash
# 1. Naviguer vers le projet
cd projects/22-proces-jk-rowling/hp_nlp/

# 2. Installer tout (dépendances + modèle spaCy)
make setup

# 3. Exécuter le pipeline complet
make run

# 4. Voir les résultats
make open-report
```

C'est tout ! 🎉

## 📋 Prérequis

- Python 3.11+ (testé avec 3.12)
- 4GB RAM minimum
- 2GB espace disque
- Livres Harry Potter en PDF dans `../../context/books/`

## 🎯 Commandes Essentielles

### Installation

```bash
make setup          # Installation complète (recommandé)
make install-spacy  # Seulement le modèle spaCy
make test           # Vérifier l'installation
```

### Exécution

```bash
make run       # Pipeline complet (10-30 min)
make run-nb1   # Seulement ingestion
make run-nb2   # Seulement NLP
make run-nb3   # Seulement événements
make run-nb4   # Seulement visualisations
make run-nb5   # Seulement rapport
```

### Développement

```bash
make jupyter   # Ouvrir Jupyter Lab
make report    # Générer rapport uniquement
make stats     # Voir statistiques projet
```

### Nettoyage

```bash
make clean          # Tout nettoyer
make clean-outputs  # Seulement outputs
```

### Aide

```bash
make help      # Voir toutes les commandes
```

## 📁 Où Trouver les Résultats ?

Après exécution de `make run`, vous trouverez :

```
outputs/
├── methodology_report.html    # 📄 Rapport principal (OUVRIR CELUI-CI)
├── agg_by_book.csv           # 📊 Données agrégées
├── events_evolution.png      # 📈 Graphique évolution
├── normalized_stats.png      # 📊 Statistiques normalisées
├── heatmap_events.png        # 🔥 Heatmap
├── dialogues_comparison.png  # 💬 Comparaison dialogues
└── summary.md                # 📝 Résumé textuel
```

**👉 Ouvrez `outputs/methodology_report.html` dans votre navigateur !**

## 🐛 Problèmes Courants

### "Modèle spaCy non trouvé"

```bash
python -m spacy download fr_core_news_lg
# OU
python -m spacy download fr_core_news_sm
```

### "Livres PDF non trouvés"

Vérifier que les PDFs sont dans le bon répertoire :

```bash
ls ../../context/books/*.pdf
```

### "Mémoire insuffisante"

Réduire `SAMPLE_SIZE` dans les notebooks :

```python
# Dans notebook 02 ou 03
SAMPLE_SIZE = 1000  # Au lieu de 5000
```

### "Jupyter ne démarre pas"

```bash
pip install --upgrade jupyter notebook
```

## 📚 Documentation Complète

- **README.md** : Documentation complète du projet
- **METHODOLOGY.md** : Documentation technique exhaustive
- **ACCEPTANCE_CRITERIA.md** : Validation des critères

## ⏱️ Temps d'Exécution

Sur un laptop standard (4 cores, 8GB RAM) :

| Étape | Temps |
|-------|-------|
| Installation (make setup) | 3-5 min |
| Notebook 1 (ingestion) | 2-5 min |
| Notebook 2 (NLP) | 5-15 min |
| Notebook 3 (événements) | 3-10 min |
| Notebook 4 (visualisations) | 1-3 min |
| Notebook 5 (rapport) | 0.5-1 min |
| **TOTAL** | **11.5-34 min** |

## 🎓 Exemples de Résultats

### Statistiques Globales (exemple)

```
📊 Total phrases analysées : 52,847
📚 Total mots : 1,234,567
📄 Total pages : 3,576

🔥 Cicatrice de Harry : 156 occurrences
💬 Hermione dit "Mais" : 89 occurrences
🧙 Interventions Dumbledore : 234 occurrences
🖤 Rogue mystérieux : 178 occurrences
⚖️ Actes répréhensibles : 1,247 occurrences

🏆 Le plus bavard : Harry avec 842 dialogues!
```

### Visualisations

Le pipeline génère 4 graphiques professionnels :

1. **Évolution des événements** : Line charts montrant les tendances
2. **Stats normalisées** : Comparaison équitable par 100 pages
3. **Heatmap** : Vue d'ensemble couleur de tous les événements
4. **Dialogues** : Bar chart + pie chart des prises de parole

## 🔄 Workflow Typique

### Première utilisation

```bash
# 1. Installation
make setup

# 2. Test sur échantillon (modifier SAMPLE_SIZE=1000 dans notebooks)
make run-nb1
make run-nb2

# 3. Vérifier les sorties
ls data/
ls outputs/

# 4. Si OK, exécution complète
make run
```

### Développement itératif

```bash
# 1. Ouvrir Jupyter
make jupyter

# 2. Modifier les notebooks
# 3. Tester changements
# 4. Régénérer rapport

make report
make open-report
```

### Production

```bash
# Nettoyer puis exécuter
make clean
make run

# Vérifier résultats
make stats
make open-report
```

## 💡 Astuces

### Accélérer l'exécution

1. **Réduire SAMPLE_SIZE** dans notebooks 02 et 03
2. **Utiliser modèle sm** au lieu de lg : plus rapide mais moins précis
3. **Exécuter par étapes** : `make run-nb1`, vérifier, puis continuer

### Améliorer la qualité

1. **Corpus complet** : Retirer limite SAMPLE_SIZE
2. **Modèle lg** : Plus précis pour NER
3. **Validation manuelle** : Annoter échantillon pour calibrer

### Personnaliser

1. **Nouveaux événements** : Ajouter patterns dans notebook 03
2. **Nouveaux graphiques** : Modifier notebook 04
3. **Custom rapport** : Ajuster template dans notebook 05

## 📞 Support

### Ressources

- [spaCy Documentation](https://spacy.io/usage)
- [Pandas Guide](https://pandas.pydata.org/docs/)
- [Jupyter Documentation](https://jupyter-notebook.readthedocs.io/)

### Issues Communes

Consulter **METHODOLOGY.md** section "Limites et Considérations"

## ✨ Et Ensuite ?

Une fois le pipeline exécuté avec succès :

1. ✅ Ouvrir le rapport HTML
2. ✅ Explorer les visualisations
3. ✅ Analyser les tendances
4. ✅ Lire la méthodologie complète
5. ✅ Partager les résultats !

---

**Besoin d'aide détaillée ?** → Voir README.md et METHODOLOGY.md

**Prêt à démarrer ?** → `make setup` puis `make run` ! 🚀
