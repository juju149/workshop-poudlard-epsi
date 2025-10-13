# 🦉 Hedwige - Email Web Application with OAuth2

A modern web application for sending and receiving emails with secure OAuth2 authentication using Google services.

## 🎯 Objectif

Créer une application web complète pour la gestion d'emails (réception/envoi) avec authentification OAuth2 sécurisée via Google. L'application permet aux utilisateurs de se connecter avec leur compte Google pour accéder à leurs emails et en envoyer de nouveaux.

## 🏗️ Architecture

```
15-hedwige/
├── docker-compose.snippet.yml    # Configuration Docker Compose
├── src/
│   ├── backend/                  # API Node.js/Express
│   │   ├── server.js            # Serveur principal
│   │   ├── routes/              # Routes API
│   │   │   ├── auth.js         # OAuth2 authentication
│   │   │   └── email.js        # Email management
│   │   ├── tests/              # Tests unitaires
│   │   └── Dockerfile
│   └── frontend/                 # Application React
│       ├── src/
│       │   ├── components/     # Composants réutilisables
│       │   ├── pages/          # Pages de l'application
│       │   └── styles/         # Fichiers CSS
│       ├── tests/              # Tests unitaires frontend
│       ├── Dockerfile
│       └── nginx.conf
├── tests/                        # Tests d'intégration
├── docs/                         # Documentation
└── README.md
```

### Services et modules

- **Backend (Node.js/Express)** : API REST pour l'authentification et la gestion des emails
  - Port: 3001
  - OAuth2 avec Google
  - Gmail API pour les emails
  
- **Frontend (React + Vite)** : Interface utilisateur moderne
  - Port: 3000 (via Nginx)
  - React Router pour la navigation
  - Design responsive

## ⚙️ Technologies utilisées

### Backend
- **Node.js** avec Express
- **Google APIs** (OAuth2 + Gmail)
- **Nodemailer** pour l'envoi d'emails
- **Jest** pour les tests unitaires
- **Docker** pour la containerisation

### Frontend
- **React 18** avec hooks
- **Vite** pour le build rapide
- **React Router** pour la navigation
- **Vitest** pour les tests
- **Nginx** pour le serveur de production

## 🚀 Lancement rapide

### Prérequis

1. Docker et Docker Compose installés
2. Credentials Google OAuth2 (voir Configuration OAuth2)

### Configuration OAuth2

1. Aller sur [Google Cloud Console](https://console.cloud.google.com/)
2. Créer un nouveau projet
3. Activer Gmail API
4. Créer des credentials OAuth2
5. Ajouter les URIs de redirection autorisées:
   - `http://localhost:3001/auth/google/callback`
6. Copier `.env.example` vers `.env` et remplir les valeurs:

```env
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
GOOGLE_REDIRECT_URI=http://localhost:3001/auth/google/callback
```

### Démarrage avec Docker

```bash
# Lancer les services
docker compose -f docker-compose.snippet.yml up -d

# Vérifier les logs
docker compose -f docker-compose.snippet.yml logs -f

# Accéder à l'application
# Frontend: http://localhost:3000
# Backend API: http://localhost:3001
```

### Arrêt des services

```bash
docker compose -f docker-compose.snippet.yml down -v
```

### Développement local

#### Backend

```bash
cd src/backend
npm install
cp .env.example .env
# Éditer .env avec vos credentials
npm run dev
```

#### Frontend

```bash
cd src/frontend
npm install
npm run dev
```

## 🧪 Tests

### Tests unitaires backend

```bash
cd src/backend
npm install
npm test
```

### Tests unitaires frontend

```bash
cd src/frontend
npm install
npm test
```

### Smoke tests

```bash
bash tests/test_smoke.sh
```

### Tests d'intégration

```bash
bash tests/test_integration.sh
```

## 📚 Documentation

- [Rendu complet](docs/rendu.md) - Document de rendu détaillé
- [API Documentation](docs/api.md) - Documentation des endpoints
- [Test Scenarios](docs/test_scenarios.md) - Scénarios de test
- [Prompts utilisés](docs/prompts_used.md) - Historique des prompts IA

## 🔐 Sécurité

- Authentification OAuth2 avec Google
- Sessions sécurisées
- CORS configuré
- Helmet.js pour la sécurité HTTP
- Pas de stockage de mots de passe

## 📦 Fonctionnalités

✅ **Authentification**
- Connexion via Google OAuth2
- Gestion de session sécurisée
- Déconnexion

✅ **Gestion des emails**
- Consultation de la boîte de réception
- Lecture détaillée des emails
- Envoi de nouveaux emails
- Interface utilisateur intuitive

✅ **Interface moderne**
- Design responsive
- Navigation fluide
- Feedback utilisateur
- Gestion des erreurs

## 🛠️ API Endpoints

### Authentication

- `GET /api/auth/google` - Initier OAuth2 flow
- `POST /api/auth/callback` - Callback OAuth2
- `GET /api/auth/session/:sessionId` - Vérifier session
- `DELETE /api/auth/logout/:sessionId` - Déconnexion

### Emails

- `GET /api/emails` - Lister les emails
- `GET /api/emails/:id` - Détail d'un email
- `POST /api/emails/send` - Envoyer un email

## 👥 Copilots recommandés

- 💻 **Frontend Copilot** (lead) - Interface utilisateur
- 🔐 **Security Copilot** - OAuth2 et sécurité
- 🧩 **CI/CD Copilot** - Tests automatisés
- 📚 **Documentation Copilot** - Documentation

## ⏱️ Informations

- **Story Points**: 8
- **Deadline**: 16/10/2025
- **Challenge #15** - HEDWIGE

## 🚧 Améliorations futures

- [ ] Gestion des pièces jointes
- [ ] Filtres et recherche avancée
- [ ] Support multi-comptes
- [ ] Notifications en temps réel
- [ ] Mode hors ligne
- [ ] Archivage d'emails
- [ ] Labels et dossiers
- [ ] Mode sombre

## 📄 Licence

Projet développé dans le cadre du Workshop "Poudlard à l'EPSI/WIS" 2025.

---

**Note**: Cette application nécessite des credentials Google OAuth2 valides pour fonctionner. En production, utiliser des variables d'environnement sécurisées et un stockage de session persistant (Redis, base de données).

✨ *"Les hiboux sont des messagers fiables."* - Rubeus Hagrid
