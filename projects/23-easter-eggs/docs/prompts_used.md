# 💬 Prompts IA utilisés – Défi 23: EASTER EGGS

Ce document archive tous les prompts utilisés pour générer et développer ce projet, conformément aux standards du Workshop Poudlard.

---

## 🔹 Prompt 1 – Conception du projet

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Définir l'approche éthique et sûre pour le défi "Easter Eggs"

```
Défi 23: Easter Eggs (Section Chaos)

Besoin de concevoir un projet qui explore les "limites" de l'IA de manière 
éthique et scientifique, sans aucun code malveillant.

Options considérées:
1. Faire planter une IA (preuve scientifique exigée)
2. Reverse engineering de jeux de données (rapport complet exigé)
3. Fork bomb expérimentale (ATTENTION : risques et interdictions)

Contraintes:
- Doit être ÉTHIQUE et LÉGAL
- Environnement isolé et sécurisé
- Documentation scientifique complète
- Pas de dommages aux systèmes

Proposition: Créer un framework de test qui soumet des paradoxes logiques 
à des modèles d'IA et analyse comment ils gèrent les contradictions.

Avantages:
✅ Éthique et légal (recherche en AI safety)
✅ Scientifiquement pertinent
✅ Pas de risques pour les systèmes
✅ Documentation riche possible
✅ Reproductible et testable
```

---

## 🔹 Prompt 2 – Structure du projet

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Créer la structure de fichiers conforme aux standards AGENTS.md

```
Créer la structure complète pour le projet 23-easter-eggs suivant 
le standard défini dans agents/AGENTS.md.

Structure requise:
projects/23-easter-eggs/
├── Dockerfile
├── docker-compose.snippet.yml
├── README.md
├── requirements.txt
├── docs/
│   ├── rendu.md
│   ├── prompts_used.md
│   ├── methodology.md
│   └── scientific_report.md
├── tests/
│   └── test_smoke.sh
├── src/
│   └── ai_stress_test.py
└── results/

Le README doit inclure:
- Description du projet
- Avertissements de sécurité
- Architecture
- Technologies
- Lancement rapide
- Tests
- Documentation des paradoxes
```

---

## 🔹 Prompt 3 – Script principal Python

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Développer le script de test de stress IA

```
Créer un script Python (ai_stress_test.py) qui:

1. Définit une classe AIStressTest avec:
   - Liste de paradoxes logiques classiques
   - Méthode pour simuler des réponses d'IA
   - Analyse de la cohérence des réponses
   - Génération de statistiques

2. Paradoxes à tester:
   - Paradoxe du Menteur
   - Paradoxe du Barbier
   - Instructions contradictoires
   - Boucles conceptuelles infinies
   - Auto-références paradoxales

3. Pour chaque test:
   - Soumettre le paradoxe
   - Récupérer la réponse (simulée pour démo)
   - Analyser: cohérence, reconnaissance du paradoxe, stratégie
   - Sauvegarder les résultats en JSON

4. Interface:
   - Utiliser Rich pour affichage élégant
   - Barre de progression pour les tests
   - Tableau de résumé final
   - Sauvegarde horodatée des résultats

5. Éthique:
   - Rate limiting entre les requêtes
   - Aucun code malveillant
   - Documentation claire du but éducatif
```

---

## 🔹 Prompt 4 – Dockerfile et Docker Compose

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Conteneuriser l'application

```
Créer un Dockerfile pour le projet easter-eggs:

Base: python:3.11-slim
Workdir: /app
Installer: requirements.txt (rich, requests)
Copier: src/
Créer: dossier results/
CMD: python src/ai_stress_test.py

Créer docker-compose.snippet.yml:
- Service: easter-eggs
- Build: context local
- Volumes: results/ pour persistance
- Env: PYTHONUNBUFFERED=1
- Interactive: stdin_open + tty pour voir la sortie formatée
```

---

