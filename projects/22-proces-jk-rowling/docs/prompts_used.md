# 💬 Prompts IA utilisés – Défi 22: Le Procès de J.K. Rowling

Ce document liste tous les prompts utilisés avec des outils d'IA pour générer le code, la documentation et les analyses de ce projet.

---

## 🔹 Prompt 1 – Architecture globale du projet

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Définir l'architecture du projet d'analyse textuelle

```
Crée l'architecture complète d'un projet d'analyse textuelle pour extraire des 
statistiques des livres Harry Potter. Le projet doit inclure:

1. Un pipeline d'extraction de texte depuis PDFs
2. Des analyses statistiques spécifiques:
   - Occurrences de la cicatrice de Harry
   - Hermione disant "Mais"
   - Interventions de Dumbledore
   - Prises de parole (Harry, Hermione, Ron)
   - Comportements de Rogue
   - Actes répréhensibles
3. Des visualisations avec matplotlib/seaborn
4. Export des données en CSV et JSON
5. Statistiques normalisées par page

Structure le projet selon les standards définis dans agents/AGENTS.md avec:
- README.md
- requirements.txt
- Dockerfile
- docker-compose.snippet.yml
- docs/rendu.md
- docs/prompts_used.md
- tests/test_smoke.sh
- src/analyze_corpus.py

Le projet doit être dans projects/22-proces-jk-rowling/
```

---

## 🔹 Prompt 2 – Script d'analyse Python

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Créer le script principal d'analyse

```
Développe un script Python complet (analyze_corpus.py) pour analyser les livres 
Harry Potter. Le script doit:

1. Extraire le texte de PDFs avec PyPDF2
2. Implémenter des fonctions d'analyse pour:
   - count_scar_touches(): Compter quand Harry touche sa cicatrice (patterns: 
     cicatrice + douleur/brûle, porta main cicatrice, etc.)
   - count_hermione_mais(): Compter quand Hermione dit "Mais" dans ses dialogues
   - count_dumbledore_interventions(): Interventions arbitraires de Dumbledore
   - count_character_speeches(): Prises de parole de Harry, Hermione, Ron
   - count_snape_mysterious(): Moments où Rogue est mystérieux/sombre
   - count_questionable_acts(): Actes moralement/légalement répréhensibles

3. Utiliser des expressions régulières pour détecter les patterns
4. Créer un DataFrame pandas avec toutes les statistiques
5. Calculer des statistiques normalisées (par 100 pages)
6. Exporter en CSV et JSON
7. Afficher un résumé dans la console

Inclure la gestion d'erreurs et des messages de progression clairs.
```

---

## 🔹 Prompt 3 – Visualisations de données

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Créer les visualisations des statistiques

```
Ajoute une fonction create_visualizations() qui génère 5 graphiques professionnels:

1. statistics_trends.png: 4 subplots montrant l'évolution de:
   - Cicatrice de Harry (ligne rouge)
   - Hermione dit "Mais" (ligne violette)
   - Interventions Dumbledore (ligne bleue)
   - Rogue mystérieux (ligne noire)

2. speech_comparison.png: Graphique à barres groupées comparant les prises de 
   parole de Harry, Hermione et Ron par livre

3. questionable_acts.png: Bar chart des actes répréhensibles par livre avec 
   annotations et dégradé de couleur

4. normalized_statistics.png: 4 subplots des statistiques normalisées (par 100 pages)

5. heatmap_all_stats.png: Heatmap complète de toutes les statistiques avec 
   colormap YlOrRd

Tous les graphiques doivent:
- Avoir des titres clairs avec emojis
- Être exportés en haute résolution (300 DPI)
- Utiliser seaborn pour le style
- Avoir une grille légère pour faciliter la lecture
```

---

## 🔹 Prompt 4 – Dockerfile et Docker Compose

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Créer la configuration Docker

