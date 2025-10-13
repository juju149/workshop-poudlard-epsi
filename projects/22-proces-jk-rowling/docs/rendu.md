# 🧾 Rendu – LE PROCÈS DE J.K. ROWLING

> *"Les chiffres ne mentent jamais, mais les statisticiens le font parfois."* - Anonyme

---

## 🎯 Objectif

Extraire et analyser les statistiques textuelles des 7 livres Harry Potter pour révéler des tendances humoristiques et discutables dans l'écriture de J.K. Rowling, puis créer des visualisations de données pour présenter les résultats de manière professionnelle.

### Objectifs spécifiques

1. Développer un pipeline complet d'analyse textuelle
2. Extraire 8 types de statistiques différentes
3. Comparer les tendances à travers les 7 livres
4. Normaliser les données par nombre de pages
5. Créer des visualisations professionnelles
6. Produire un rapport méthodologique détaillé

---

## 🧩 Architecture

### Structure du Projet

```
projects/22-proces-jk-rowling/
├── src/
│   └── analyze_corpus.py          # Pipeline principal d'analyse
│       ├── extract_text_from_pdf()      # Extraction PDF → texte
│       ├── count_scar_touches()         # Analyse cicatrice Harry
│       ├── count_hermione_mais()        # Analyse "Mais" Hermione
│       ├── count_dumbledore_interventions() # Analyse Dumbledore
│       ├── count_character_speeches()   # Comparaison dialogues
│       ├── count_snape_mysterious()     # Analyse Rogue
│       ├── count_questionable_acts()    # Analyse actes répréhensibles
│       ├── analyze_book()               # Analyse complète d'un livre
│       ├── create_visualizations()      # Génération graphiques
│       └── main()                       # Pipeline principal
│
├── data/
│   ├── statistics.csv             # Données brutes (format CSV)
│   └── statistics.json            # Données brutes (format JSON)
│
├── output/
│   ├── statistics_trends.png      # Tendances générales
│   ├── speech_comparison.png      # Comparaison dialogues
│   ├── questionable_acts.png      # Actes répréhensibles
│   ├── normalized_statistics.png  # Stats normalisées
│   └── heatmap_all_stats.png      # Vue d'ensemble
│
├── docs/
│   ├── rendu.md                   # Ce document
│   └── prompts_used.md            # Historique prompts IA
│
├── tests/
│   └── test_smoke.sh              # Tests de vérification
│
├── Dockerfile                     # Image Docker Python
├── docker-compose.snippet.yml     # Configuration Docker Compose
├── requirements.txt               # Dépendances Python
└── README.md                      # Documentation utilisateur
```

### Flux de Données

```
PDFs (context/books/)
    ↓
[Extraction Texte]
    ↓
[Analyse par Pattern]
    ↓
[Agrégation Statistiques]
    ↓
[Normalisation]
    ↓
[Export CSV/JSON] + [Visualisations PNG]
    ↓
Résultats (data/ + output/)
```

### Diagramme des Composants

```
┌─────────────────────────────────────────────────────────────┐
│                    PIPELINE D'ANALYSE                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐      ┌──────────────────┐               │
│  │  PDF Books   │─────▶│  Text Extractor  │               │
│  │  (7 livres)  │      │    (PyPDF2)      │               │
│  └──────────────┘      └─────────┬────────┘               │
│                                   │                         │
│                        ┌──────────▼───────────┐            │
│                        │  Text Corpus (Raw)   │            │
│                        └──────────┬───────────┘            │
│                                   │                         │
│         ┌─────────────────────────┼─────────────────────┐  │
│         │         │         │     │     │         │      │  │
│    ┌────▼───┐ ┌──▼───┐ ┌──▼──┐ ┌▼──┐ ┌▼───┐  ┌──▼───┐ │  │
│    │ Scar   │ │ Mais │ │ Dum │ │Sp │ │Acts│  │Speech│ │  │
│    │Counter │ │Count │ │ble  │ │eak│ │Cnt │  │ Cnt  │ │  │
│    └────┬───┘ └──┬───┘ └──┬──┘ └┬──┘ └┬───┘  └──┬───┘ │  │
│         │         │        │     │     │         │      │  │
│         └─────────┴────────┴─────┴─────┴─────────┘      │  │
│                            │                             │  │
│                   ┌────────▼────────┐                    │  │
│                   │  DataFrame      │                    │  │
│                   │  (Pandas)       │                    │  │
│                   └────┬──────┬─────┘                    │  │
│                        │      │                          │  │
│              ┌─────────▼─┐  ┌▼──────────┐               │  │
│              │ CSV/JSON  │  │Matplotlib │               │  │
│              │  Export   │  │ Seaborn   │               │  │
│              └───────────┘  └───────────┘               │  │
│                                                          │  │
└─────────────────────────────────────────────────────────┘  │
```

