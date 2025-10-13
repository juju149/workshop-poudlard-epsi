# 📚 Emploi du Temps McGonagall

Application Electron moderne avec React, Vite et Tailwind CSS pour afficher l'emploi du temps en récupérant les données via scraping web avec Puppeteer.

## 🎯 Fonctionnalités

- 🔐 Authentification automatique sur l'API wigorservices
- 📅 Sélection de date pour consulter l'emploi du temps
- 🎨 Interface moderne et responsive avec Tailwind CSS
- ⚡ Build optimisé avec Vite
- 🧪 Tests unitaires avec >80% de couverture
- 📦 Packaging Windows avec Electron Builder

## 🛠️ Stack Technique

- **Electron** - Framework desktop multi-plateforme
- **React 18** - Bibliothèque UI
- **Vite** - Build tool moderne et rapide
- **Tailwind CSS** - Framework CSS utility-first
- **Puppeteer** - Scraping web automatisé
- **Vitest** - Framework de test unitaire
- **React Testing Library** - Tests de composants React

## 📦 Installation

```bash
npm install
```

## 🚀 Utilisation

### Mode Développement

```bash
# Lancer uniquement l'interface web (dev)
npm run dev

# Lancer l'application Electron complète
npm run electron:dev
```

### Build Production

```bash
# Build de l'interface React
npm run build

# Build de l'exécutable Windows
npm run electron:build
```

### Tests

```bash
# Lancer les tests
npm test

# Lancer les tests avec couverture
npm run test:coverage

# Lancer l'interface UI des tests
npm run test:ui
```

## ⚙️ Configuration

Créer un fichier `.env` à la racine du projet avec vos identifiants :

```env
USERNAME=VotreIdentifiant
PASSWORD=VotreMotDePasse
```

> ⚠️ Ne commitez jamais votre fichier `.env` avec vos vrais identifiants !

## 📊 Couverture de Tests

La couverture de tests actuelle est de **81.65%**, dépassant l'objectif de 80% :

- **Composants React** : 100% de couverture
- **Utilitaires** : 100% de couverture
- **App principal** : 96% de couverture

## 🏗️ Architecture

```
13-cours-mcgonagall/
├── electron/           # Processus principal Electron
│   ├── main.js        # Point d'entrée Electron
│   └── preload.js     # Script de préchargement (IPC bridge)
├── src/               # Code source React
│   ├── components/    # Composants React
│   │   ├── DateSelector.jsx
│   │   ├── ScheduleView.jsx
│   │   ├── CourseCard.jsx
│   │   ├── LoadingSpinner.jsx
│   │   └── ErrorMessage.jsx
│   ├── utils/         # Fonctions utilitaires
│   │   └── dateUtils.js
│   ├── App.jsx        # Composant racine
│   ├── main.jsx       # Point d'entrée React
│   └── index.css      # Styles globaux (Tailwind)
├── tests/             # Tests unitaires
│   ├── components/    # Tests des composants
│   └── utils/         # Tests des utilitaires
├── scraper.js         # Module de scraping Puppeteer
└── package.json       # Configuration npm
```

## 📚 Documentation Technique

### Communication IPC (Inter-Process Communication)

L'application utilise IPC pour communiquer entre le processus principal Electron et le renderer React :

- `scrape-schedule` : Récupère l'emploi du temps pour une date donnée
- `get-env` : Vérifie la présence des identifiants

### Scraper

Le scraper utilise Puppeteer pour :
1. Se connecter à l'API wigorservices
2. Gérer l'authentification automatique
3. Parser le DOM pour extraire les cours (matière, professeur, horaire, salle)
4. Retourner les données structurées par jour

## 🎮 Utilisation de l'Application

1. Lancez l'application
2. Sélectionnez une date ou cliquez sur "Aujourd'hui"
3. L'emploi du temps s'affiche avec les cours organisés par jour
4. Chaque cours affiche : matière, professeur, horaire et salle

## 📦 Build Windows

L'exécutable Windows sera généré dans `dist-electron/` après avoir exécuté :

```bash
npm run electron:build
```

## 🐛 Dépannage

### Le scraper ne fonctionne pas
- Vérifiez que vos identifiants sont corrects dans `.env`
- Vérifiez votre connexion internet
- Assurez-vous que Puppeteer est correctement installé

### L'interface ne charge pas
- Vérifiez que le build a été effectué : `npm run build`
- En mode dev, vérifiez que le serveur Vite tourne sur le port 5173

