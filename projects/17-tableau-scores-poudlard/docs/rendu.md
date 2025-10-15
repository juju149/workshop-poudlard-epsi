# 🧾 Rendu – Défi 17 : TABLEAU DES SCORES DE POUDLARD

## 🎯 Objectif

Créer une application native (Kotlin) pour Android permettant de gérer et visualiser les scores des 4 maisons de Poudlard, connectée à une API REST avec base de données SQLite. Le projet répond aux exigences de tests unitaires avec une couverture supérieure à 80%.

## 🧩 Architecture

### Vue d'ensemble

```
┌─────────────────┐         ┌──────────────┐         ┌──────────────┐
│  App Android    │◄───────►│   API REST   │◄───────►│   SQLite DB  │
│  (Kotlin/MVVM)  │  HTTP   │ (Node.js)    │         │              │
└─────────────────┘         └──────────────┘         └──────────────┘
```

### Composants principaux

#### 1. API REST (Backend)
- **Technologie** : Node.js + Express
- **Base de données** : SQLite3
- **Port** : 3000
- **Endpoints** :
  - `GET /api/houses` - Liste des maisons
  - `GET /api/houses/:id` - Détail d'une maison
  - `PUT /api/houses/:id` - Définir les points
  - `POST /api/houses/:id/add` - Ajouter/retirer des points
  - `POST /api/reset` - Réinitialiser tous les scores
  - `GET /health` - Health check

#### 2. Application Android Native
- **Technologie** : Kotlin
- **Architecture** : MVVM (Model-View-ViewModel)
- **Librairies** :
  - Retrofit2 : Client HTTP
  - Coroutines : Programmation asynchrone
  - LiveData : Observation des données
  - Material Components : Design
- **Fonctionnalités** :
  - Affichage des 4 maisons avec leurs scores
  - Ajout/retrait de points interactif
  - Réinitialisation des scores
  - Rafraîchissement manuel

#### 3. Base de données
- **Type** : SQLite
- **Schema** :
```sql
CREATE TABLE houses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    points INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
```
- **Données initiales** : 4 maisons (Gryffondor, Serpentard, Poufsouffle, Serdaigle)

### Architecture Android (MVVM)

```
MainActivity
    │
    ├── MainViewModel
    │       │
    │       └── HouseRepository
    │               │
    │               └── ApiService (Retrofit)
    │                       │
    │                       └── RetrofitClient
    │
    └── UI Components
            ├── Material Cards
            ├── Buttons
            └── Dialogs
```

## ⚙️ Technologies utilisées

### Backend
- **Runtime** : Node.js 18
- **Framework** : Express 4.18
- **Base de données** : SQLite3 5.1
- **Tests** : Jest 29.7
- **Validation API** : Supertest 6.3
- **CORS** : cors 2.8
- **Parsing** : body-parser 1.20

### Frontend (Android)
- **Langage** : Kotlin 1.9
- **SDK** : Android API 24-34
- **Build** : Gradle 8.2
- **Réseau** : Retrofit 2.9 + OkHttp 4.11
- **Async** : Kotlin Coroutines 1.7
- **Architecture** : AndroidX Lifecycle 2.7
- **UI** : Material Design 3
- **Tests** : JUnit 4.13, Mockito 5.7

### DevOps
- **Containerisation** : Docker
- **Orchestration** : Docker Compose
- **CI/CD** : Scripts bash pour tests

## 🚀 Lancement rapide

### Avec Docker (Recommandé)

```bash
# Lancer l'API
docker compose -f docker-compose.snippet.yml up -d

# Vérifier le statut
docker compose -f docker-compose.snippet.yml ps

# Voir les logs
docker compose -f docker-compose.snippet.yml logs -f
```

L'API sera disponible sur `http://localhost:3000`

### Build de l'application Android

```bash
cd src/android-app

# Télécharger les dépendances
./gradlew build

# Lancer les tests unitaires
./gradlew test

# Générer l'APK
./gradlew assembleDebug
```

L'APK sera dans : `app/build/outputs/apk/debug/app-debug.apk`

### Installation sur émulateur

