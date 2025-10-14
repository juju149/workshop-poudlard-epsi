# Tests et Couverture de Code

Ce projet utilise Jest pour les tests unitaires avec une couverture de code complète pour les fichiers JSX et JS.

## 🧪 Configuration

### Dépendances installées

- **jest**: Framework de test
- **@testing-library/react**: Utilitaires pour tester les composants React
- **@testing-library/jest-dom**: Matchers personnalisés pour Jest
- **@testing-library/user-event**: Simulation d'événements utilisateur
- **babel-jest**: Transpilation du code pour Jest
- **@babel/preset-react**: Support JSX
- **jest-environment-jsdom**: Environnement DOM pour les tests
- **identity-obj-proxy**: Mock pour les imports CSS

## 📋 Scripts disponibles

```bash
# Lancer tous les tests
npm test

# Lancer les tests en mode watch (relance automatique)
npm run test:watch

# Lancer les tests avec rapport de couverture
npm run test:coverage

# Lancer les tests avec couverture et ouvrir le rapport HTML
npm run test:coverage:open
```

## 📊 Couverture de code

La couverture minimale requise est configurée dans `jest.config.cjs` :

- **Statements**: 76%
- **Branches**: 63%
- **Functions**: 76%
- **Lines**: 78%

### Fichiers couverts

- ✅ `src/App.jsx` - 100% de couverture
- ✅ `src/components/ScheduleGrid.jsx` - 87.67% de couverture
- ⚠️ `scraper.js` - 41.66% de couverture (mock Puppeteer)

## 🧪 Tests disponibles

### Tests du composant App (`src/__tests__/App.test.jsx`)

- Rendu du titre
- Structure CSS correcte
- Présence du composant ScheduleGrid
- Styles Tailwind appliqués

### Tests du composant ScheduleGrid (`src/__tests__/ScheduleGrid.test.jsx`)

- État de chargement initial
- Gestion des erreurs API
- Affichage des données d'emploi du temps
- Navigation entre les semaines
- Formatage des noms de professeurs
- Gestion des créneaux horaires
- Bouton de retry en cas d'erreur
- Affichage du nombre de cours
- Mode développement sans Electron

### Tests du Scraper (`src/__tests__/scraper.test.js`)

- Lancement du navigateur Puppeteer
- Navigation vers l'URL correcte
- Gestion de la page de connexion
- Extraction des données de planning
- Filtrage des jours sans cours
- Utilisation des variables d'environnement
- Fermeture du navigateur

## 🔧 Configuration Jest

Le fichier `jest.config.cjs` configure :

- **Environnement**: jsdom (simulation du navigateur)
- **Transform**: babel-jest pour JSX/JS
- **Coverage**: Répertoire `coverage/` avec rapports text, lcov et HTML
- **Setup**: Mock de l'API Electron pour les tests
- **Exclusions**: node_modules, coverage, fichiers de test

## 📁 Structure des tests

```
src/
├── __tests__/
│   ├── setup.js              # Configuration globale des tests
│   ├── App.test.jsx          # Tests du composant principal
│   ├── ScheduleGrid.test.jsx # Tests du composant grille
│   └── scraper.test.js       # Tests du scraper Puppeteer
```

## 🎯 Bonnes pratiques

1. **Isolation des tests** : Chaque test est indépendant
2. **Mocks** : L'API Electron et Puppeteer sont mockés
3. **waitFor** : Utilisation correcte pour les opérations asynchrones
4. **Coverage** : Tests couvrant les cas normaux et les erreurs
5. **Nommage** : Tests descriptifs et clairs

## 📈 Rapport de couverture

Après avoir lancé `npm run test:coverage`, vous pouvez consulter :

- **Terminal** : Résumé de la couverture
- **coverage/lcov-report/index.html** : Rapport HTML interactif détaillé

Le rapport HTML montre ligne par ligne quelles parties du code sont testées.

## 🚀 Améliorer la couverture

Pour améliorer la couverture du scraper (actuellement 41.66%), il faudrait :

1. Tester les chemins d'erreur (timeout, échec de login)
2. Tester l'extraction des données HTML plus en détail
3. Ajouter des tests d'intégration avec un vrai environnement Puppeteer

## 🐛 Debugging

Pour débugger un test spécifique :

```bash
# Lancer un seul fichier de test
npm test -- src/__tests__/App.test.jsx

# Lancer avec plus de détails
npm test -- --verbose

# Lancer en mode watch pour un fichier
npm test -- --watch src/__tests__/ScheduleGrid.test.jsx
```

## ✅ CI/CD

Les tests peuvent être intégrés dans une pipeline CI/CD :

```bash
# Exemple pour GitHub Actions
npm ci
npm run test:coverage
```

La commande échouera si les seuils de couverture ne sont pas atteints.

---

## 📝 Historique des prompts et consignes

### Couverture et robustesse

- **Demande initiale** : « Ajoute un test coverage de l'app avec jest pour du JSX et du js »
- **Objectif coverage** : « Je veux 80% de coverage »
- **Seuils configurés** :
  - branches: 80
  - functions: 80
  - lines: 80
  - statements: 80
- **Correction** : « fix les tests maintenant »
- **Fusion de créneaux** : Ajout de tests pour la fusion des cours consécutifs dans ScheduleGrid
- **Mock process.exit** : Ajout d’un mock global dans le setup pour éviter l’arrêt du process lors des tests du scraper
- **Robustesse du scraper** : Modification du code pour garantir la fermeture du navigateur en cas d’erreur
- **Tests edge cases** : Ajout de tests pour les cas limites (tableau incomplet, absence de données, erreur de login)
- **Conseil coverage** : Proposition d’améliorer la couverture des branches/fonctions si besoin

### Conseils et bonnes pratiques

- Toujours mocker les effets globaux (process.exit, window.electronAPI) pour éviter les effets de bord
- Utiliser des tests ciblés pour chaque branche complexe du code
- Documenter chaque étape et chaque consigne dans le README pour la traçabilité

---
