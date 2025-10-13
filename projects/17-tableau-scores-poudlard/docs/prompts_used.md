# 💬 Prompts utilisés – Défi 17 : TABLEAU DES SCORES DE POUDLARD

Ce document archive tous les prompts IA utilisés pour générer le code, la documentation et les tests de ce projet.

---

## 🔹 Prompt 1 – Planification du projet

**Objectif** : Définir l'architecture globale et les technologies à utiliser

```
Créer un plan détaillé pour développer une application native (Kotlin pour Android) 
avec une API REST et base de données pour gérer les scores de 4 maisons de Poudlard.

Exigences:
- App native Kotlin/Swift (choisir Kotlin pour Android)
- API REST avec Node.js
- Base de données SQLite (pas de BaaS)
- Tests unitaires avec coverage > 80%
- Documentation technique

Proposer:
1. Architecture globale (3-tier: app, API, DB)
2. Stack technologique précis
3. Structure des dossiers selon AGENTS.md
4. Plan de tests
```

---

## 🔹 Prompt 2 – API REST Backend

**Objectif** : Créer le serveur Node.js avec Express et SQLite

```
Créer une API REST complète en Node.js/Express avec SQLite pour gérer les scores 
des 4 maisons de Poudlard (Gryffondor, Serpentard, Poufsouffle, Serdaigle).

Endpoints requis:
- GET /api/houses : liste des maisons avec scores
- GET /api/houses/:id : détail d'une maison
- PUT /api/houses/:id : définir les points (body: {points: number})
- POST /api/houses/:id/add : ajouter/retirer points (body: {points: number})
- POST /api/reset : réinitialiser tous les scores à 0
- GET /health : health check

Spécifications:
- Base SQLite avec table houses (id, name, points, created_at, updated_at)
- Seed data automatique avec les 4 maisons
- Validation des entrées
- Gestion d'erreurs (400, 404, 500)
- CORS activé
- Body parser JSON

Fichiers à créer:
- server.js : serveur Express
- database.js : classe Database pour SQLite
- package.json : dépendances
```

---

## 🔹 Prompt 3 – Tests unitaires Backend

**Objectif** : Tests Jest pour l'API avec couverture > 80%

```
Créer des tests unitaires complets avec Jest pour l'API des scores de Poudlard.

Tests à couvrir:
1. Health check endpoint
2. GET /api/houses (liste complète, vérification des 4 maisons)
3. GET /api/houses/:id (succès, 404, ID invalide)
4. PUT /api/houses/:id (succès, validation, erreurs)
5. POST /api/houses/:id/add (ajout positif, retrait négatif, validation)
6. POST /api/reset (vérification que tous les scores = 0)
7. Routes 404
8. Tests de la classe Database

Configuration:
- Utiliser supertest pour les tests d'API
- Base de données en mémoire (:memory:)
- Coverage avec Jest (--coverage)
- Objectif: > 80% coverage

Fichiers:
- server.test.js
- database.test.js
```

---

## 🔹 Prompt 4 – Application Android Kotlin

**Objectif** : Créer l'app native avec architecture MVVM

```
Créer une application Android native en Kotlin avec architecture MVVM pour gérer 
les scores des maisons de Poudlard.

Architecture MVVM:
- Models: House, HousesResponse, UpdatePointsRequest, Resource
- Repository: HouseRepository (appels API avec Retrofit)
- ViewModel: MainViewModel (LiveData, Coroutines)
- View: MainActivity (UI Material Design)

Fonctionnalités:
- Affichage des 4 maisons avec scores en cards colorées
- Bouton +/- par maison pour ajouter/retirer points
- Dialog pour saisir les points
- Bouton Rafraîchir
- Bouton Réinitialiser (avec confirmation)
- Loading states (ProgressBar)
- Gestion d'erreurs (Toast)

Technologies:
- Retrofit2 pour HTTP
- Kotlin Coroutines pour async
- LiveData pour observer les données
- Material Components pour UI
- OkHttp logging interceptor

URL API: http://10.0.2.2:3000 (pour émulateur)

Fichiers à créer:
- Models.kt
- ApiService.kt (interface Retrofit)
- RetrofitClient.kt
- Resource.kt (sealed class pour états)
- HouseRepository.kt
- MainViewModel.kt
- MainActivity.kt
- activity_main.xml (layout)
- dialog_add_points.xml
- build.gradle (app et project)
- AndroidManifest.xml
```