```
Crée un Dockerfile pour le projet d'analyse textuelle:
- Image de base: python:3.11-slim
- Installer les dépendances système nécessaires
- Copier requirements.txt et installer les dépendances Python
- Copier le code source
- Monter les livres depuis ../../context/books
- Point d'entrée: python analyze_corpus.py

Crée aussi un docker-compose.snippet.yml qui:
- Build le Dockerfile avec le bon context
- Monte les volumes pour books (ro), output, et data
- Se connecte au réseau poudlard-network
- Nom du conteneur: proces-jk-rowling
```

---

## 🔹 Prompt 5 – README.md

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Créer le README principal

```
Crée un README.md professionnel et complet pour le projet d'analyse statistique 
Harry Potter.

Sections:
1. Titre avec emoji et citation
2. Objectif clair
3. Liste des 8 statistiques analysées avec emojis
4. Architecture du projet (arborescence)
5. Lancement rapide (Docker et local)
6. Résultats attendus
7. Liste des visualisations générées
8. Section Tests
9. Méthodologie détaillée
10. Technologies utilisées
11. Exemples de résultats
12. Interprétation des tendances
13. Documentation complète (lien vers rendu.md)
14. Crédits et licence

Utilise des emojis, du formatting markdown, et des exemples de code.
```

---

## 🔹 Prompt 6 – Script de test

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Créer le script de smoke test

```
Crée un script bash test_smoke.sh qui vérifie:
1. Structure du projet (src/, docs/, tests/)
2. Présence des livres Harry Potter dans context/books/
3. Dépendances Python installées (si local)
4. Présence et syntaxe du script analyze_corpus.py
5. Fichiers Docker (Dockerfile, docker-compose.snippet.yml)
6. Documentation (README.md, docs/rendu.md, docs/prompts_used.md)
7. Création des répertoires output/ et data/
8. Docker installé (optionnel)

Utilise des couleurs (GREEN, RED, YELLOW) et des emojis pour les messages.
Affiche des instructions finales sur comment lancer l'analyse.
Le script doit être robuste avec set -e et gérer les erreurs.
```

---

## 🔹 Prompt 7 – Documentation rendu.md

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Créer le rapport méthodologique complet

```
Rédige un rapport méthodologique complet (docs/rendu.md) pour le défi 22 suivant 
le format standard de agents/AGENTS.md.

Le document doit inclure:
1. Objectif du projet
2. Architecture complète avec diagramme textuel
3. Technologies utilisées et justification
4. Méthodologie détaillée:
   - Extraction de texte PDF
   - Patterns d'analyse textuelle
   - Normalisation des données
   - Création des visualisations
5. Lancement rapide avec exemples de commandes
6. Tests et validation
7. Résultats et interprétations:
   - Statistiques brutes
   - Tendances observées
   - Insights intéressants
8. Limites et améliorations possibles
9. Annexes avec exemples de patterns regex

Utilise un ton professionnel mais accessible, avec des emojis pour structurer.
```

---

## 🔹 Prompt 8 – .gitignore pour le projet

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Créer le .gitignore adapté

```
Crée un .gitignore pour le projet d'analyse textuelle Python qui exclut:
- __pycache__/ et *.pyc
- .pytest_cache/
- *.egg-info/
- venv/ et env/
- .env
- Les fichiers de sortie temporaires mais garde la structure des dossiers
- .DS_Store
- *.log

Garde les répertoires output/ et data/ avec .gitkeep si vides.
```

---

## 📊 Résumé de l'usage IA

- **Nombre de prompts**: 8
- **Outils utilisés**: GitHub Copilot
- **Types de contenu généré**:
  - Code Python (100%)
  - Configuration Docker (100%)
  - Documentation (100%)
  - Scripts de test (100%)

Tous les prompts ont été utilisés de manière itérative avec validation et ajustement manuel.

---

> 💡 **Note**: Ces prompts servent de base et ont été affinés durant le développement 
> pour améliorer la précision des analyses et la qualité des visualisations.
