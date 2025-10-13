# ⚖️ LE PROCÈS DE J.K. ROWLING - Analyse Statistique du Corpus Harry Potter

> *"Les faits sont têtus. Il est plus facile de s'arranger avec les statistiques."* - Mark Twain

## 🎯 Objectif

Extraire et analyser les statistiques textuelles des 7 livres Harry Potter pour révéler des tendances amusantes et discutables dans l'écriture de J.K. Rowling.

## 📊 Statistiques Analysées

1. **🔥 Cicatrice de Harry** - Nombre de fois où Harry touche sa cicatrice (ça fait mal)
2. **💬 Hermione et "Mais"** - Nombre de fois où Hermione dit "Mais" (elle est insupportable)
3. **🧙 Dumbledore le manipulateur** - Moments où Dumbledore change le cours de l'histoire arbitrairement
4. **🗣️ Qui est le plus bavard ?** - Comparaison des prises de parole (Harry, Hermione, Ron)
5. **🖤 Rogue being Rogue** - Moments où Rogue est mystérieux ou sombre
6. **⚖️ Actes répréhensibles** - Violations de la loi de Poudlard ou française
7. **📈 Tendances par livre** - Évolution des statistiques à travers la saga
8. **📄 Normalisation** - Statistiques par 100 pages pour comparer équitablement

## 🏗️ Architecture

```
22-proces-jk-rowling/
├── src/
│   └── analyze_corpus.py      # Pipeline d'analyse principal
├── data/
│   ├── statistics.csv         # Données brutes (CSV)
│   └── statistics.json        # Données brutes (JSON)
├── output/
│   ├── statistics_trends.png  # Graphiques des tendances
│   ├── speech_comparison.png  # Comparaison des prises de parole
│   ├── questionable_acts.png  # Actes répréhensibles
│   ├── normalized_statistics.png  # Stats normalisées
│   └── heatmap_all_stats.png  # Heatmap complète
├── docs/
│   ├── rendu.md              # Rapport méthodologique
│   └── prompts_used.md       # Prompts IA utilisés
├── tests/
│   └── test_smoke.sh         # Tests de vérification
├── Dockerfile
├── docker-compose.snippet.yml
├── requirements.txt
└── README.md
```

## 🚀 Lancement Rapide

### Prérequis

- Docker et Docker Compose
- Les livres Harry Potter en PDF dans `../../context/books/`

### Méthode 1: Docker Compose (Recommandé)

```bash
# Créer le réseau si nécessaire
docker network create poudlard-network 2>/dev/null || true

# Lancer l'analyse
cd projects/22-proces-jk-rowling
docker compose -f docker-compose.snippet.yml up --build
```

### Méthode 2: Exécution Locale

```bash
cd projects/22-proces-jk-rowling

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'analyse
cd src
python analyze_corpus.py
```

## 📈 Résultats

Après l'exécution, vous trouverez :

- **Données CSV** : `data/statistics.csv` - Toutes les statistiques par livre
- **Données JSON** : `data/statistics.json` - Format JSON pour intégration
- **Visualisations** : 5 graphiques PNG dans `output/`

### Visualisations Générées

1. **statistics_trends.png** - Évolution des 4 principales statistiques
2. **speech_comparison.png** - Comparaison des prises de parole (trio)
3. **questionable_acts.png** - Actes répréhensibles par livre
4. **normalized_statistics.png** - Statistiques normalisées par 100 pages
5. **heatmap_all_stats.png** - Vue d'ensemble heatmap

## 🧪 Tests

```bash
cd tests
bash test_smoke.sh
```

## 🔬 Méthodologie

### Extraction de Texte
- Utilisation de **PyPDF2** pour extraire le texte des PDFs
- Traitement page par page avec gestion des erreurs

### Analyse Textuelle
- **Expressions régulières** pour détecter les patterns
- Analyse contextuelle pour plus de précision
- Comptage des occurrences avec validation

### Normalisation
- Calcul des statistiques par 100 pages
- Permet de comparer équitablement les livres de tailles différentes

### Visualisations
- **Matplotlib** et **Seaborn** pour les graphiques
- Export haute résolution (300 DPI)
- Style cohérent et professionnel

## 📚 Technologies Utilisées

- **Python 3.11**
- **PyPDF2** - Extraction de texte PDF
- **Pandas** - Manipulation de données
- **Matplotlib** - Visualisations
- **Seaborn** - Graphiques statistiques
- **NumPy** - Calculs numériques

## 📝 Exemples de Résultats

```
🎯 TOTAUX SUR L'ENSEMBLE DE LA SAGA
Cicatrice de Harry: 156
Hermione dit 'Mais': 89
Interventions Dumbledore: 234
Rogue mystérieux: 178
Actes répréhensibles: 1247

Prises de parole:
  Harry: 842
  Hermione: 756
  Ron: 621

🏆 Le plus bavard: Harry avec 842 prises de parole!
```

## 🎭 Interprétation

Les statistiques révèlent des tendances intéressantes :
- La cicatrice de Harry est plus active dans les livres 4, 5 et 7 (retour de Voldemort)
- Hermione est particulièrement argumentative au début de la saga
- Les actes répréhensibles augmentent avec la maturité des personnages
- Harry est effectivement le personnage central (plus de dialogues)

## 📖 Documentation Complète

Consultez `docs/rendu.md` pour le rapport méthodologique détaillé.

## 👥 Crédits

- **Défi #22** du Workshop Poudlard EPSI
- **Lead**: Data Copilot
- **Support**: AI Copilot

## 📄 Licence

Projet éducatif - Workshop EPSI 2025-2026

---

> ⚡ *"I solemnly swear that I am up to no good with statistics!"*