---

## 🔹 Prompt 5 – Tests unitaires Android

**Objectif** : Tests JUnit et Mockito pour l'app Android

```
Créer des tests unitaires pour l'application Android Kotlin.

Tests à couvrir:
1. ModelsTest.kt:
   - Vérifier les propriétés des data classes
   - Tests de House, UpdatePointsRequest, ApiResponse

2. ResourceTest.kt:
   - Tests de Resource.Success avec données
   - Tests de Resource.Error avec message
   - Tests de Resource.Loading

3. HouseRepositoryTest.kt (avec Mockito):
   - Mock ApiService
   - Tests getAllHouses (success, error, exception)
   - Tests getHouseById
   - Tests updateHousePoints
   - Tests addPoints
   - Tests resetAllScores

4. MainViewModelTest.kt (avec Coroutines):
   - Mock Repository
   - Tests loadHouses
   - Tests addPoints avec reload
   - Tests updatePoints avec reload
   - Tests resetScores
   - Vérifier que les erreurs n'entraînent pas de reload

Configuration:
- JUnit 4.13
- Mockito Kotlin
- Coroutines Test
- InstantTaskExecutorRule pour LiveData
- StandardTestDispatcher pour coroutines
```

---

## 🔹 Prompt 6 – Dockerfile et Docker Compose

**Objectif** : Containerisation de l'API

```
Créer les fichiers Docker pour containeriser l'API Node.js.

1. Dockerfile (src/api/Dockerfile):
   - Base: node:18-alpine
   - Workdir /app
   - Copy package.json et install
   - Copy source
   - Expose port 3000
   - Volume /data pour SQLite
   - CMD npm start

2. docker-compose.snippet.yml:
   - Service api:
     * Build depuis src/api
     * Port 3000:3000
     * Environnement: PORT, DB_PATH
     * Volume nommé pour /data
     * Restart unless-stopped
     * Health check sur /health toutes les 30s

Volume persistant pour la base de données SQLite.
```

---

## 🔹 Prompt 7 – Tests Smoke et Intégration

**Objectif** : Scripts bash pour tests automatisés

```
Créer deux scripts de test bash pour valider l'application.

1. test_smoke.sh:
   - Lancer Docker Compose
   - Attendre 30s
   - Vérifier containers actifs
   - Test health check
   - Test GET /api/houses (vérifier 4 maisons)
   - Test POST /api/houses/1/add
   - Test GET /api/houses/1 (vérification points)
   - Test POST /api/reset
   - Afficher logs
   - Cleanup avec trap EXIT
   - Couleurs pour output (GREEN, RED, YELLOW)

2. test_integration.sh:
   - Scénario 1: Gestion complète d'une maison
     * Reset
     * Ajouter 100 points
     * Retirer 30 points
     * Vérifier = 70
   - Scénario 2: Compétition entre maisons
     * Attribuer points différents à chaque maison
     * Vérifier classement
   - Scénario 3: Validation des contraintes
     * Test ID invalide (404)
     * Test points invalides (400)
   - Scénario 4: Persistance
     * Définir scores
     * Redémarrer container
     * Vérifier persistance
   - Rapport final

Les deux scripts doivent être robustes avec gestion d'erreurs.
```

---

## 🔹 Prompt 8 – Documentation technique

**Objectif** : Rédiger la documentation complète (README + rendu.md)

