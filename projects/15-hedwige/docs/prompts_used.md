# 💬 Prompts IA utilisés – Défi 15: HEDWIGE

Ce document archive tous les prompts utilisés pour créer l'application Hedwige avec l'aide de GitHub Copilot et d'autres outils IA.

---

## 🔹 Prompt 1 – Architecture globale

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Définir l'architecture de l'application

```
Créer une architecture pour une application web d'emails avec OAuth2.

Exigences:
- Frontend moderne (React)
- Backend API (Node.js/Express)
- Authentification OAuth2 Google
- Intégration Gmail API
- Docker Compose pour le déploiement
- Tests unitaires

Structure:
- Frontend: React + Vite + React Router
- Backend: Express + Google APIs + Nodemailer
- Documentation complète
- Tests automatisés
```

---

## 🔹 Prompt 2 – Configuration Backend

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Créer la structure du backend Node.js

```
Créer un serveur Express avec les fonctionnalités suivantes:

1. Configuration de base:
   - Express server sur port 3001
   - Middleware: Helmet, CORS, Morgan
   - Routes modulaires
   - Gestion d'erreurs

2. Routes d'authentification OAuth2:
   - GET /api/auth/google - Initier OAuth2
   - POST /api/auth/callback - Gérer le callback
   - GET /api/auth/session/:id - Vérifier session
   - DELETE /api/auth/logout/:id - Déconnexion

3. Routes emails:
   - GET /api/emails - Lister emails
   - GET /api/emails/:id - Détail email
   - POST /api/emails/send - Envoyer email

4. Middleware de sécurité:
   - Vérification de session
   - Validation des inputs

Utiliser Google APIs pour OAuth2 et Gmail.
```

---

## 🔹 Prompt 3 – Routes OAuth2

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Implémenter l'authentification OAuth2 avec Google

```
Créer un fichier routes/auth.js avec:

1. Endpoint GET /google qui génère l'URL OAuth2 avec les scopes:
   - gmail.readonly
   - gmail.send
   - userinfo.email
   - userinfo.profile

2. Endpoint POST /callback qui:
   - Échange le code OAuth2 contre des tokens
   - Récupère les infos utilisateur
   - Crée une session avec sessionId unique
   - Stocke tokens et user info dans un Map
   - Retourne sessionId et user

3. Endpoint GET /session/:sessionId qui vérifie si la session existe

4. Endpoint DELETE /logout/:sessionId qui supprime la session

Exporter le tokenStore pour utilisation dans d'autres routes.
```

---

## 🔹 Prompt 4 – Routes Email

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Implémenter la gestion des emails via Gmail API

```
Créer un fichier routes/email.js avec:

1. Middleware verifySession pour vérifier x-session-id

2. GET /emails avec query param maxResults:
   - Récupérer la liste des messages Gmail
   - Pour chaque message, extraire: id, subject, from, to, date, snippet, body
   - Décoder les données base64
   - Gérer les différents formats de payload

3. GET /emails/:id:
   - Récupérer le message complet
   - Décoder le corps du message
   - Retourner toutes les métadonnées

4. POST /emails/send avec body {to, subject, body}:
   - Valider les champs requis
   - Créer l'email au format RFC 2822
   - Encoder en base64url
   - Envoyer via Gmail API
   - Retourner l'ID du message envoyé

Utiliser googleapis pour interagir avec Gmail.
```

---

## 🔹 Prompt 5 – Frontend React

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Créer l'application React

```
Créer une application React avec Vite incluant:

1. Structure:
   - src/main.jsx - Point d'entrée
   - src/App.jsx - Composant principal avec router
   - src/pages/ - LoginPage, MailboxPage, ComposePage
   - src/components/ - EmailList, EmailDetail
   - src/styles/ - CSS pour chaque composant

2. App.jsx:
   - React Router avec routes protégées
   - Gestion de sessionId dans localStorage
   - Vérification de session au montage
   - Fonctions handleLogin et handleLogout

3. Navigation:
   - /login - Page de connexion
   - /mailbox - Liste des emails
   - /compose - Composition d'email
   - Redirection automatique selon l'authentification

4. État global:
   - sessionId
   - user (id, email, name, picture)

Utiliser React Router 6 et hooks modernes.
```

---

## 🔹 Prompt 6 – Page de Login

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Créer la page d'authentification

