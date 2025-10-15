# 🏰 Tableau des Scores de Poudlard

Application native (Kotlin) + API REST pour gérer les points des 4 maisons de Poudlard.

## 🎯 Objectif

Créer une solution complète permettant de :
- Visualiser les scores des 4 maisons (Gryffondor, Serpentard, Poufsouffle, Serdaigle)
- Ajouter ou retirer des points
- Réinitialiser tous les scores
- Persister les données dans une base SQLite

## 🧩 Architecture

### Services
- **API REST** : Backend Node.js/Express avec SQLite
- **App Android** : Application native Kotlin avec MVVM
- **Base de données** : SQLite (persistée dans un volume Docker)

### Technologies utilisées
- **Backend** : Node.js, Express, SQLite3, Jest
- **Frontend** : Kotlin, Retrofit, Coroutines, LiveData
- **Tests** : Jest (backend), JUnit + Mockito (Android)
- **Containerisation** : Docker, Docker Compose

## 🚀 Lancement rapide

### Prérequis
- Docker et Docker Compose
- Android Studio (pour build de l'app Android)
- Node.js 18+ (pour développement local)

### Démarrage de l'API

```bash
# Avec Docker Compose (recommandé)
docker compose -f docker-compose.snippet.yml up -d

# Ou en local
cd src/api
npm install
npm start
```

L'API sera accessible sur `http://localhost:3000`

### Build de l'application Android

```bash
cd src/android-app
./gradlew build
./gradlew test
```

Pour l'émulateur, l'API sera accessible via `http://10.0.2.2:3000`

## 📡 API Endpoints

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/houses` | Liste des 4 maisons avec scores |
| GET | `/api/houses/:id` | Détail d'une maison |
| PUT | `/api/houses/:id` | Définir les points d'une maison |
| POST | `/api/houses/:id/add` | Ajouter/retirer des points |
| POST | `/api/reset` | Réinitialiser tous les scores |
| GET | `/health` | Health check |

## 🧪 Tests

### Tests Backend (coverage > 80%)

```bash
cd src/api
npm test
```

### Tests Android

```bash
cd src/android-app
./gradlew test
```

## 📦 Structure du projet

```
17-tableau-scores-poudlard/
├── docker-compose.snippet.yml
├── README.md
├── docs/
│   ├── rendu.md
│   ├── prompts_used.md
│   └── notes.md
├── tests/
│   ├── test_smoke.sh
│   └── test_integration.sh
└── src/
    ├── api/                    # Backend Node.js
    │   ├── server.js
    │   ├── database.js
    │   ├── *.test.js
    │   ├── package.json
    │   └── Dockerfile
    └── android-app/            # App native Kotlin
        ├── app/
        │   ├── build.gradle
        │   └── src/
        │       ├── main/
        │       │   ├── java/
        │       │   └── res/
        │       └── test/
        └── build.gradle
```

## 🎮 Fonctionnalités de l'app Android

- ✅ Affichage des 4 maisons avec scores en temps réel
- ✅ Ajout/retrait de points par maison
- ✅ Réinitialisation de tous les scores
- ✅ Rafraîchissement manuel des données
- ✅ Interface Material Design avec couleurs des maisons
- ✅ Gestion d'erreurs et loading states

## 💾 Persistance des données

Les données sont persistées dans une base SQLite stockée dans un volume Docker :
- Volume : `hogwarts-data`
- Chemin : `/data/hogwarts.db`

## 📚 Documentation

- [Documentation technique complète](docs/rendu.md)
- [Prompts IA utilisés](docs/prompts_used.md)
- [Notes de développement](docs/notes.md)

## 🧑‍💻 Développement

### Variables d'environnement

**API** :
- `PORT` : Port du serveur (défaut: 3000)
- `DB_PATH` : Chemin vers la base SQLite

**Android** :
- Configurer l'URL de base dans `RetrofitClient.kt`

## 🏅 Couverture des tests

- Backend : **81.13%** (> 80% requis ✅)
- Android : Tests unitaires pour Models, Repository, ViewModel et Resource

## 🔧 Maintenance

### Backup de la base de données

```bash
docker compose -f docker-compose.snippet.yml exec api cat /data/hogwarts.db > backup.db
```

### Restauration

```bash
cat backup.db | docker compose -f docker-compose.snippet.yml exec -T api sh -c 'cat > /data/hogwarts.db'
```

## 📄 Licence

MIT - EPSI Workshop 2025