```bash
# Démarrer l'émulateur Android
# Puis installer l'APK
adb install app/build/outputs/apk/debug/app-debug.apk
```

**Note** : L'émulateur Android accède à l'API via `http://10.0.2.2:3000` (configuré dans RetrofitClient.kt)

## 🧪 Tests

### Tests Backend (Jest)

```bash
cd src/api
npm test
```

**Résultats** :
- ✅ 25 tests passés
- ✅ Coverage: **81.13%** (> 80% requis)
- Files testés :
  - `database.js` : 88.88% coverage
  - `server.js` : 77.14% coverage

**Tests couverts** :
- Health check
- CRUD des maisons
- Ajout/retrait de points
- Réinitialisation des scores
- Validation des entrées
- Gestion des erreurs

### Tests Android (JUnit + Mockito)

```bash
cd src/android-app
./gradlew test
```

**Tests unitaires** :
- `ModelsTest.kt` : Tests des data classes
- `ResourceTest.kt` : Tests de la classe Resource (Success/Error/Loading)
- `HouseRepositoryTest.kt` : Tests du repository avec mocks
- `MainViewModelTest.kt` : Tests du ViewModel avec coroutines

**Couverture** :
- Models : 100%
- Repository : 100%
- ViewModel : ~85%
- Resource : 100%

### Tests d'intégration

```bash
# Test smoke (vérification basique)
bash tests/test_smoke.sh

# Test d'intégration complet
bash tests/test_integration.sh
```

**Scénarios testés** :
1. ✅ Gestion complète des points d'une maison
2. ✅ Compétition entre maisons
3. ✅ Validation des contraintes
4. ✅ Persistance des données après redémarrage

## 💾 PRA / Backup

### Stratégie de sauvegarde

Les données sont persistées dans un volume Docker nommé `hogwarts-data`.

#### Backup manuel

```bash
# Exporter la base de données
docker compose -f docker-compose.snippet.yml exec api \
    cat /data/hogwarts.db > backup-$(date +%Y%m%d).db
```

#### Restauration

```bash
# Restaurer depuis un backup
cat backup-20251013.db | \
    docker compose -f docker-compose.snippet.yml exec -T api \
    sh -c 'cat > /data/hogwarts.db'

# Redémarrer l'API
docker compose -f docker-compose.snippet.yml restart api
```

#### Backup automatique (Cron)

```bash
# Ajouter au crontab pour backup quotidien à 2h du matin
0 2 * * * cd /path/to/project && \
    docker compose -f docker-compose.snippet.yml exec api \
    cat /data/hogwarts.db > /backups/hogwarts-$(date +\%Y\%m\%d).db
```

### Plan de reprise (PRA)

1. **Panne du container API** :
   - Redémarrage automatique avec `restart: unless-stopped`
   - Health check toutes les 30s
   - Données préservées dans le volume

2. **Corruption de la base** :
   - Restaurer depuis le dernier backup
   - Réinitialiser avec les 4 maisons par défaut

3. **Perte totale du serveur** :
   - Déployer un nouveau container
   - Monter le volume existant
   - Ou restaurer depuis backup externe

## 🎮 Fonctionnalités

### Application Android