```
Créer LoginPage.jsx avec:

1. Design attrayant:
   - Titre "🦉 Hedwige"
   - Sous-titre "Your magical email companion"
   - Bouton "Sign in with Google" avec logo Google
   - Liste des fonctionnalités

2. Fonctionnalité:
   - Appeler /api/auth/google pour obtenir authUrl
   - Ouvrir popup OAuth2 centrée (500x600)
   - Détecter le code OAuth2 dans l'URL du popup
   - Fermer la popup
   - Appeler /api/auth/callback avec le code
   - Appeler onLogin avec sessionId et user

3. États:
   - loading pendant l'authentification
   - error pour afficher les erreurs
   - Spinner animé pendant le chargement

Inclure le CSS correspondant avec gradient de fond.
```

---

## 🔹 Prompt 7 – Page Mailbox

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Créer la page de consultation des emails

```
Créer MailboxPage.jsx avec:

1. Layout:
   - Header avec logo, user info, bouton logout
   - Sidebar avec boutons "Compose" et "Refresh"
   - Zone principale pour EmailList ou EmailDetail

2. Fonctionnalité:
   - Charger les emails au montage
   - Afficher EmailList par défaut
   - handleEmailClick pour afficher EmailDetail
   - handleBackToList pour revenir à la liste
   - handleCompose pour naviguer vers /compose
   - handleRefresh pour recharger les emails

3. États:
   - emails (array)
   - selectedEmail (object ou null)
   - loading
   - error

4. Gestion d'erreurs:
   - Afficher message si échec de chargement
   - Vérifier la session

Inclure le CSS avec layout flexible.
```

---

## 🔹 Prompt 8 – Page Compose

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Créer la page de composition d'email

```
Créer ComposePage.jsx avec:

1. Formulaire:
   - Input "To" (type email)
   - Input "Subject"
   - Textarea "Message" (15 lignes)
   - Boutons "Send Email" et "Cancel"

2. Validation:
   - Vérifier que tous les champs sont remplis
   - Afficher erreur si champs manquants
   - Validation email du destinataire

3. Envoi:
   - POST /api/emails/send avec to, subject, body
   - Afficher message de succès
   - Rediriger vers /mailbox après 2 secondes
   - Désactiver les champs pendant l'envoi

4. États:
   - to, subject, body
   - sending
   - error
   - success

Inclure le CSS avec design moderne et professionnel.
```

---

## 🔹 Prompt 9 – Composant EmailList

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Créer le composant de liste d'emails

```
Créer EmailList.jsx qui affiche:

1. Header avec "Inbox (X)" où X = nombre d'emails

2. Liste d'emails avec pour chaque item:
   - Expéditeur (extractName)
   - Sujet (ou "(No Subject)")
   - Date formatée (relative: Aujourd'hui, Hier, etc.)
   - Snippet (extrait du message)
   - onClick pour appeler onEmailClick(id)

3. Fonctions utilitaires:
   - formatDate: convertir date en format relatif
   - extractEmail: extraire email de "Name <email>"
   - extractName: extraire nom de "Name <email>"

4. État vide:
   - Afficher "No emails found" si liste vide

CSS avec items cliquables et hover effect.
```

---

## 🔹 Prompt 10 – Composant EmailDetail

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Créer le composant de détail d'email

```
Créer EmailDetail.jsx qui affiche:

1. Bouton "← Back to Inbox"

2. Contenu de l'email:
   - Sujet (grand titre)
   - Métadonnées:
     * From: nom et <email>
     * To: destinataire
     * Date: format complet
   - Corps du message (dans <pre> pour préserver formatting)

3. Fonctions:
   - formatDate: date complète formatée
   - extractName: nom de l'expéditeur
   - extractEmail: email de l'expéditeur

4. Gestion du cas null:
   - Afficher "Select an email to read" si email = null

CSS avec mise en page claire et lisible.
```

---

## 🔹 Prompt 11 – Tests Backend

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Créer les tests unitaires backend

```
Créer tests/api.test.js avec Jest et Supertest pour tester:

1. Health check:
   - GET /health retourne 200 et status ok

2. Routes auth:
   - GET /api/auth/google retourne authUrl
   - POST /api/auth/callback sans code retourne 400
   - GET /api/auth/session/:id avec ID invalide retourne 404

3. Routes email:
   - GET /api/emails sans session retourne 401
   - GET /api/emails avec session invalide retourne 401
   - POST /api/emails/send sans session retourne 401
   - POST /api/emails/send sans champs requis retourne 400

4. 404 handler:
   - Route inconnue retourne 404

Configuration Jest:
- testEnvironment: node
- collectCoverageFrom
- coverageThreshold: 60%
```

---

## 🔹 Prompt 12 – Tests Frontend

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Créer les tests unitaires frontend

