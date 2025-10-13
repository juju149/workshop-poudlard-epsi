# 🚀 Quick Start Guide - Magic Box

## Installation rapide

### Linux
```bash
cd 14-boite-magique
mkdir build && cd build
cmake ..
make
./bin/magic-box --help
```

### Windows
```cmd
cd 14-boite-magique
mkdir build && cd build
cmake ..
cmake --build . --config Release
.\bin\Release\magic-box.exe --help
```

## Commandes essentielles

```bash
# Afficher l'aide
magic-box --help

# Scanner le répertoire courant et afficher les stats
magic-box --stats

# Créer une archive du répertoire courant
magic-box

# Créer une archive d'un projet spécifique
magic-box -r /path/to/project -o /path/to/archive

# Filtrer par extensions (C++)
magic-box -e .cpp,.h,.hpp

# Filtrer par extensions (Python)
magic-box -e .py,.yml,.json

# Filtrer par extensions (Documentation)
magic-box -e .md,.txt,.pdf

# Stats uniquement pour des extensions spécifiques
magic-box -s -e .cpp,.h
```

## Exemples pratiques

### 1. Backup d'un projet C++
```bash
magic-box -r ~/mon-projet-cpp -o ~/backups/projet-cpp -e .cpp,.h,.hpp,.cmake
```

### 2. Collecter la documentation
```bash
magic-box -r ~/workshop -o ~/docs -e .md,.txt
```

### 3. Archiver un projet Python
```bash
magic-box -r ~/projet-python -o ~/archive-python -e .py,.yml,.json,.txt,.md
```

### 4. Analyser un grand projet
```bash
# D'abord voir les stats
magic-box -r ~/grand-projet -s

# Puis créer l'archive si OK
magic-box -r ~/grand-projet -o ~/archive
```

## Exclusions automatiques

Le programme exclut automatiquement :
- Dossiers `.git/`
- Dossiers `build/`

## Besoin d'aide ?

Consultez la documentation complète :
- `README.md` - Documentation principale
- `docs/USAGE.md` - Guide d'utilisation détaillé
