# 🧾 Rendu – Défi 15 : HEDWIGE

## 🎯 Objectif

Créer une application web complète pour la gestion d'emails (réception/envoi) avec authentification OAuth2 sécurisée via Google Gmail API. L'application permet aux utilisateurs de se connecter avec leur compte Google pour accéder à leurs emails et en envoyer de nouveaux.

## 🧩 Architecture

### Services et modules

L'application est composée de deux services principaux communiquant via API REST:

1. **Backend API (Node.js/Express)**
   - Serveur API REST sur le port 3001
   - Gestion OAuth2 avec Google
   - Intégration Gmail API pour les emails
   - Middleware de sécurité (Helmet, CORS)
   - Gestion de sessions

2. **Frontend SPA (React)**
   - Application React moderne
   - Servie par Nginx sur le port 3000
   - Interface responsive
   - React Router pour la navigation

### Diagramme d'architecture

```
┌─────────────────────────────────────────────────┐
│                  Utilisateur                     │
└────────────────────┬────────────────────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │   Frontend (React)     │
         │   Port: 3000 (Nginx)  │
         │  - Login page          │
         │  - Mailbox page        │
         │  - Compose page        │
         └───────────┬───────────┘
                     │ HTTP/REST API
                     ▼
         ┌───────────────────────┐
         │  Backend (Express)     │
         │   Port: 3001           │
         │  - OAuth2 routes       │
         │  - Email routes        │
         └───────────┬───────────┘
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
┌──────────────┐         ┌──────────────┐
│ Google OAuth2│         │  Gmail API   │
│   Service    │         │   Service    │
└──────────────┘         └──────────────┘
```

### Ports et dépendances

- **Frontend**: Port 3000 (HTTP)
  - Dépend du backend pour l'API
  
- **Backend**: Port 3001 (HTTP)
  - Dépend de Google OAuth2
  - Dépend de Gmail API

## ⚙️ Technologies utilisées

### Backend
- **Docker** / Docker Compose - Containerisation
- **Node.js 18** - Runtime JavaScript
- **Express 4** - Framework web
- **Google APIs** - OAuth2 + Gmail
- **Nodemailer** - Gestion emails
- **Helmet** - Sécurité HTTP
- **Morgan** - Logging
- **Jest** - Tests unitaires
- **Supertest** - Tests API

### Frontend
- **Docker** / Docker Compose - Containerisation
- **React 18** - Bibliothèque UI
- **Vite** - Build tool moderne
- **React Router 6** - Navigation SPA
- **Axios** - Client HTTP
- **Vitest** - Tests unitaires
- **Testing Library** - Tests composants
- **Nginx** - Serveur web production

## 🚀 Lancement rapide

### Configuration préalable