```
Créer les tests avec Vitest et Testing Library:

1. tests/App.test.jsx:
   - Vérifie que App render sans erreur
   - Vérifie la redirection vers login par défaut

2. tests/LoginPage.test.jsx:
   - Vérifie le rendu de LoginPage
   - Vérifie la présence du bouton Google login
   - Vérifie l'affichage du titre "Hedwige"

3. tests/EmailList.test.jsx:
   - Vérifie l'affichage de l'état vide
   - Vérifie l'affichage d'emails
   - Vérifie le compteur d'inbox

Configuration Vitest:
- environment: jsdom
- setupFiles: tests/setup.js
- coverage avec v8
```

---

## 🔹 Prompt 13 – Dockerfiles

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Créer les Dockerfiles

```
Créer deux Dockerfiles:

1. Backend (src/backend/Dockerfile):
   - Base: node:18-alpine
   - Copier package.json et installer dépendances (npm ci)
   - Copier le code source
   - Exposer port 3001
   - Healthcheck sur /health
   - CMD: node server.js

2. Frontend (src/frontend/Dockerfile):
   - Multi-stage build
   - Stage 1: builder avec node:18-alpine
     * Installer dépendances
     * Build avec npm run build
   - Stage 2: nginx:alpine
     * Copier dist/ vers /usr/share/nginx/html
     * Copier nginx.conf
     * Exposer port 80

Optimiser pour la taille et la sécurité.
```

---

## 🔹 Prompt 14 – Docker Compose

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Créer docker-compose.snippet.yml

```
Créer docker-compose.snippet.yml avec:

1. Service backend:
   - Build: src/backend
   - Port: 3001:3001
   - Variables d'environnement depuis .env
   - Healthcheck
   - Restart: unless-stopped

2. Service frontend:
   - Build: src/frontend
   - Port: 3000:80
   - Depends_on: backend avec condition service_healthy
   - Restart: unless-stopped

3. Network:
   - hedwige-network (bridge)

Les deux services doivent être sur le même réseau.
```

---

## 🔹 Prompt 15 – Nginx Configuration

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Configurer Nginx pour le frontend

```
Créer nginx.conf avec:

1. Server block:
   - Listen 80
   - Root /usr/share/nginx/html
   - index index.html

2. Proxy /api vers backend:3001:
   - Headers X-Real-IP, X-Forwarded-For
   - Support WebSocket (Upgrade, Connection)

3. React Router support:
   - try_files pour SPA routing
   - Redirection vers index.html

4. Cache des assets statiques:
   - Cache 1 an pour .js, .css, images
   - Gzip compression

5. Security headers
```

---

## 🔹 Prompt 16 – Scripts de test

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Créer les scripts de test

```
Créer deux scripts bash:

1. tests/test_smoke.sh:
   - Vérifier la structure du projet
   - Tester l'existence des fichiers essentiels
   - Vérifier le contenu (OAuth, Gmail API, React Router)
   - Compteur de tests passed/failed
   - Couleurs pour le feedback
   - Exit code approprié

2. tests/test_integration.sh:
   - Démarrer docker compose
   - Attendre 30 secondes
   - Tester health check backend (200)
   - Tester accessibilité frontend (200)
   - Tester endpoints API
   - Vérifier containers en cours d'exécution
   - Arrêter docker compose
   - Rapport de tests avec compteur

Les deux scripts doivent être exécutables (chmod +x).
```

---

## 🔹 Prompt 17 – README

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Créer le README principal

```
Créer README.md avec:

1. Titre et description
2. Architecture et diagramme
3. Technologies utilisées
4. Guide de configuration OAuth2
5. Instructions de lancement (Docker et local)
6. Section tests
7. Documentation API (liens)
8. Fonctionnalités
9. Sécurité
10. Améliorations futures
11. Informations projet (Story Points, deadline)

Style professionnel avec emojis et sections claires.
Inclure des exemples de commandes.
```

---

## 🔹 Prompt 18 – Documentation API

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Documenter tous les endpoints

```
Créer docs/api.md avec:

1. Pour chaque endpoint:
   - Méthode HTTP et URL
   - Description
   - Headers requis
   - Query parameters (si applicable)
   - Body (si applicable)
   - Exemple de requête
   - Exemple de réponse (200)
   - Erreurs possibles

2. Endpoints à documenter:
   - GET /auth/google
   - POST /auth/callback
   - GET /auth/session/:id
   - DELETE /auth/logout/:id
   - GET /emails
   - GET /emails/:id
   - POST /emails/send
   - GET /health

3. Sections supplémentaires:
   - Authentication flow
   - Sécurité
   - Exemples cURL et JavaScript
   - Codes de statut HTTP
   - Format des erreurs

Style OpenAPI-like avec exemples complets.
```

---

## 🔹 Prompt 19 – Scénarios de test

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Documenter les scénarios de test