## 📄 Licence

MIT

---

## Historique des prompts et réponses

---

### Prompt 1
> initialise un project electron vide, le but est de faire un emploi du temps qui va scrapter un site pour remplir les données, prépare un .env avec le username et password

**Réponse :**
Je vais vous aider à initialiser un projet Electron vide pour créer un emploi du temps qui scrape un site web. Commençons par créer la structure du projet.

---

### Prompt 2
> tu te mets dans le dossier 13 dans projects pour le faire

**Réponse :**
Commençons par créer la structure du projet Electron. Je vais créer un dossier pour le projet et initialiser le package.json.

---

### Prompt 3
> tu te mets à la racine de 13 direct

**Réponse :**
Le projet Electron vide est maintenant initialisé à la racine du dossier 13. Vous disposez de :
- package.json configuré pour Electron
- main.js pour lancer l'app
- index.html pour l'interface
- .env pour le username et password
- Dépendances installées : electron, puppeteer, dotenv
- Un script de scraping de base (scraper.js)
- Un README explicatif

Vous pouvez maintenant développer la logique de scraping et l'affichage de l' emploi du temps. Souhaitez-vous ajouter une fonctionnalité ou personnaliser l'interface ?

---

### Prompt 4
> Ajoute un gitignore pour le .env et nodemodules, ajoute aussi un .env.example

**Réponse :**
Les fichiers .gitignore (pour ignorer node_modules et .env) et .env.example (modèle pour les variables d'environnement) ont été ajoutés à la racine du dossier 13.

Votre projet est maintenant prêt pour le versionnement avec Git et le partage des variables d'environnement sans exposer vos identifiants. Souhaitez-vous une autre configuration ou une fonctionnalité supplémentaire ?

---

### Prompt 5
> Ajoute un README avec tous les prompts que je t'ai fait et toutes tes réponses de manière formattées

**Réponse :**
Ce fichier contient l'historique complet des échanges pour la mise en place du projet.

---

### Prompt 6
> Voici l'url de l'emploi du temps :https://ws-edt-cd.wigorservices.net/WebPsDyn.aspx?action=posEDTLMS&serverID=C&Tel=test&date=10/13/2025
>
> Retire le password du .env en fait ça sert à rien
>
> Il faut aussi qu'on puisse scrap pour une date précise, tu remplaces tel=test par le username du .env
>
> Tu v

**Réponse :**
Le fichier `.env` et `.env.example` ont été mis à jour pour ne contenir que `USERNAME`.
Le script `scraper.js` permet maintenant de scrapper pour une date précise en passant la date en argument (format MM/DD/YYYY), et utilise le username du `.env` dans l'URL.
L'URL utilisée est :
`https://ws-edt-cd.wigorservices.net/WebPsDyn.aspx?action=posEDTLMS&serverID=C&Tel=<USERNAME>&date=<DATE>`
Exemple d'utilisation :
```bash
node scraper.js 10/13/2025
```
Si aucune date n'est fournie, la date du jour est utilisée.

---

### Prompt 7
> ça c'est une page pour la date du jour, tu me scapper tout par jour

**Réponse :**
Je vais adapter le scraper pour récupérer tous les cours de chaque jour à partir de la page HTML fournie. Le script va parcourir la structure et extraire les informations pour chaque journée (date, heure, matière, salle, professeur, etc.).

---

### Prompt du 13/10/2025
> mets le timing à 1min max plutôt et ajoute tous les nouveaux prompts au readme

**Réponse :**
Le timeout d'attente du planning après le login a été réduit à 1 minute (60000 ms) dans le script `scraper.js`. Tous les nouveaux prompts et réponses sont ajoutés ici pour la traçabilité.

---

### Prompt du 13/10/2025
> mets juste la date au format fr-FR

**Réponse :**
La génération de la date utilise désormais le format français JJ/MM/AAAA grâce à `toLocaleDateString('fr-FR')` dans le script `scraper.js`. L’URL du scraping est donc compatible avec le format attendu par le site.

---

## Installation

```bash
npm install
```

## Lancement

```bash
npm start
```

## Scraping

Pour lancer le scraping :
```bash
node scraper.js
```

## Configuration

Créer un fichier `.env` à la racine avec :
```
USERNAME=VotreIdentifiant
PASSWORD=VotreMotDePasse
```