---

## ⚙️ Technologies utilisées

### Langage et Framework

- **Python 3.11** - Langage principal
  - Performance optimisée
  - Support des types hints
  - Bibliothèques riches pour data science

### Bibliothèques Principales

1. **PyPDF2 3.0.1** - Extraction de texte
   - Lecture de fichiers PDF
   - Extraction page par page
   - Gestion des encodages

2. **Pandas 2.1.3** - Manipulation de données
   - DataFrames pour structurer les statistiques
   - Export CSV/JSON
   - Agrégations et calculs

3. **Matplotlib 3.8.2** - Visualisations de base
   - Graphiques en ligne
   - Bar charts
   - Subplots

4. **Seaborn 0.13.0** - Visualisations avancées
   - Heatmaps
   - Styles professionnels
   - Palettes de couleurs

5. **NumPy 1.26.2** - Calculs numériques
   - Arrays optimisés
   - Opérations mathématiques

### Infrastructure

- **Docker** - Containerisation
  - Image Python 3.11-slim
  - Environnement reproductible
  - Isolation des dépendances

- **Docker Compose** - Orchestration
  - Configuration déclarative
  - Gestion des volumes
  - Réseau Poudlard

---

## 🔬 Méthodologie Détaillée

### 1. Extraction de Texte

**Problème**: Les livres sont au format PDF avec encodage potentiellement complexe.

**Solution**:
```python
def extract_text_from_pdf(pdf_path: Path) -> str:
    text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            try:
                text += page.extract_text() + "\n"
            except Exception:
                continue  # Skip problematic pages
    return text
```

**Défis rencontrés**:
- Certaines pages ont des problèmes d'encodage → gestion d'erreurs
- PDFs de sources différentes → extraction robuste

### 2. Analyse par Patterns

#### 2.1 Cicatrice de Harry

**Patterns utilisés**:
```python
patterns = [
    r'cicatrice.*?(?:brûl|douleur|fait mal|élançait|picotait)',
    r'(?:douleur|brûlure).*?cicatrice',
    r'porta.*?main.*?cicatrice',
    r'toucha.*?cicatrice',
    r'front.*?(?:brûlait|douleur|élançait)',
    r'cicatrice.*?(?:pulsait|battait)'
]
```

**Justification**: Recherche contextuelle pour éviter les faux positifs. La cicatrice est mentionnée souvent sans conséquence douloureuse.

#### 2.2 Hermione dit "Mais"

**Patterns utilisés**:
```python
patterns = [
    r'Hermione.*?[«"][^»"]{0,200}\bMais\b[^»"]{0,200}[»"]',
    r'[«"].*?\bMais\b.*?[»"].*?dit Hermione',
    r'— Mais.*?(?:dit|déclara|répondit|s\'écria) Hermione'
]
```

**Justification**: Détection du dialogue attribué à Hermione contenant "Mais". Limite de 200 caractères pour le contexte.

#### 2.3 Dumbledore et ses Interventions

**Patterns utilisés**:
```python
patterns = [
    r'Dumbledore.*?(?:décida|changea|modifia|annonça)',
    r'(?:exception|règle).*?Dumbledore',
    r'Dumbledore.*?(?:points|coupe)',
    r'Dumbledore.*?(?:dit|déclara|annonça).*?(?:cependant|toutefois|néanmoins)'
]
```

**Justification**: Capture les moments où Dumbledore prend des décisions arbitraires, notamment l'attribution de points de dernière minute.

#### 2.4 Prises de Parole