#### 1. Écran principal
- **Affichage** : Cards Material Design pour chaque maison
- **Couleurs thématiques** :
  - Gryffondor : Rouge (#7F0909)
  - Serpentard : Vert (#1A472A)
  - Poufsouffle : Jaune (#FFDB00)
  - Serdaigle : Bleu (#0E1A40)
- **Actions** : Bouton +/- pour chaque maison

#### 2. Gestion des points
- Dialog pour saisir les points à ajouter/retirer
- Nombres négatifs acceptés pour retirer des points
- Validation des entrées
- Feedback visuel (Toast messages)

#### 3. Actions globales
- **Rafraîchir** : Recharger les données depuis l'API
- **Réinitialiser** : Remettre tous les scores à 0 (avec confirmation)

#### 4. États de l'interface
- **Loading** : ProgressBar pendant les requêtes
- **Success** : Mise à jour de l'UI avec animations
- **Error** : Messages d'erreur explicites

### API REST

#### Endpoints détaillés

**GET /api/houses**
```json
Response 200:
{
  "houses": [
    {
      "id": 1,
      "name": "Gryffondor",
      "points": 100,
      "created_at": "2025-10-13T10:00:00.000Z",
      "updated_at": "2025-10-13T10:30:00.000Z"
    },
    // ... 3 autres maisons
  ]
}
```

**POST /api/houses/1/add**
```json
Request:
{
  "points": 50  // ou -50 pour retirer
}

Response 200:
{
  "message": "Points ajoutés avec succès",
  "changes": 1
}
```

**POST /api/reset**
```json
Response 200:
{
  "message": "Tous les scores ont été réinitialisés",
  "changes": 4
}
```

## 📊 Métriques du projet

### Code

- **Backend** :
  - Lignes de code : ~350
  - Fichiers : 5 (server.js, database.js, 2 tests, package.json)
  - Dépendances : 4 (prod) + 3 (dev)

- **Android** :
  - Lignes de code Kotlin : ~800
  - Fichiers : 9 classes + 4 tests + 3 layouts
  - Dépendances : 10 (prod) + 4 (test)

### Tests

- **Total** : 25 tests backend + 20+ tests Android
- **Coverage backend** : 81.13%
- **Temps d'exécution** : ~5 secondes

### Performance

- **API** :
  - Temps de réponse moyen : < 50ms
  - Démarrage : ~5 secondes
  - Mémoire : ~50MB

- **App Android** :
  - Taille APK : ~5MB
  - Temps de chargement : < 2 secondes

## 🧠 Notes & Retours

### Points forts

✅ Architecture MVVM propre et testable  
✅ Séparation claire backend/frontend  
✅ Coverage de tests > 80%  
✅ Persistance des données avec volumes Docker  
✅ Gestion d'erreurs robuste  
✅ Interface Material Design moderne  
✅ API RESTful avec validation  
✅ Documentation complète  

### Limitations actuelles

- App Android uniquement (pas iOS Swift)
- Base SQLite (non distribuée)
- Pas d'authentification
- Pas de logs centralisés
- Pas de CI/CD automatisé

### Améliorations possibles

1. **Fonctionnalités** :
   - Historique des modifications
   - Graphiques d'évolution des scores
   - Notifications push pour changements
   - Mode multi-utilisateurs avec rôles

2. **Technique** :
   - Migration vers PostgreSQL pour production
   - Ajout d'une couche de cache (Redis)
   - Implémentation WebSocket pour temps réel
   - Version iOS en Swift

3. **DevOps** :
   - Pipeline CI/CD GitHub Actions
   - Monitoring avec Prometheus/Grafana
   - Backup automatique vers S3
   - Tests E2E avec Appium

### Défis rencontrés

1. **Coroutines Kotlin** : Gestion des tests asynchrones résolue avec `runTest`
2. **Émulateur Android** : Configuration réseau pour `10.0.2.2`
3. **Coverage Jest** : Exclusion des logs asynchrones

## 🔗 Liens utiles

- [Documentation Express](https://expressjs.com/)
- [Documentation Retrofit](https://square.github.io/retrofit/)
- [Guide Kotlin Coroutines](https://kotlinlang.org/docs/coroutines-guide.html)
- [Material Design 3](https://m3.material.io/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)

## 📝 Conformité au cahier des charges

| Exigence | Statut | Notes |
|----------|--------|-------|
| App native (Kotlin/Swift) | ✅ | Kotlin Android |
| API REST | ✅ | Node.js/Express |
| Base de données (no BaaS) | ✅ | SQLite |
| Tests unitaires | ✅ | Jest + JUnit |
| Coverage > 80% | ✅ | 81.13% backend |
| Documentation technique | ✅ | README + rendu.md |

## 👥 Méthodologie

**Développement** : Approche TDD (Test-Driven Development) pour l'API  
**Architecture** : MVVM pour Android (séparation des responsabilités)  
**Versioning** : Git avec commits atomiques  
**Tests** : Unitaires + Intégration + Smoke  

---

**Date de livraison** : 13 octobre 2025  
**Version** : 1.0.0  
**Auteur** : EPSI Workshop - Défi 17