```
Créer docs/test_scenarios.md avec:

1. Scénarios d'authentification (4-5):
   - Connexion réussie
   - Connexion annulée
   - Session persistante
   - Déconnexion

2. Scénarios emails (6-7):
   - Consultation boîte de réception
   - Lecture email
   - Composition et envoi
   - Validation formulaire
   - Rafraîchissement

3. Scénarios sécurité (4):
   - Accès sans auth
   - Session invalide
   - Protection API
   - CORS

4. Scénarios UI (4-5):
   - Responsive
   - États de chargement
   - Gestion erreurs
   - Edge cases

5. Tests intégration et performance (3-4)

Pour chaque scénario:
- Objectif
- Préconditions
- Étapes
- Résultat attendu
- Critères de succès

Inclure une matrice de tests et couverture.
```

---

## 🔹 Prompt 20 – Document de rendu

**Date**: 2025-10-13  
**Outil**: GitHub Copilot  
**Objectif**: Créer le document de rendu final

```
Créer docs/rendu.md suivant le template AGENTS.md avec:

1. Objectif (1 phrase claire)
2. Architecture détaillée:
   - Services et modules
   - Diagramme ASCII
   - Ports et dépendances
3. Technologies utilisées (backend + frontend)
4. Lancement rapide (Docker + local)
5. Tests (tous les types)
6. PRA / Backup:
   - Stratégie de données
   - Recommandations production
7. Sécurité:
   - Mesures implémentées
   - Améliorations recommandées
8. Métriques de qualité
9. Notes & Retours:
   - Points forts
   - Limitations
   - Perspectives
10. Livrables
11. Apprentissages

Format markdown professionnel avec emojis.
Suivre exactement le template du fichier agents/AGENTS.md.
```

---

## 🔹 Prompts & résultats – 15 octobre 2025

### Prompt utilisateur :

On va modifier le provider pour se connecter avec Outlook plutôt, je veux pouvoir envoyer des mails à partir de mon adresse mail/mot de passe, ils seront écrits en dur dans le code
Je veux pouvoir envoyer et recevoir des mails

**Résultat Copilot :**
- Ajout de nodemailer et imap-simple
- Modification du backend pour Outlook SMTP/IMAP
- Variables d'environnement pour le mail et le mot de passe
- Suppression de la logique Google/Gmail
- Adaptation du docker-compose

---

### Prompt utilisateur :

Déjà ajoute moi des variables d'environnement pour le mail et le mot de passe

**Résultat Copilot :**
- Ajout des variables OUTLOOK_EMAIL et OUTLOOK_PASSWORD dans le backend
- Création du fichier .env et .env.example

---

### Prompt utilisateur :

Oui vérifie et modifie le .env.example pour le match

**Résultat Copilot :**
- Synchronisation des variables entre .env et .env.example

---

### Prompt utilisateur :

supprime la partie google aussi

**Résultat Copilot :**
- Suppression des variables Google OAuth et Gmail du .env.example

---

### Prompt utilisateur :

Le session secret sert à rien vérifie

**Résultat Copilot :**
- Vérification de l'utilisation de SESSION_SECRET
- Suppression de SESSION_SECRET du .env.example et du docker-compose

---

### Prompt utilisateur :

supprime là et clean le docker compose au niveau des variables d'environnement

**Résultat Copilot :**
- Suppression de SESSION_SECRET
- Nettoyage du docker-compose (suppression Google et SESSION_SECRET, ajout Outlook)

---

### Prompt utilisateur :

Alors maintenant on va delete la page de login comme c'est écrit en dur, tu récupères directement mes mails lors du lancement de l'app

**Résultat Copilot :**
- Suppression de LoginPage.jsx
- Modification de App.jsx pour accès direct à la boîte mail

---

### Prompt utilisateur :

j'ai trouvé le problème, le .env est pas correctement récupéré dans le fichier email.js

**Résultat Copilot :**
- Ajout de dotenv dans email.js

---

### Prompt utilisateur :

là j'ai un .env qui contient l'url du frontend aussi faudrait en faire 2 ou le déplacer

**Résultat Copilot :**
- Création d'un .env pour le frontend
- Suppression de FRONTEND_URL du backend
- Création de .env et .env.example dans le frontend
- Nettoyage du .env backend

---

### Prompt utilisateur :

ajoute un .env.example dans le frontend

**Résultat Copilot :**
- Ajout de .env.example dans src/frontend

---

### Prompt utilisateur :

Maintenant adapte le docker compose avec tout ça

**Résultat Copilot :**
- Adaptation du docker-compose pour séparer les variables frontend/backend

---