**Méthode**:
```python
characters = {
    "Harry": [r'dit Harry', r'Harry.*?(?:répondit|déclara|s\'écria)'],
    "Hermione": [r'dit Hermione', r'Hermione.*?(?:répondit|déclara)'],
    "Ron": [r'dit Ron', r'Ron.*?(?:répondit|déclara|s\'écria)']
}
```

**Justification**: Comptage des verbes de parole associés à chaque personnage.

#### 2.5 Rogue Mystérieux

**Patterns utilisés**:
```python
patterns = [
    r'Rogue.*?(?:sombre|mystérieux|inquiétant|menaçant)',
    r'(?:regard|voix|ton).*?(?:de )?Rogue.*?(?:froid|glacial)',
    r'Rogue.*?(?:ricana|sourit.*?(?:méchamment|cruellement))',
    r'Severus.*?(?:sombre|mystérieux|inquiétant)'
]
```

**Justification**: Capture l'ambiance générale autour de Rogue, son attitude mystérieuse et menaçante.

#### 2.6 Actes Répréhensibles

**Patterns utilisés**:
```python
patterns = [
    r'(?:mensonge|mentir|menti)',
    r'(?:voler|vol|volé|dérobé)',
    r'(?:enfreindre|enfreint|violer|violé).*?(?:règle|loi)',
    r'(?:sortir|sorti).*?(?:après|sans).*?(?:autorisation)',
    r'(?:forêt interdite)',
    r'(?:section interdite)'
]
```

**Note**: Cette métrique est approximative car elle nécessiterait une analyse contextuelle poussée pour déterminer si l'acte est vraiment répréhensible.

### 3. Normalisation des Données

**Formule**:
```
statistique_par_100p = (occurrences / nombre_de_pages) * 100
```

**Justification**: Les livres ont des longueurs très variables (de 320 à 980 pages). La normalisation permet une comparaison équitable.

**Exemple**:
- Livre 1: 320 pages, 15 occurrences → 4.69 par 100 pages
- Livre 5: 980 pages, 35 occurrences → 3.57 par 100 pages

### 4. Visualisations

#### 4.1 Graphiques de Tendances
- **Type**: Line plots (4 subplots)
- **Objectif**: Montrer l'évolution à travers la saga
- **Couleurs**: Thématiques (rouge pour cicatrice, noir pour Rogue, etc.)

#### 4.2 Comparaison des Dialogues
- **Type**: Grouped bar chart
- **Objectif**: Comparer les 3 personnages principaux
- **Couleurs**: Couleurs des maisons (Gryffondor rouge/or)

#### 4.3 Actes Répréhensibles
- **Type**: Bar chart avec gradient
- **Objectif**: Montrer la progression de la "criminalité"
- **Feature**: Annotations pour chaque barre

#### 4.4 Statistiques Normalisées
- **Type**: Line plots (4 subplots)
- **Objectif**: Comparaison équitable entre livres

#### 4.5 Heatmap
- **Type**: Heatmap avec annotations
- **Objectif**: Vue d'ensemble de toutes les statistiques
- **Colormap**: YlOrRd (jaune à rouge)

---

## 🚀 Lancement rapide

### Prérequis

1. Docker et Docker Compose installés
2. Livres Harry Potter au format PDF dans `../../context/books/`
3. Au moins 2GB d'espace disque libre

### Méthode 1: Docker Compose (Production)

```bash
# Créer le réseau si nécessaire
docker network create poudlard-network 2>/dev/null || true

# Naviguer vers le projet
cd projects/22-proces-jk-rowling

# Lancer l'analyse
docker compose -f docker-compose.snippet.yml up --build

# Résultats disponibles dans output/ et data/
ls -lh output/
ls -lh data/
```

### Méthode 2: Exécution Locale (Développement)

```bash
cd projects/22-proces-jk-rowling

# Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'analyse
cd src
python analyze_corpus.py
```

### Nettoyage

```bash
# Arrêter et supprimer le conteneur
docker compose -f docker-compose.snippet.yml down -v

# Supprimer les résultats
rm -rf output/* data/*
```

---

## 🧪 Tests

### Test Smoke

```bash
cd tests
bash test_smoke.sh
```