1. **Obtenir les credentials Google OAuth2**:
   - Créer un projet sur [Google Cloud Console](https://console.cloud.google.com/)
   - Activer Gmail API
   - Créer des credentials OAuth2
   - Configurer les URIs de redirection: `http://localhost:3001/auth/google/callback`

2. **Créer le fichier .env** (à la racine du projet):

```env
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:3001/auth/google/callback
FRONTEND_URL=http://localhost:3000
SESSION_SECRET=your_random_secret_here
```

### Lancement avec Docker

```bash
# Lancer tous les services
docker compose -f docker-compose.snippet.yml up -d

# Vérifier les logs
docker compose -f docker-compose.snippet.yml logs -f

# Accéder à l'application
# Frontend: http://localhost:3000
# Backend API: http://localhost:3001/health
```

### Arrêt des services

```bash
docker compose -f docker-compose.snippet.yml down -v
```

### Développement local (sans Docker)

**Backend**:
```bash
cd src/backend
npm install
cp .env.example .env
# Éditer .env avec vos credentials
npm run dev
```

**Frontend**:
```bash
cd src/frontend
npm install
npm run dev
```

## 🧪 Tests

### Smoke tests (structure du projet)

```bash
bash tests/test_smoke.sh
```

Vérifie:
- Structure des dossiers
- Présence des fichiers essentiels
- Configuration Docker
- Documentation

### Tests d'intégration

```bash
bash tests/test_integration.sh
```

Vérifie:
- Démarrage des services Docker
- Health checks
- Accessibilité des endpoints
- Authentification requise

### Tests unitaires backend

```bash
cd src/backend
npm install
npm test

# Avec coverage
npm test -- --coverage
```

Tests:
- Routes d'authentification OAuth2
- Routes de gestion des emails
- Middleware de session
- Gestion d'erreurs

### Tests unitaires frontend

```bash
cd src/frontend
npm install
npm test

# Avec coverage
npm run test -- --coverage
```

Tests:
- Composants React
- Pages de l'application
- Navigation
- Gestion d'état

## 💾 PRA / Backup

### Données

- **Sessions utilisateur**: Stockées en mémoire (Map)
  - En production: utiliser Redis ou base de données
  
- **Tokens OAuth2**: Stockés temporairement
  - Rafraîchissement automatique via refresh token
  
- **Emails**: Récupérés depuis Gmail (pas de stockage local)

### Stratégie de sauvegarde

- Code source versionné sur GitHub
- Configuration Docker reproductible
- Variables d'environnement externalisées
- Documentation complète

### Recommandations production

1. **Base de données** pour les sessions persistantes
2. **Redis** pour le cache
3. **Load balancer** pour la scalabilité
4. **HTTPS** avec certificats SSL
5. **Monitoring** (Prometheus, Grafana)
6. **Logging centralisé** (ELK stack)

## 🔐 Sécurité

### Mesures implémentées

- ✅ OAuth2 avec Google (pas de gestion de mots de passe)
- ✅ CORS configuré
- ✅ Helmet.js pour headers HTTP sécurisés
- ✅ Validation des inputs
- ✅ Sessions avec IDs aléatoires
- ✅ HTTPS ready (via reverse proxy)

### Améliorations recommandées

- [ ] Rate limiting
- [ ] JWT pour les tokens
- [ ] CSRF protection
- [ ] Audit logs
- [ ] Encryption at rest

## 📊 Métriques de qualité

### Backend
- **Tests unitaires**: 11 tests
- **Coverage**: > 60%
- **Endpoints**: 7 routes API

### Frontend
- **Tests unitaires**: 5+ tests
- **Composants**: 2 composants + 3 pages
- **Coverage**: > 50%

## 🧠 Notes & Retours

### Points forts

✅ Architecture moderne et scalable
✅ Séparation frontend/backend claire
✅ OAuth2 sécurisé (pas de gestion de mots de passe)
✅ Interface utilisateur intuitive
✅ Tests automatisés
✅ Documentation complète
✅ Dockerisé et reproductible

### Limitations actuelles

⚠️ Sessions en mémoire (non persistantes)
⚠️ Pas de gestion des pièces jointes
⚠️ Pas de recherche avancée
⚠️ Pas de filtres/labels
⚠️ UI basique (pas de rich text editor)

### Perspectives d'amélioration

1. **Fonctionnalités**:
   - Support des pièces jointes
   - Filtres et recherche avancée
   - Labels et dossiers personnalisés
   - Brouillons
   - Réponses/transferts

2. **Technique**:
   - Base de données pour persistance
   - WebSocket pour notifications temps réel
   - Service Workers pour mode hors ligne
   - Pagination optimisée
   - Cache intelligent

3. **UX**:
   - Rich text editor
   - Drag & drop pour pièces jointes
   - Mode sombre
   - Raccourcis clavier
   - Prévisualisation emails

## 📈 Performances

- **Temps de chargement**: < 2s (première visite)
- **Build frontend**: < 30s
- **Build backend**: < 20s
- **Démarrage Docker**: < 60s

## 📚 Livrables

✅ **Code source**
- Repository frontend + backend
- Structure claire et documentée
- Code commenté

✅ **Documentation**
- README technique complet
- Documentation API (docs/api.md)
- Scénarios de test (docs/test_scenarios.md)
- Prompts IA utilisés (docs/prompts_used.md)

✅ **Tests**
- Tests unitaires backend (Jest)
- Tests unitaires frontend (Vitest)
- Tests d'intégration (Bash)
- Smoke tests

✅ **Déploiement**
- Docker Compose configuré
- Dockerfiles optimisés
- Scripts de test automatisés

## 🎓 Apprentissages

- Intégration OAuth2 avec Google
- Architecture microservices
- React moderne avec hooks
- Tests automatisés full-stack
- Containerisation Docker
- API REST design
- Gestion de sessions

---

**Développé avec 🦉 dans le cadre du Workshop Poudlard EPSI/WIS 2025**

✨ *"Les hiboux sont remarquablement intelligents... ils sont capables de trouver n'importe qui n'importe où."* - Hermione Granger
