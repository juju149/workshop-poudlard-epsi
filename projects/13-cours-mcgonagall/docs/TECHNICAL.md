# 📖 Documentation Technique - Emploi du Temps McGonagall

## Table des Matières

1. [Architecture Globale](#architecture-globale)
2. [Technologies Utilisées](#technologies-utilisées)
3. [Structure des Données](#structure-des-données)
4. [Composants React](#composants-react)
5. [Tests](#tests)
6. [Build et Déploiement](#build-et-déploiement)

---

## Architecture Globale

L'application suit une architecture Electron classique avec deux processus :

### Processus Principal (Main Process)
- **Fichier** : `electron/main.js`
- **Responsabilités** :
  - Création et gestion de la fenêtre BrowserWindow
  - Gestion des événements IPC
  - Exécution du scraper Puppeteer
  - Gestion du cycle de vie de l'application

### Processus de Rendu (Renderer Process)
- **Fichier** : `src/main.jsx`
- **Responsabilités** :
  - Interface utilisateur React
  - Gestion de l'état de l'application
  - Communication avec le processus principal via IPC

### Pont de Communication (Preload Script)
- **Fichier** : `electron/preload.js`
- **Responsabilités** :
  - Exposition sécurisée des APIs IPC au renderer
  - Isolation du contexte entre Node.js et le navigateur

## Technologies Utilisées

### Frontend
- **React 18.2** : Bibliothèque UI moderne avec hooks
- **Vite 5.0** : Build tool ultra-rapide avec HMR
- **Tailwind CSS 3.4** : Framework utility-first pour styling

### Testing
- **Vitest 1.1** : Framework de test moderne
- **React Testing Library 14.1** : Tests centrés utilisateur
- **Coverage V8** : Rapports de couverture détaillés

### Scraping & Desktop
- **Puppeteer 24.24** : Contrôle headless Chrome
- **Electron 38.2** : Framework desktop cross-platform
- **Electron Builder 24.9** : Packaging Windows

## Structure des Données

### Schedule Data Structure

```typescript
interface Course {
  matiere: string;    // Nom de la matière
  prof: string;       // Nom du professeur
  heure: string;      // Horaire du cours
  salle: string;      // Numéro de salle
}

interface Day {
  date: string;       // Date formatée (ex: "Lundi 13 Oct")
  cours: Course[];    // Liste des cours du jour
}

type Schedule = Day[];
```

### IPC Response Structure

```typescript
interface ScraperResponse {
  success: boolean;
  data?: Schedule;
  error?: string;
}

interface EnvResponse {
  hasCredentials: boolean;
}
```

## Composants React

### App.jsx
**Composant racine de l'application**

**State Management:**
```javascript
const [schedule, setSchedule] = useState(null);
const [loading, setLoading] = useState(false);
const [error, setError] = useState(null);
const [hasCredentials, setHasCredentials] = useState(false);
```

### DateSelector.jsx
**Composant de sélection de date**

**Features:**
- Input manuel de date (format JJ/MM/AAAA)
- Bouton "Aujourd'hui" pour la date courante
- Validation côté client

### ScheduleView.jsx
**Composant d'affichage de l'emploi du temps**

**Features:**
- Affichage par jour avec header de date
- Grille responsive (1 col mobile, 2 cols tablette, 3 cols desktop)
- Gestion des jours sans cours

### CourseCard.jsx
**Composant carte de cours**

**Features:**
- Affichage conditionnel des informations
- Fallback pour données manquantes
- Icônes emoji pour meilleure UX

## Tests

### Configuration (vitest.config.js)

```javascript
{
  test: {
    coverage: {
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 80,
        statements: 80
      }
    }
  }
}
```

### Métriques de Couverture

| Fichier | Statements | Branches | Functions | Lines |
|---------|-----------|----------|-----------|-------|
| **Components** | 100% | 100% | 100% | 100% |
| **Utils** | 100% | 100% | 100% | 100% |
| **App** | 96% | 88% | 75% | 96% |
| **Global** | 81.65% | 92.3% | 88.23% | 81.65% |

## Build et Déploiement

### Build de Production

```bash
# 1. Build de l'interface React
npm run build

# 2. Package de l'application Electron
npm run electron:build
```

### Artefacts de Build

```
dist-electron/
├── win-unpacked/
└── Emploi du Temps McGonagall Setup.exe
```

### Optimisations

1. **Tree Shaking** : Vite élimine le code inutilisé
2. **Code Splitting** : Séparation automatique des chunks
3. **Minification** : Compression CSS et JS

## Sécurité

### Context Isolation
```javascript
webPreferences: {
  nodeIntegration: false,
  contextIsolation: true,
  preload: path.join(__dirname, 'preload.js')
}
```

### Credentials
- Variables d'environnement (`.env`)
- Jamais exposées au renderer process
- Utilisées uniquement dans le main process

## Performance

### Métriques

- **Bundle Size** : ~148 KB (gzipped: ~48 KB)
- **CSS Size** : ~12 KB (gzipped: ~3 KB)
- **Build Time** : ~1.3s
- **Test Time** : ~7s (59 tests)

---

**Dernière mise à jour** : Octobre 2025  
**Version** : 1.0.0