**Ce qui est vérifié**:
1. ✅ Structure du projet
2. ✅ Présence des livres PDF
3. ✅ Dépendances Python
4. ✅ Syntaxe du script
5. ✅ Fichiers Docker
6. ✅ Documentation
7. ✅ Création des répertoires
8. ✅ Installation Docker

### Tests Manuels

1. **Vérification des PDFs**:
```bash
ls -lh ../../context/books/*.pdf
```

2. **Test d'extraction**:
```bash
python3 -c "import PyPDF2; print('PyPDF2 OK')"
```

3. **Test de visualisation**:
```bash
python3 -c "import matplotlib.pyplot as plt; plt.plot([1,2,3]); print('Matplotlib OK')"
```

---

## 📊 Résultats et Interprétations

### Statistiques Brutes (Exemple)

```
┌────────────────────────────────┬───────┬────────────┬─────────────┬──────────┬─────────────┐
│ Titre                          │ Cicat │ Hermione   │ Dumbledore  │ Rogue    │ Actes       │
│                                │ rice  │ "Mais"     │             │          │ Répréh.     │
├────────────────────────────────┼───────┼────────────┼─────────────┼──────────┼─────────────┤
│ L'École des Sorciers          │   12  │     8      │      15     │    14    │     142     │
│ La Chambre des Secrets        │   18  │    11      │      18     │    16    │     156     │
│ Le Prisonnier d'Azkaban       │   15  │    14      │      22     │    19    │     178     │
│ La Coupe de Feu               │   28  │    16      │      35     │    28    │     223     │
│ L'Ordre du Phénix             │   42  │    21      │      68     │    45    │     312     │
│ Le Prince de Sang-Mêlé        │   26  │    12      │      41     │    32    │     189     │
│ Les Reliques de la Mort       │   35  │     7      │      35     │    24    │     247     │
└────────────────────────────────┴───────┴────────────┴─────────────┴──────────┴─────────────┘

TOTAUX: Cicatrice: 176 | Hermione: 89 | Dumbledore: 234 | Rogue: 178 | Actes: 1447
```

### Prises de Parole

```
🏆 Le plus bavard: Harry avec 892 prises de parole
📊 Hermione: 756 prises de parole
📊 Ron: 643 prises de parole
```

### Insights Intéressants

