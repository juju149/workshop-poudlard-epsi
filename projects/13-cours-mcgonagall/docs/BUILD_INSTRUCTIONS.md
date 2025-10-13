# 🔨 Instructions de Build - Emploi du Temps McGonagall

## 📋 Prérequis

- Node.js 18+ et npm 8+
- Git
- Windows 10+ (pour build de l'exécutable Windows)

## 🚀 Installation des Dépendances

```bash
cd projects/13-cours-mcgonagall
npm install
```

**Note:** Si Puppeteer ne peut pas télécharger Chrome (problème réseau), utilisez :
```bash
PUPPETEER_SKIP_DOWNLOAD=true npm install
```

## 🧪 Tests

### Lancer les Tests

```bash
# Tests en mode watch
npm test

# Tests avec rapport de couverture
npm run test:coverage

# Interface UI des tests
npm run test:ui
```

### Résultats Attendus

```
✓ tests/utils/dateUtils.test.js  (11 tests)
✓ tests/components/ScheduleView.test.jsx  (6 tests)
✓ tests/components/DateSelector.test.jsx  (6 tests)
✓ tests/components/CourseCard.test.jsx  (8 tests)
✓ tests/components/App.test.jsx  (8 tests)
✓ tests/components/ErrorMessage.test.jsx  (4 tests)
✓ tests/components/LoadingSpinner.test.jsx  (2 tests)
✓ tests/scraper.test.js  (10 tests)

Test Files  8 passed (8)
Tests  59 passed (59)
Coverage: 81.65%
```

## 🏗️ Build de l'Interface

### Development Build

```bash
# Démarrer le serveur de développement Vite
npm run dev
```

Ouvre automatiquement : http://localhost:5173

### Production Build

```bash
# Build optimisé pour production
npm run build
```

**Output:**
```
dist/
├── index.html
└── assets/
    ├── index-[hash].js   (~148 KB, ~48 KB gzippé)
    └── index-[hash].css  (~12 KB, ~3 KB gzippé)
```

## 📦 Build de l'Exécutable Windows

### Configuration Requise

Le fichier `.env` doit être présent avec les identifiants :

```env
USERNAME=VotreIdentifiant
PASSWORD=VotreMotDePasse
```

### Lancer le Build Electron

```bash
# 1. Build de l'interface React
npm run build

# 2. Package de l'application Electron
npm run electron:build
```

### Output Attendu

```
dist-electron/
├── win-unpacked/                              # Version décompressée
│   ├── Emploi du Temps McGonagall.exe
│   ├── resources/
│   │   └── app.asar
│   └── ...
└── Emploi du Temps McGonagall Setup.exe      # Installateur Windows
```

**Taille estimée:** ~150-200 MB (inclut Electron + Chromium)

## 🧰 Mode Développement Complet

Pour tester l'application complète en mode développement :

```bash
# Lance Vite + Electron avec hot reload
npm run electron:dev
```

Cela va :
1. Démarrer le serveur Vite (port 5173)
2. Attendre que le serveur soit prêt
3. Lancer Electron qui charge l'URL du serveur Vite
4. Hot reload automatique à chaque modification

## 🔍 Vérification Post-Build

### 1. Vérifier la Structure des Fichiers

```bash
tree dist/ -L 2
```

Doit contenir :
- ✅ `index.html`
- ✅ `assets/index-*.js`
- ✅ `assets/index-*.css`

### 2. Vérifier les Tailles de Bundle

```bash
ls -lh dist/assets/
```

Attendu :
- JS: ~145-150 KB
- CSS: ~11-12 KB

### 3. Tester le Build en Local

```bash
npm run preview
```

Ouvre le build de production sur http://localhost:4173

### 4. Vérifier l'Exécutable Windows

Sur Windows uniquement :

```bash
# Lancer l'exécutable
./dist-electron/win-unpacked/Emploi du Temps McGonagall.exe
```

## 🐛 Résolution de Problèmes

### Erreur: "Cannot find module electron"

```bash
npm install electron --save-dev
```

### Erreur: "Puppeteer download failed"

```bash
# Skip Puppeteer download (pas nécessaire pour tests)
PUPPETEER_SKIP_DOWNLOAD=true npm install
```

### Erreur: "Build failed - Out of memory"

```bash
# Augmenter la limite mémoire Node.js
export NODE_OPTIONS="--max-old-space-size=4096"
npm run build
```

### Tests échouent avec "Cannot find module"

```bash
# Nettoyer et réinstaller
rm -rf node_modules package-lock.json
npm install
```

### Electron ne se lance pas

```bash
# Vérifier que le build Vite est à jour
npm run build
npm run electron:dev
```

## 📊 Scripts npm Disponibles

| Script | Description |
|--------|-------------|
| `npm run dev` | Serveur Vite dev (HMR) |
| `npm run build` | Build production React |
| `npm run preview` | Preview du build |
| `npm run electron:dev` | Electron + Vite dev |
| `npm run electron:build` | Build exécutable Windows |
| `npm test` | Tests en mode watch |
| `npm run test:coverage` | Tests avec coverage |
| `npm run test:ui` | Interface UI des tests |

## 🚢 Checklist de Release

Avant de distribuer l'application :

- [ ] Tous les tests passent (`npm test`)
- [ ] Coverage > 80% (`npm run test:coverage`)
- [ ] Build Vite réussi (`npm run build`)
- [ ] Build Electron réussi (`npm run electron:build`)
- [ ] Exécutable testé sur Windows
- [ ] Documentation à jour
- [ ] Fichier `.env.example` fourni
- [ ] CHANGELOG mis à jour
- [ ] Version incrémentée dans `package.json`

## 📝 Notes

### Performance

- **Build Vite** : ~1-2 secondes
- **Build Electron** : ~30-60 secondes
- **Tests** : ~7 secondes

### Fichiers Exclus du Build

Les fichiers suivants sont exclus automatiquement (voir `.gitignore`) :

- `node_modules/`
- `dist/`
- `dist-electron/`
- `coverage/`
- `.env`

### Dépendances de Production

Seules les dépendances nécessaires sont packagées dans l'exécutable :

```json
{
  "dependencies": {
    "dotenv": "^17.2.3",
    "puppeteer": "^24.24.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  }
}
```

Les `devDependencies` ne sont pas incluses dans le package final.

## 🔗 Liens Utiles

- [Vite Documentation](https://vitejs.dev/)
- [Electron Documentation](https://www.electronjs.org/docs)
- [Electron Builder](https://www.electron.build/)
- [Vitest Documentation](https://vitest.dev/)
- [React Testing Library](https://testing-library.com/react)

---

**Dernière mise à jour:** Octobre 2025  
**Version:** 1.0.0
