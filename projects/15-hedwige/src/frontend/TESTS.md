# Tests - Frontend Hedwige

Ce document explique l'organisation des tests dans le projet frontend Hedwige.

## Organisation des tests

### Tests Unitaires
- **Emplacement** : `src/**/*.{test,spec}.{js,jsx,ts,tsx}`
- **Configuration** : `vitest.unit.config.js`
- **Script** : `npm run test-unitaire`
- **Script en mode watch** : `npm run test-unitaire:watch`

Les tests unitaires couvrent les composants individuels et leurs fonctionnalités spécifiques :
- `src/pages/__tests__/` : Tests des pages (LoginPage, MailboxPage, ComposePage)
- `src/components/__tests__/` : Tests des composants (EmailList, EmailDetail)

### Tests d'Intégration
- **Emplacement** : `tests/integration/**/*.{test,spec}.{js,jsx,ts,tsx}`
- **Configuration** : `vitest.integration.config.js`
- **Script** : `npm run test-integration`
- **Script en mode watch** : `npm run test-integration:watch`

Les tests d'intégration vérifient les interactions entre plusieurs composants et le flux complet de l'application :
- `tests/integration/login-flow.test.jsx` : Test du flux de connexion utilisateur

## Scripts disponibles

```bash
# Tests unitaires
npm run test-unitaire          # Exécute les tests unitaires avec couverture
npm run test-unitaire:watch    # Exécute les tests unitaires en mode watch

# Tests d'intégration
npm run test-integration       # Exécute les tests d'intégration
npm run test-integration:watch # Exécute les tests d'intégration en mode watch

# Tests globaux (legacy)
npm run test                   # Exécute tous les tests (unitaires + intégration)
npm run test:watch            # Exécute tous les tests en mode watch
```

## Configuration des tests

### Setup global
Le fichier `tests/setup.js` contient la configuration globale pour tous les tests :
- Configuration de `@testing-library/jest-dom`
- Mocks globaux (console, variables d'environnement)
- Importation de Vitest

### Configurations spécifiques

#### Tests unitaires (`vitest.unit.config.js`)
- Inclut : `src/**/*.{test,spec}.{js,jsx,ts,tsx}`
- Exclut : `tests/integration/**`
- Couverture de code activée

#### Tests d'intégration (`vitest.integration.config.js`)
- Inclut : `tests/integration/**/*.{test,spec}.{js,jsx,ts,tsx}`
- Timeout prolongé (10s) pour les interactions complexes
- Couverture de code activée

## Bonnes pratiques

### Tests unitaires
- Testent un seul composant à la fois
- Mockent les dépendances externes
- Utilisent des snapshots pour les tests de rendu
- Vérifient les interactions utilisateur simples

### Tests d'intégration
- Testent les interactions entre composants
- Vérifient les flux complets (ex: connexion → boîte mail)
- Mockent les appels API
- Testent les cas d'erreur et les cas de succès

### Structure des tests d'intégration
```javascript
describe('Tests d\'intégration - [Nom du flux]', () => {
  beforeEach(() => {
    // Configuration des mocks
  });

  it('teste le cas de succès', async () => {
    // Rendu du composant
    // Interactions utilisateur
    // Vérifications
  });

  it('teste le cas d\'erreur', async () => {
    // Configuration d'erreur
    // Interactions utilisateur
    // Vérifications d'erreur
  });
});
```

## Coverage

La couverture de code est générée pour les deux types de tests :
- **Format** : HTML, JSON, Text
- **Répertoire de sortie** : `coverage/`
- **Exclusions** : `node_modules/`, `tests/setup.js`, `*.config.js`