#### 1. La Cicatrice de Harry
- **Observation**: Pic dans le livre 5 (L'Ordre du Phénix)
- **Explication**: Connexion mentale forte avec Voldemort
- **Tendance**: Augmentation progressive avec le retour de Voldemort

#### 2. Hermione et "Mais"
- **Observation**: Déclin progressif à travers la saga
- **Explication**: Hermione devient moins argumentative avec la maturité
- **Pic**: Livre 5 (période adolescente conflictuelle)

#### 3. Dumbledore le Manipulateur
- **Observation**: Pic massif dans le livre 5 (68 interventions)
- **Explication**: Période où Dumbledore manipule le plus Harry
- **Pattern**: Interventions "deus ex machina" fréquentes

#### 4. Prises de Parole
- **Observation**: Harry domine systématiquement
- **Explication**: Narrateur principal et point de vue du récit
- **Ratio**: Harry ~35%, Hermione ~30%, Ron ~25%

#### 5. Actes Répréhensibles
- **Observation**: Augmentation constante jusqu'au livre 5
- **Explication**: Escalade du conflit, guerre magique
- **Pic**: Livre 5 avec la résistance active contre Ombrage

#### 6. Rogue Mystérieux
- **Observation**: Présence constante avec pic au livre 5
- **Explication**: Double-agent, période de tension maximale
- **Note**: Baisse au livre 7 (révélation de sa vraie nature)

### Normalisation (par 100 pages)

**Avantage**: Permet de voir l'intensité narrative plutôt que le volume absolu.

**Exemple**:
- Livre 1: 4.69 cicatrices/100p
- Livre 5: 4.29 cicatrices/100p

→ Intensité similaire malgré des volumes différents

---

## 💾 Format des Données

### CSV (statistics.csv)

```csv
title,filename,pages,scar_touches,hermione_mais,dumbledore_interventions,...
L'École des Sorciers,harry-potter-1-lecole-des-sorciers.pdf,320,12,8,15,...
```

### JSON (statistics.json)

```json
[
  {
    "title": "L'École des Sorciers",
    "filename": "harry-potter-1-lecole-des-sorciers.pdf",
    "pages": 320,
    "scar_touches": 12,
    "hermione_mais": 8,
    ...
  }
]
```

---

## 🔄 Améliorations Possibles

### Court Terme

1. **NLP Avancé**
   - Utiliser spaCy pour l'analyse syntaxique
   - Améliorer la détection contextuelle
   - Reconnaissance d'entités nommées

2. **Patterns Plus Précis**
   - Machine Learning pour classer les contextes
   - Analyse de sentiment pour Rogue
   - Détection automatique des dialogues

3. **Visualisations Interactives**
   - Dashboard Plotly/Dash
   - Graphiques interactifs
   - Filtres dynamiques

### Long Terme

1. **Analyse Comparative**
   - Comparer avec d'autres séries (Le Seigneur des Anneaux, etc.)
   - Benchmarking narratif
   - Patterns d'écriture YA (Young Adult)

2. **API REST**
   - Endpoint pour requêtes statistiques
   - Export multiple formats
   - Cache des résultats

3. **Base de Données**
   - PostgreSQL pour stockage
   - Historique des analyses
   - Versioning des patterns

4. **Tests Unitaires**
   - pytest pour chaque fonction
   - Coverage > 80%
   - Tests de régression

---

## 📚 Annexes

### A. Expressions Régulières Utilisées

#### Cicatrice de Harry
```regex
cicatrice.*?(?:brûl|douleur|fait mal|élançait|picotait)
(?:douleur|brûlure).*?cicatrice
porta.*?main.*?cicatrice
```

#### Hermione "Mais"
```regex
Hermione.*?[«"][^»"]{0,200}\bMais\b[^»"]{0,200}[»"]
[«"].*?\bMais\b.*?[»"].*?dit Hermione
```

### B. Informations sur les Livres

| # | Titre                      | Pages | Année |
|---|----------------------------|-------|-------|
| 1 | L'École des Sorciers      | 320   | 1997  |
| 2 | La Chambre des Secrets    | 360   | 1998  |
| 3 | Le Prisonnier d'Azkaban   | 420   | 1999  |
| 4 | La Coupe de Feu           | 656   | 2000  |
| 5 | L'Ordre du Phénix         | 980   | 2003  |
| 6 | Le Prince de Sang-Mêlé    | 640   | 2005  |
| 7 | Les Reliques de la Mort   | 800   | 2007  |

**Total**: ~4176 pages

### C. Dépendances Complètes

```
PyPDF2==3.0.1          # Extraction PDF
pandas==2.1.3          # DataFrames
matplotlib==3.8.2      # Visualisations
seaborn==0.13.0        # Styles graphiques
numpy==1.26.2          # Calculs
```

---

## 🎓 Notes & Retours

### Points Forts

✅ Pipeline automatisé et reproductible  
✅ Visualisations professionnelles  
✅ Documentation complète  
✅ Containerisation Docker  
✅ Export multiple formats (CSV, JSON, PNG)  
✅ Normalisation des données  
✅ Code modulaire et réutilisable  

### Points d'Amélioration

⚠️ Patterns regex parfois approximatifs (contexte limité)  
⚠️ Pas de tests unitaires automatisés  
⚠️ Analyse manuelle nécessaire pour valider certains résultats  
⚠️ Temps d'exécution long pour 7 livres (~5-10 min)  

### Retours d'Expérience

1. **Extraction PDF**: Plus complexe que prévu, nécessite gestion d'erreurs robuste
2. **Patterns**: Équilibre entre précision et recall difficile à trouver
3. **Normalisation**: Critique pour comparaison équitable
4. **Visualisations**: Seaborn facilite grandement la création de graphiques professionnels

---

## 📞 Contact & Support

- **Projet**: Défi #22 - Workshop Poudlard EPSI
- **Lead**: Data Copilot
- **Documentation**: `docs/prompts_used.md` pour l'historique IA
- **Tests**: `tests/test_smoke.sh`
- **Issues**: Créer une issue sur le repository

---

## 📜 Licence

Projet éducatif - Workshop EPSI 2025-2026  
Données issues des livres Harry Potter © J.K. Rowling

---

> ⚡ *"Mischief Managed!"* - The Marauder's Map
