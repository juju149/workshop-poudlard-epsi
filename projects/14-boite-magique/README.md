# 🧪 La Boite Magique de Severus Rogue

**Challenge #14 - Cross-Platform Workshop Archive Tool**

Un outil cross-platform (Linux/Windows) développé avec CMake pour rassembler et archiver les sources et documents du Workshop Poudlard.

## 🎯 Objectif

Créer un binaire exécutable qui scanne récursivement un répertoire de workshop et collecte tous les fichiers sources et documents dans une archive organisée, tout en préservant la structure des répertoires.

## ✨ Fonctionnalités

- 🔍 **Scan récursif** : Parcourt tous les sous-répertoires
- 📁 **Filtrage par extension** : Collecte uniquement les types de fichiers souhaités
- 📊 **Statistiques** : Affiche le nombre de fichiers par type
- 📦 **Archivage** : Crée une copie organisée des fichiers collectés
- 🌍 **Cross-platform** : Fonctionne sur Linux et Windows
- 🚀 **Performance** : Utilise C++17 std::filesystem pour une gestion efficace des fichiers

## 🏗️ Architecture

```
14-boite-magique/
├── CMakeLists.txt          # Configuration CMake
├── README.md               # Cette documentation
├── include/
│   └── MagicBox.h         # Header de la classe principale
├── src/
│   ├── main.cpp           # Point d'entrée du programme
│   └── MagicBox.cpp       # Implémentation de la classe
├── build/                 # Répertoire de build (généré)
└── docs/
    └── USAGE.md          # Documentation utilisateur détaillée
```

## 📋 Prérequis

### Linux
```bash
sudo apt-get update
sudo apt-get install build-essential cmake g++
```

### Windows
- Visual Studio 2019 ou plus récent (avec C++ tools)
- CMake 3.15+
- Ou MinGW-w64 avec GCC

## 🔧 Compilation

### Linux

```bash
# Se placer dans le dossier du projet
cd 14-boite-magique

# Créer le répertoire de build
mkdir -p build
cd build

# Configurer avec CMake
cmake ..

# Compiler
cmake --build .

# Le binaire se trouve dans build/bin/magic-box
```

### Windows (Visual Studio)

```cmd
REM Se placer dans le dossier du projet
cd 14-boite-magique

REM Créer le répertoire de build
mkdir build
cd build

REM Configurer avec CMake
cmake ..

REM Compiler
cmake --build . --config Release

REM Le binaire se trouve dans build\bin\Release\magic-box.exe
```

### Windows (MinGW)

```bash
cd 14-boite-magique
mkdir build && cd build
cmake -G "MinGW Makefiles" ..
cmake --build .
```

## 🚀 Utilisation

### Utilisation basique

```bash
# Archiver tous les fichiers du répertoire courant
./magic-box

# Archiver depuis un répertoire spécifique
./magic-box -r /path/to/workshop

# Spécifier le répertoire de sortie
./magic-box -o ./my-archive
```

### Filtrage par extensions

```bash
# Collecter uniquement les fichiers C++ et headers
./magic-box -e .cpp,.h,.hpp

# Collecter les fichiers Markdown et Python
./magic-box -e .md,.py

# Collecter plusieurs types de fichiers
./magic-box -e .cpp,.h,.py,.md,.yml,.json
```

### Mode statistiques

```bash
# Afficher uniquement les statistiques sans créer d'archive
./magic-box -s

# Statistiques pour des extensions spécifiques
./magic-box -s -e .cpp,.h
```

### Exemples combinés

```bash
# Scanner le workshop et archiver uniquement le code source
./magic-box -r ~/workshop-poudlard -o ~/backup-code -e .cpp,.h,.py,.js

# Analyser les documents du workshop
./magic-box -r ~/workshop-poudlard -s -e .md,.pdf,.docx
```

## 📖 Options de ligne de commande

