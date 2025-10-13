# 🧪 Scénarios de test - Hedwige

Ce document décrit les scénarios de test pour l'application Hedwige, couvrant les aspects fonctionnels, techniques et de sécurité.

---

## 📋 Table des matières

1. [Tests d'authentification](#tests-dauthentification)
2. [Tests de gestion des emails](#tests-de-gestion-des-emails)
3. [Tests de sécurité](#tests-de-sécurité)
4. [Tests d'interface utilisateur](#tests-dinterface-utilisateur)
5. [Tests d'intégration](#tests-dintégration)
6. [Tests de performance](#tests-de-performance)

---

## 🔐 Tests d'authentification

### Scénario 1: Authentification réussie avec Google

**Objectif**: Vérifier que l'utilisateur peut se connecter avec son compte Google.

**Préconditions**:
- Application démarrée
- Credentials Google OAuth2 configurés

**Étapes**:
1. Accéder à http://localhost:3000
2. Cliquer sur "Sign in with Google"
3. Saisir les identifiants Google valides
4. Autoriser l'application à accéder aux emails

**Résultat attendu**:
- Redirection vers la page Mailbox
- Affichage du nom et photo de profil de l'utilisateur
- Session créée avec succès

**Critères de succès**:
- ✅ L'utilisateur est authentifié
- ✅ Le sessionId est stocké
- ✅ Les informations utilisateur sont affichées

---

### Scénario 2: Tentative de connexion annulée

**Objectif**: Vérifier le comportement quand l'utilisateur annule l'authentification.

**Étapes**:
1. Accéder à http://localhost:3000
2. Cliquer sur "Sign in with Google"
3. Fermer la popup OAuth2 sans s'authentifier

**Résultat attendu**:
- Retour à la page de login
- Aucune session créée
- Message ou indication que la connexion a été annulée

---

### Scénario 3: Session persistante

**Objectif**: Vérifier que la session persiste après rafraîchissement.

**Préconditions**:
- Utilisateur déjà connecté

**Étapes**:
1. Être connecté à l'application
2. Rafraîchir la page (F5)

**Résultat attendu**:
- L'utilisateur reste connecté
- Pas de redirection vers login
- Les données sont restaurées

---

### Scénario 4: Déconnexion

**Objectif**: Vérifier que l'utilisateur peut se déconnecter.

**Préconditions**:
- Utilisateur connecté

**Étapes**:
1. Cliquer sur le bouton "Logout"

**Résultat attendu**:
- Redirection vers la page de login
- Session supprimée
- localStorage nettoyé

---

## 📧 Tests de gestion des emails

### Scénario 5: Consultation de la boîte de réception

**Objectif**: Vérifier que l'utilisateur peut consulter ses emails.

**Préconditions**:
- Utilisateur authentifié
- Au moins 1 email dans la boîte de réception

**Étapes**:
1. Accéder à la page Mailbox
2. Observer la liste des emails

**Résultat attendu**:
- Liste des emails affichée
- Pour chaque email: expéditeur, sujet, date, extrait
- Compteur d'emails affiché (ex: "Inbox (5)")

**Critères de succès**:
- ✅ Les emails sont chargés depuis Gmail
- ✅ Les informations sont correctement formatées
- ✅ Les dates sont relatives (Aujourd'hui, Hier, etc.)

---

### Scénario 6: Lecture d'un email

**Objectif**: Vérifier que l'utilisateur peut lire le contenu complet d'un email.

**Préconditions**:
- Utilisateur authentifié
- Liste d'emails affichée

**Étapes**:
1. Cliquer sur un email dans la liste

**Résultat attendu**:
- Vue détaillée de l'email
- Affichage du sujet complet
- Affichage de l'expéditeur et destinataire
- Affichage du corps complet du message
- Bouton "Back to Inbox" visible

---

### Scénario 7: Retour à la liste depuis la vue détaillée

**Objectif**: Vérifier la navigation entre liste et détail.

**Préconditions**:
- Vue détaillée d'un email affichée

**Étapes**:
1. Cliquer sur "← Back to Inbox"

**Résultat attendu**:
- Retour à la liste des emails
- Liste préservée (pas de rechargement)

---

### Scénario 8: Rafraîchir la liste des emails

**Objectif**: Vérifier que l'utilisateur peut actualiser sa boîte de réception.

**Préconditions**:
- Utilisateur authentifié sur la page Mailbox

**Étapes**:
1. Cliquer sur le bouton "🔄 Refresh"

**Résultat attendu**:
- Nouvelle requête API
- Liste des emails mise à jour
- Indicateur de chargement (si applicable)

---

### Scénario 9: Composition d'un nouvel email

**Objectif**: Vérifier que l'utilisateur peut composer un email.

**Préconditions**:
- Utilisateur authentifié

**Étapes**:
1. Cliquer sur "✉️ Compose"
2. Remplir le destinataire: "test@example.com"
3. Remplir le sujet: "Test Email"
4. Remplir le corps: "This is a test message"
5. Cliquer sur "Send Email"

**Résultat attendu**:
- Message de succès affiché
- Redirection vers Mailbox après 2 secondes
- Email envoyé via Gmail API

**Critères de succès**:
- ✅ Email envoyé avec succès
- ✅ Format RFC 2822 respecté
- ✅ Confirmation visuelle

---

### Scénario 10: Validation du formulaire de composition

**Objectif**: Vérifier que les champs obligatoires sont validés.

**Préconditions**:
- Page de composition affichée

**Étapes**:
1. Laisser le champ "To" vide
2. Cliquer sur "Send Email"

**Résultat attendu**:
- Message d'erreur affiché
- Email non envoyé
- Formulaire reste affiché

**Variations**:
- Sujet vide
- Corps vide
- Email invalide

---

### Scénario 11: Annulation de la composition

**Objectif**: Vérifier que l'utilisateur peut annuler la composition.

**Préconditions**:
- Page de composition affichée
- Contenu saisi dans le formulaire

**Étapes**:
1. Cliquer sur "Cancel"

**Résultat attendu**:
- Retour à la page Mailbox
- Contenu du brouillon perdu (pas de sauvegarde automatique)

---

## 🔒 Tests de sécurité

### Scénario 12: Accès sans authentification

**Objectif**: Vérifier qu'un utilisateur non authentifié ne peut pas accéder aux emails.

**Préconditions**:
- Aucune session active
- localStorage vide

**Étapes**:
1. Accéder directement à http://localhost:3000/mailbox

**Résultat attendu**:
- Redirection automatique vers /login
- Aucune donnée sensible accessible

---

### Scénario 13: Session invalide

**Objectif**: Vérifier le comportement avec un sessionId invalide.

**Préconditions**:
- localStorage contient un sessionId inexistant

**Étapes**:
1. Modifier le sessionId dans localStorage
2. Rafraîchir la page

**Résultat attendu**:
- Redirection vers /login
- Session nettoyée
- Pas d'erreur JavaScript

---

### Scénario 14: Tentative d'accès API directe

**Objectif**: Vérifier que l'API refuse les requêtes sans session.

**Étapes**:
1. Faire une requête GET sur /api/emails sans header x-session-id

**Résultat attendu**:
- Réponse 401 Unauthorized
- Message d'erreur clair

---

### Scénario 15: Protection CORS

**Objectif**: Vérifier que l'API refuse les requêtes d'origines non autorisées.

**Étapes**:
1. Faire une requête depuis un domaine différent

**Résultat attendu**:
- Requête bloquée par le navigateur
- Erreur CORS visible dans la console

---

## 🎨 Tests d'interface utilisateur

### Scénario 16: Interface responsive

**Objectif**: Vérifier que l'interface s'adapte aux différentes tailles d'écran.

**Étapes**:
1. Redimensionner la fenêtre du navigateur
2. Tester sur mobile (375px)
3. Tester sur tablette (768px)
4. Tester sur desktop (1920px)

**Résultat attendu**:
- Layout adaptatif
- Tous les éléments visibles et utilisables
- Pas de dépassement horizontal

---

### Scénario 17: États de chargement

**Objectif**: Vérifier l'affichage pendant le chargement des données.

**Étapes**:
1. Se connecter
2. Observer le chargement initial des emails

**Résultat attendu**:
- Indicateur de chargement affiché
- Message "Loading emails..."
- Pas de contenu vide brusque

---

### Scénario 18: Gestion des erreurs

**Objectif**: Vérifier l'affichage des messages d'erreur.

**Étapes**:
1. Simuler une erreur réseau (désactiver le backend)
2. Tenter de charger les emails

**Résultat attendu**:
- Message d'erreur clair et convivial
- Pas d'erreur JavaScript non gérée
- Possibilité de réessayer

---

### Scénario 19: Email sans sujet

**Objectif**: Vérifier l'affichage d'un email sans sujet.

**Préconditions**:
- Un email sans sujet dans la boîte

**Étapes**:
1. Consulter la liste des emails

**Résultat attendu**:
- Affichage de "(No Subject)" à la place du sujet
- Pas de bug d'affichage

---

### Scénario 20: Email avec contenu HTML

**Objectif**: Vérifier le traitement des emails HTML.

**Préconditions**:
- Un email avec contenu HTML dans la boîte

**Étapes**:
1. Ouvrir un email HTML

**Résultat attendu**:
- Affichage de la version texte
- Ou rendu HTML sécurisé (si implémenté)
- Pas d'exécution de scripts malveillants

---

## 🔗 Tests d'intégration

### Scénario 21: Flux complet utilisateur

**Objectif**: Tester le parcours complet d'un utilisateur.

**Étapes**:
1. Accéder à l'application
2. Se connecter avec Google
3. Consulter la liste des emails
4. Lire un email
5. Composer et envoyer un email
6. Rafraîchir la boîte
7. Se déconnecter

**Résultat attendu**:
- Tous les composants fonctionnent ensemble
- Navigation fluide
- Pas d'erreur

---

### Scénario 22: Démarrage Docker

**Objectif**: Vérifier que l'application démarre correctement via Docker.

**Étapes**:
1. Exécuter `docker compose -f docker-compose.snippet.yml up -d`
2. Attendre 30 secondes
3. Accéder à http://localhost:3000

**Résultat attendu**:
- Containers démarrés
- Frontend accessible
- Backend répond aux health checks
- Pas d'erreur dans les logs

---

## ⚡ Tests de performance

### Scénario 23: Temps de chargement initial

**Objectif**: Mesurer le temps de chargement de l'application.

**Étapes**:
1. Vider le cache du navigateur
2. Accéder à http://localhost:3000
3. Mesurer le temps jusqu'à l'affichage complet

**Critères de succès**:
- ✅ < 2 secondes pour le chargement initial
- ✅ < 500ms pour les interactions

---

### Scénario 24: Chargement de nombreux emails

**Objectif**: Vérifier les performances avec beaucoup d'emails.

**Préconditions**:
- Boîte de réception avec 100+ emails

**Étapes**:
1. Charger la liste des emails (maxResults=100)
2. Observer le temps de rendu

**Résultat attendu**:
- Liste affichée en < 3 secondes
- Scroll fluide
- Pas de ralentissement du navigateur

---

## 📊 Matrice de tests

| Scénario | Type | Priorité | Automatisé |
|----------|------|----------|------------|
| 1-4 | Authentification | Haute | ✅ Partiel |
| 5-11 | Emails | Haute | ✅ Partiel |
| 12-15 | Sécurité | Critique | ✅ Oui |
| 16-20 | UI | Moyenne | ❌ Manuel |
| 21-22 | Intégration | Haute | ✅ Oui |
| 23-24 | Performance | Basse | ❌ Manuel |

---

## 🎯 Couverture des tests

### Tests automatisés

**Backend** (Jest):
- ✅ Routes d'authentification
- ✅ Routes d'emails
- ✅ Middleware de session
- ✅ Gestion d'erreurs

**Frontend** (Vitest):
- ✅ Composants React
- ✅ Navigation
- ✅ Rendu conditionnel

**Intégration** (Bash):
- ✅ Démarrage Docker
- ✅ Health checks
- ✅ Accessibilité endpoints

### Tests manuels requis

- 🔨 Interface responsive
- 🔨 Flux OAuth2 complet
- 🔨 Envoi d'emails réels
- 🔨 Performance avec données volumineuses

---

## 📝 Notes

- Les tests nécessitant des credentials Google OAuth2 réels doivent être effectués manuellement
- Les tests d'intégration Docker sont automatisés via `test_integration.sh`
- Les tests unitaires visent une couverture > 60%
- Les scénarios critiques de sécurité sont prioritaires

---

**Version**: 1.0.0  
**Dernière mise à jour**: 13 octobre 2025
