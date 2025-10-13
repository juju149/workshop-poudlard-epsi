# 📖 Documentation API - Hedwige

## Base URL

```
http://localhost:3001/api
```

## Authentication

L'API utilise un système de session basé sur des identifiants de session. Après authentification OAuth2, l'utilisateur reçoit un `sessionId` qu'il doit inclure dans le header `x-session-id` pour toutes les requêtes authentifiées.

---

## 🔐 Authentication Endpoints

### 1. Initier l'authentification Google OAuth2

**Endpoint**: `GET /auth/google`

**Description**: Génère l'URL d'authentification Google OAuth2.

**Request**:
```http
GET /api/auth/google
```

**Response** (200 OK):
```json
{
  "authUrl": "https://accounts.google.com/o/oauth2/v2/auth?..."
}
```

**Utilisation**:
1. Appeler cet endpoint pour obtenir l'URL OAuth2
2. Rediriger l'utilisateur vers cette URL
3. L'utilisateur s'authentifie avec Google
4. Google redirige vers l'URI de callback avec un code

---

### 2. Callback OAuth2

**Endpoint**: `POST /auth/callback`

**Description**: Échange le code OAuth2 contre des tokens d'accès et crée une session.

**Request**:
```http
POST /api/auth/callback
Content-Type: application/json

{
  "code": "4/0AfJohXk..."
}
```

**Response** (200 OK):
```json
{
  "sessionId": "session_1234567890_abc123",
  "user": {
    "id": "1234567890",
    "email": "user@example.com",
    "name": "John Doe",
    "picture": "https://..."
  }
}
```

**Errors**:
- `400 Bad Request`: Code manquant
- `500 Internal Server Error`: Échec de l'authentification

---

### 3. Vérifier une session

**Endpoint**: `GET /auth/session/:sessionId`

**Description**: Vérifie si une session est valide et retourne les informations utilisateur.

**Request**:
```http
GET /api/auth/session/session_1234567890_abc123
```

**Response** (200 OK):
```json
{
  "user": {
    "id": "1234567890",
    "email": "user@example.com",
    "name": "John Doe",
    "picture": "https://..."
  }
}
```

**Errors**:
- `404 Not Found`: Session inexistante ou expirée

---

### 4. Déconnexion

**Endpoint**: `DELETE /auth/logout/:sessionId`

**Description**: Supprime la session et déconnecte l'utilisateur.

**Request**:
```http
DELETE /api/auth/logout/session_1234567890_abc123
```

**Response** (200 OK):
```json
{
  "message": "Logged out successfully"
}
```

---

## 📧 Email Endpoints

Tous les endpoints email nécessitent le header `x-session-id`.

### 5. Lister les emails

**Endpoint**: `GET /emails`

**Description**: Récupère la liste des emails de la boîte de réception.

**Headers**:
```
x-session-id: session_1234567890_abc123
```

**Query Parameters**:
- `maxResults` (optional): Nombre d'emails à récupérer (défaut: 10, max: 100)

**Request**:
```http
GET /api/emails?maxResults=20
x-session-id: session_1234567890_abc123
```

**Response** (200 OK):
```json
{
  "emails": [
    {
      "id": "18c5f3a4b2e1d9f0",
      "threadId": "18c5f3a4b2e1d9f0",
      "subject": "Welcome to Hedwige",
      "from": "Hedwige Team <noreply@hedwige.com>",
      "to": "user@example.com",
      "date": "Mon, 13 Oct 2025 10:30:00 +0000",
      "snippet": "Welcome to your magical email companion...",
      "body": "Welcome to your magical email companion..." 
    }
  ],
  "total": 1
}
```

**Errors**:
- `401 Unauthorized`: Session ID manquant ou invalide
- `500 Internal Server Error`: Échec de récupération des emails

---

### 6. Lire un email spécifique

**Endpoint**: `GET /emails/:id`

**Description**: Récupère le contenu complet d'un email.

**Headers**:
```
x-session-id: session_1234567890_abc123
```

**Request**:
```http
GET /api/emails/18c5f3a4b2e1d9f0
x-session-id: session_1234567890_abc123
```

**Response** (200 OK):
```json
{
  "id": "18c5f3a4b2e1d9f0",
  "threadId": "18c5f3a4b2e1d9f0",
  "subject": "Welcome to Hedwige",
  "from": "Hedwige Team <noreply@hedwige.com>",
  "to": "user@example.com",
  "date": "Mon, 13 Oct 2025 10:30:00 +0000",
  "snippet": "Welcome to your magical email companion...",
  "body": "Full email body content here...\n\nWith multiple lines..."
}
```

**Errors**:
- `401 Unauthorized`: Session ID manquant ou invalide
- `404 Not Found`: Email inexistant
- `500 Internal Server Error`: Échec de récupération de l'email