## 🔹 Prompt 5 – Test Smoke

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Créer le script de test de validation

```
Créer tests/test_smoke.sh qui vérifie:

Structure:
✅ Dossiers src/, docs/, tests/ existent
✅ Fichiers essentiels présents:
   - README.md
   - Dockerfile
   - docker-compose.snippet.yml
   - requirements.txt
   - src/ai_stress_test.py
   - docs/rendu.md
   - docs/prompts_used.md

Contenu:
✅ README contient "EASTER EGGS"
✅ README contient avertissement sécurité
✅ Script Python contient classe AIStressTest
✅ requirements.txt contient "rich"
✅ Dockerfile utilise python:3.11

Validation:
✅ Syntaxe Python valide (py_compile)
✅ Docker Compose a service défini

Affichage:
- Couleurs (vert/rouge/jaune/bleu)
- Compteur de tests passés/échoués
- Résumé final
- Exit code approprié (0 = succès, 1 = échec)
```

---

## 🔹 Prompt 6 – README.md

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Créer le README principal du projet

```
Rédiger README.md pour le projet 23-easter-eggs:

Sections:
1. Titre et émojis 🎭
2. Objectif (test de stress IA éthique)
3. ⚠️ AVERTISSEMENT DE SÉCURITÉ en évidence
   - Ce qui est fait ✅
   - Ce qui n'est PAS fait ❌
4. Architecture (structure des fichiers)
5. Technologies utilisées
6. Lancement rapide (Docker et sans Docker)
7. Tests (comment lancer test_smoke.sh)
8. Exemples de paradoxes testés
9. Résultats attendus
10. Contexte pédagogique
11. Documentation (liens vers docs/)
12. Crédits et copilots
13. Planning (deadline 17/10/2025)
14. Références (AI safety, prompt engineering)

Ton: Professionnel mais accessible
Style: Markdown avec emojis
Format: Inspiré des autres projets du workshop
```

---

## 🔹 Prompt 7 – Document de rendu (docs/rendu.md)

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Créer le document de rendu final pour le jury

```
Créer docs/rendu.md suivant EXACTEMENT le template de agents/AGENTS.md:

Structure obligatoire:
1. 🎯 Objectif
2. 🧩 Architecture (avec diagramme ASCII)
3. ⚙️ Technologies utilisées
4. 🚀 Lancement rapide
5. 🧪 Tests
6. 💾 PRA / Backup

Sections additionnelles:
7. 📊 Méthodologie (types de paradoxes, critères d'analyse)
8. ⚠️ Considérations éthiques (détaillées)
9. 📈 Résultats obtenus (exemple de sortie)
10. 🎓 Apprentissages (techniques, méthodologiques, théoriques)
11. 🔮 Perspectives (améliorations, extensions)
12. 📦 Livrables (checklist complète)
13. 👥 Crédits (copilots, deadline)
14. 📚 Références (articles, recherche, doc technique)

Important:
- Diagramme ASCII de l'architecture
- Exemples concrets de sortie
- Justification scientifique
- Cadre légal et éthique explicite
- Liste exhaustive des livrables
```

---

## 🔹 Prompt 8 – Méthodologie scientifique

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Documenter l'approche scientifique

```
Créer docs/methodology.md détaillant:

1. Contexte théorique
   - Paradoxes logiques classiques
   - Recherche en AI safety
   - Tests adversariaux

2. Hypothèses de recherche
   - H1: Les IA modernes gèrent bien les paradoxes
   - H2: Stratégies identifiables (explication, refus, créativité)
   - H3: Certains paradoxes plus difficiles que d'autres

3. Protocole expérimental
   - Sélection des paradoxes (critères)
   - Méthode de test (séquence, timing)
   - Collecte des données (format JSON)

4. Métriques d'analyse
   - Cohérence (binaire)
   - Reconnaissance du paradoxe (présence mot-clé)
   - Stratégie utilisée (classification)
   - Qualité explication (longueur, profondeur)

5. Limitations
   - Modèle simulé (pas d'API réelle dans v1)
   - Petit échantillon (8 paradoxes)
   - Pas de comparaison multi-modèles

6. Reproductibilité
   - Docker pour environnement identique
   - JSON pour analyse ultérieure
   - Timestamps pour traçabilité
```