```
Rédiger la documentation technique complète pour le projet.

1. README.md (vue d'ensemble):
   - Objectif du projet
   - Architecture (3-tier avec schéma)
   - Technologies utilisées
   - Lancement rapide (Docker, local, Android)
   - API Endpoints (tableau)
   - Tests (backend + Android)
   - Structure du projet (arbre)
   - Fonctionnalités
   - Persistance des données
   - Liens vers docs/

2. docs/rendu.md (document jury):
   - Objectif détaillé
   - Architecture complète avec schémas
   - Technologies avec versions
   - Lancement pas à pas
   - Tests détaillés avec résultats
   - PRA/Backup (commandes)
   - Fonctionnalités exhaustives
   - Endpoints API avec exemples JSON
   - Métriques du projet
   - Notes & Retours (forces, limites, améliorations)
   - Conformité cahier des charges (tableau)
   - Liens utiles

Format Markdown avec emojis, code blocks, tableaux.
Suivre le template AGENTS.md.
```

---

## 🔹 Prompt 9 – Layouts Android XML

**Objectif** : Interface Material Design pour l'application

```
Créer les layouts XML pour l'application Android.

1. activity_main.xml:
   - ScrollView parent
   - LinearLayout vertical avec padding 16dp
   - TextView titre centré "🏰 Tableau des Scores de Poudlard"
   - ProgressBar (id: progressBar, initialement gone)
   - 4 MaterialCardView (elevation 4dp, cornerRadius 12dp):
     * Chaque card contient:
       - TextView nom de la maison (bold, couleur thématique)
       - TextView points (id: house1Points, etc.)
       - Button +/- (id: btnAddHouse1, couleur de la maison)
   - LinearLayout horizontal pour boutons:
     * Button Rafraîchir (id: btnRefresh, icône 🔄)
     * Button Réinitialiser (id: btnReset, rouge)

Couleurs:
- Gryffondor: #7F0909
- Serpentard: #1A472A
- Poufsouffle: #FFDB00
- Serdaigle: #0E1A40

2. dialog_add_points.xml:
   - TextInputLayout avec hint
   - TextInputEditText (id: inputPoints, inputType: numberSigned)

3. strings.xml:
   - app_name: "Scores de Poudlard"
```

---

## 🔹 Prompt 10 – Notes et prompts_used.md

**Objectif** : Documentation du processus de développement

```
Créer deux documents:

1. docs/notes.md:
   - Choix techniques et justifications
   - Problèmes rencontrés et solutions
   - Optimisations effectuées
   - TODO / Améliorations futures
   - Retour d'expérience

2. docs/prompts_used.md:
   - Archiver tous les prompts IA utilisés
   - Numérotés avec objectifs clairs
   - Format Markdown avec sections
   - Exemples de code générés
   - Contexte de chaque prompt

Organisation chronologique suivant le développement.
```

---

## 📊 Statistiques d'utilisation de l'IA

- **Nombre total de prompts** : 10
- **Lignes de code générées** : ~1500 (backend + Android + tests)
- **Documentation générée** : ~500 lignes Markdown
- **Taux de réutilisation sans modification** : ~70%
- **Taux nécessitant ajustements** : ~30%

## 🎯 Bénéfices de l'approche prompt-driven

✅ **Rapidité** : Développement complet en quelques heures  
✅ **Qualité** : Code structuré et testé  
✅ **Conformité** : Respect des standards AGENTS.md  
✅ **Documentation** : Générée automatiquement  
✅ **Tests** : Coverage élevé dès le départ  

## 📝 Leçons apprises

1. **Prompts détaillés** : Plus le prompt est précis, meilleur est le résultat
2. **Architecture d'abord** : Définir la structure avant le code
3. **Tests intégrés** : Demander les tests en même temps que le code
4. **Itération** : Ajuster les prompts si nécessaire
5. **Documentation** : Générer la doc pendant le développement, pas après

---

*Document généré le 13 octobre 2025 dans le cadre du Défi 17 - EPSI Workshop*