---

### 7. Envoyer un email

**Endpoint**: `POST /emails/send`

**Description**: Envoie un nouvel email.

**Headers**:
```
x-session-id: session_1234567890_abc123
Content-Type: application/json
```

**Request**:
```http
POST /api/emails/send
x-session-id: session_1234567890_abc123
Content-Type: application/json

{
  "to": "recipient@example.com",
  "subject": "Hello from Hedwige",
  "body": "This is a test email sent from Hedwige!"
}
```

**Response** (200 OK):
```json
{
  "message": "Email sent successfully",
  "id": "18c5f3a4b2e1d9f1",
  "threadId": "18c5f3a4b2e1d9f1"
}
```

**Errors**:
- `400 Bad Request`: Champs manquants (to, subject, body)
- `401 Unauthorized`: Session ID manquant ou invalide
- `500 Internal Server Error`: Échec d'envoi de l'email

---

## 🏥 Health Check

### 8. Health Check

**Endpoint**: `GET /health`

**Description**: Vérifie l'état de l'API.

**Request**:
```http
GET /health
```

**Response** (200 OK):
```json
{
  "status": "ok",
  "message": "Hedwige API is running"
}
```

---

## 🔒 Sécurité

### Headers de sécurité

L'API utilise Helmet.js pour ajouter les headers de sécurité suivants:
- `X-DNS-Prefetch-Control`
- `X-Frame-Options`
- `X-Content-Type-Options`
- `Strict-Transport-Security`
- `X-Download-Options`
- `X-Permitted-Cross-Domain-Policies`

### CORS

CORS est configuré pour accepter les requêtes depuis le frontend (http://localhost:3000).

### Session Management

Les sessions sont identifiées par un ID unique généré aléatoirement:
- Format: `session_[timestamp]_[random]`
- Stockage en mémoire (Map)
- Expiration: jamais (à implémenter en production)

---

## 📊 Codes de statut HTTP

| Code | Description |
|------|-------------|
| 200 | Succès |
| 400 | Requête invalide |
| 401 | Non authentifié |
| 404 | Ressource non trouvée |
| 500 | Erreur serveur |

---

## 🧪 Exemples d'utilisation

### Exemple complet avec cURL

```bash
# 1. Obtenir l'URL OAuth2
curl http://localhost:3001/api/auth/google

# 2. Après authentification, échanger le code
curl -X POST http://localhost:3001/api/auth/callback \
  -H "Content-Type: application/json" \
  -d '{"code":"4/0AfJohXk..."}'

# 3. Lister les emails (avec le sessionId reçu)
curl http://localhost:3001/api/emails \
  -H "x-session-id: session_1234567890_abc123"

# 4. Lire un email spécifique
curl http://localhost:3001/api/emails/18c5f3a4b2e1d9f0 \
  -H "x-session-id: session_1234567890_abc123"

# 5. Envoyer un email
curl -X POST http://localhost:3001/api/emails/send \
  -H "Content-Type: application/json" \
  -H "x-session-id: session_1234567890_abc123" \
  -d '{
    "to": "recipient@example.com",
    "subject": "Test Email",
    "body": "Hello from Hedwige!"
  }'

# 6. Déconnexion
curl -X DELETE http://localhost:3001/api/auth/logout/session_1234567890_abc123
```

### Exemple avec JavaScript (fetch)

```javascript
// 1. Obtenir l'URL OAuth2
const authResponse = await fetch('/api/auth/google');
const { authUrl } = await authResponse.json();
window.location.href = authUrl;

// 2. Après callback, échanger le code
const callbackResponse = await fetch('/api/auth/callback', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ code: authCode })
});
const { sessionId, user } = await callbackResponse.json();
localStorage.setItem('sessionId', sessionId);

// 3. Lister les emails
const emailsResponse = await fetch('/api/emails?maxResults=20', {
  headers: { 'x-session-id': sessionId }
});
const { emails } = await emailsResponse.json();

// 4. Envoyer un email
const sendResponse = await fetch('/api/emails/send', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'x-session-id': sessionId
  },
  body: JSON.stringify({
    to: 'recipient@example.com',
    subject: 'Hello',
    body: 'Test email'
  })
});
```

---

## 🐛 Gestion des erreurs

Toutes les erreurs suivent le même format:

```json
{
  "error": {
    "message": "Description de l'erreur",
    "status": 400
  }
}
```

---

## 📝 Notes

- Les tokens OAuth2 sont rafraîchis automatiquement
- Les emails sont récupérés directement depuis Gmail (pas de cache)
- Le format des emails suit le standard RFC 2822
- Les sessions sont en mémoire (non persistantes entre redémarrages)

---

**Version**: 1.0.0  
**Dernière mise à jour**: 13 octobre 2025