| Option | Description |
|--------|-------------|
| `-h, --help` | Affiche l'aide |
| `-r, --root <path>` | Répertoire racine à scanner (défaut: répertoire courant) |
| `-o, --output <path>` | Répertoire de sortie pour l'archive (défaut: ./workshop-archive) |
| `-e, --ext <extensions>` | Extensions de fichiers à inclure (séparées par des virgules) |
| `-s, --stats` | Mode statistiques uniquement (pas de création d'archive) |

## 🧪 Tests

### Test sur Linux

```bash
# Compiler
cd build
cmake --build .

# Tester avec le workshop complet
./bin/magic-box -r ../.. -o /tmp/test-archive -e .md,.cpp,.h,.py

# Vérifier les statistiques
./bin/magic-box -r ../.. -s
```

### Test sur Windows

```cmd
REM Compiler
cd build
cmake --build . --config Release

REM Tester avec le workshop complet
.\bin\Release\magic-box.exe -r ..\.. -o C:\temp\test-archive -e .md,.cpp,.h,.py

REM Vérifier les statistiques
.\bin\Release\magic-box.exe -r ..\.. -s
```

## 🎨 Exemple de sortie

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    🧪 LA BOITE MAGIQUE DE SEVERUS ROGUE 🧪                 ║
║                                                              ║
║    Cross-Platform Workshop Archive Tool                     ║
║    Poudlard à l'EPSI/WIS                                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

🎯 Configuration:
  Root path: /home/user/workshop
  Output path: ./workshop-archive
  Extensions: .cpp, .h, .md

🔍 Scanning workshop files...
✅ Found 42 files

📊 Workshop Statistics
=====================
Total files collected: 42

Files by type:
  .cpp: 15
  .h: 12
  .md: 15

📦 Creating archive at: ./workshop-archive
✅ Archive created successfully!
📂 Location: /home/user/workshop/workshop-archive

✨ Magic complete! ✨
```

## 🛠️ Technologies utilisées

- **Langage** : C++17
- **Build System** : CMake 3.15+
- **Standard Library** : std::filesystem (C++17)
- **Compatibilité** : Linux, Windows, macOS

## 📦 Livrables

✅ **Code source complet**
- Classes C++ modulaires et réutilisables
- Headers bien documentés
- Code commenté et structuré

✅ **CMakeLists.txt**
- Configuration cross-platform
- Support Linux/Windows/macOS
- Règles d'installation

✅ **Documentation**
- README.md complet
- Exemples d'utilisation
- Instructions de compilation

✅ **Binaire cross-platform**
- Exécutable compilable sur Linux et Windows
- Interface en ligne de commande intuitive

## 🚧 Améliorations possibles

- Ajout de la compression (ZIP, TAR.GZ)
- Support des exclusions (patterns .gitignore)
- Mode interactif avec menu
- Barre de progression pour les grandes collections
- Export des statistiques en JSON/CSV
- Interface graphique (Qt ou GTK)

## 👥 Auteurs

Développé pour le Workshop "Poudlard à l'EPSI/WIS"
Challenge #14 - La Boite Magique de Severus Rogue

## 📄 Licence

Ce projet est développé dans le cadre du Workshop EPSI/WIS 2025.

---

**Deadline:** 16/10/2025  
**Story Points:** 8  
**Copilots:** Frontend Copilot (lead), Documentation Copilot



---

## 🗒️ Historique des prompts utilisateur

Voici tous les prompts envoyés à GitHub Copilot durant le développement :

quand j'archive, c'est envoyé où ?
Okay alors maintenant on va push l'archive sur github
nan mais de manière automatique, tu vas ajouter une option à la CLI avec un lien github et tu prends mes credentials de git config
J'aimerais pouvoir l'envoyer dans un dossier spécifique sur mon repo github
si le dossier existe pas il va être créé ?
❌ Error: Failed to push to GitHub: filesystem error: in rename: Invalid argument ["./archive-magique/archives"] ["./archive-magique/archives/2025-10-14/archives"]
Ajoute une option pour push sur une branche choisie qui existe ou pas
/Users/tweenty/Desktop/workshop-poudlard-epsi/projects/14-boite-magique/src/MagicBox.cpp:145:16: error: out-of-line definition of 'pushToGitHub' does not match any declaration in 'MagicBox'
🚀 Pushing to GitHub...
⚠️  Push output: error: src refspec main does not match any
error: failed to push some refs to 'https://github.com/juju149/workshop-poudlard-epsi.git'
error: src refspec master does not match any
error: failed to push some refs to 'https://github.com/juju149/workshop-poudlard-epsi.git'
✅ Successfully pushed to GitHub!
🌐 View your archive at: https://github.com/juju149/workshop-poudlard-epsi.git
ajoute tous les prompts que je t'ai fait à la fin du readme
⚠️  Push output: error: src refspec ma-branche-speciale does not match any
error: failed to push some refs to 'https://github.com/juju149/workshop-poudlard-epsi.git'
Tu m'ajoutes l'historique des prompts au readme avec la solution

---

## 🏆 Solution CLI finale

La Boite Magique supporte désormais l’archivage, le push GitHub dans un dossier et sur une branche personnalisée :

```bash
./bin/magic-box -r <chemin_source> -o <chemin_archive> -e <extensions> \
  --github <url_repo> --github-folder <dossier_cible> --github-branch <nom_branche>
```

**Exemple complet** :

```bash
./bin/magic-box -r .. -o ./archive-magique -e .cpp,.h,.md \
  --github https://github.com/juju149/workshop-poudlard-epsi.git \
  --github-folder archives/2025-10-14 \
  --github-branch ma-branche-speciale
```

**Explications** :
- `--github` : URL du repo GitHub (ex : https://github.com/juju149/workshop-poudlard-epsi.git)
- `--github-folder` : dossier cible dans le repo (ex : archives/2025-10-14)
- `--github-branch` : branche cible (créée si elle n’existe pas)

Le programme :
1. Archive les fichiers dans le dossier local choisi
2. Place l’archive dans le dossier cible du repo
3. Crée/switch la branche demandée
4. Commit et push sur la branche et le dossier voulus

**Remarque** : Si le dossier ou la branche n’existent pas, ils sont créés automatiquement.