---

## 🔹 Prompt 9 – Rapport scientifique

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Créer le rapport de résultats

```
Créer docs/scientific_report.md format papier scientifique:

Structure:
1. Abstract/Résumé
2. Introduction
   - Contexte AI safety
   - Problématique
   - Objectifs
3. État de l'art
   - Paradoxes logiques
   - Tests adversariaux en IA
   - Travaux similaires
4. Méthodologie
   - Design expérimental
   - Protocole de test
   - Métriques
5. Résultats
   - Statistiques globales
   - Analyse par type de paradoxe
   - Patterns identifiés
6. Discussion
   - Interprétation des résultats
   - Comparaison aux hypothèses
   - Implications
7. Conclusion
   - Contributions
   - Limitations
   - Travaux futurs
8. Références

Inclure:
- Tableaux de résultats
- Graphiques conceptuels (ASCII)
- Exemples de réponses
- Citations académiques
```

---

## 🔹 Prompt 10 – Vérification finale

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: S'assurer de la conformité complète

```
Vérifier que le projet 23-easter-eggs est conforme à:

Checklist AGENTS.md:
✅ Documentation complète (docs/rendu.md)
✅ Prompts IA archivés (docs/prompts_used.md)
✅ Dockerfile fonctionnel
✅ Compose testé (docker-compose.snippet.yml)
✅ Tests automatisés (tests/test_smoke.sh)
✅ README détaillé

Checklist defis.md pour Défi 23:
✅ Concept défini et validé
✅ Environnement sécurisé préparé
✅ Expérimentation réalisée (ou simulée)
✅ Documentation des résultats
✅ Preuve/rapport scientifique

Standards de qualité:
✅ Code propre et commenté
✅ Documentation exhaustive
✅ Reproductibilité (Docker)
✅ Tests de validation
✅ Considérations éthiques
✅ Originalité et créativité
```

---

## 📊 Résumé des prompts

**Total de prompts utilisés**: 10

**Répartition par catégorie**:
- Conception: 2 prompts
- Code: 2 prompts
- Infrastructure: 1 prompt
- Tests: 1 prompt
- Documentation: 4 prompts

**Outils utilisés**:
- GitHub Copilot: 10/10 prompts
- Assistant de ligne de commande: 0 prompts
- Chat externe: 0 prompts

---

## 🎯 Méthodologie

### Approche itérative
1. ✅ Conception éthique du projet
2. ✅ Structure des fichiers
3. ✅ Code principal
4. ✅ Conteneurisation
5. ✅ Tests
6. ✅ Documentation utilisateur
7. ✅ Documentation scientifique
8. ✅ Vérification conformité

### Principes suivis
- **Éthique first**: Sécurité et légalité en priorité
- **Documentation complète**: Chaque aspect documenté
- **Reproductibilité**: Docker + scripts
- **Standards**: Respect strict de AGENTS.md
- **Qualité**: Code propre, tests, revue

---

## 💡 Leçons apprises

### Sur l'utilisation de l'IA
- Prompts structurés = résultats cohérents
- Itération rapide mais validation manuelle essentielle
- Documentation en parallèle du développement

### Sur le projet
- Importance du cadre éthique dès la conception
- Valeur de la méthodologie scientifique
- Nécessité de tests et reproductibilité

### Sur les standards
- AGENTS.md fournit un excellent framework
- Uniformité facilite maintenance et évaluation
- Checklist prévient les oublis

---

*Document généré conformément aux standards du Workshop Poudlard EPSI*
*Tous les prompts sont authentiques et tracés chronologiquement*
