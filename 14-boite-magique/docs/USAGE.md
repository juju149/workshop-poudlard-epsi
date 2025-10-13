# 📚 Guide d'utilisation détaillé - Magic Box

## Table des matières

1. [Installation](#installation)
2. [Premiers pas](#premiers-pas)
3. [Cas d'usage avancés](#cas-dusage-avancés)
4. [Résolution de problèmes](#résolution-de-problèmes)
5. [FAQ](#faq)

## Installation

### Méthode 1 : Compilation depuis les sources

#### Sur Linux (Ubuntu/Debian)

```bash
# Installer les dépendances
sudo apt-get update
sudo apt-get install -y build-essential cmake git

# Cloner ou naviguer vers le projet
cd 14-boite-magique

# Compiler
mkdir -p build && cd build
cmake ..
make -j$(nproc)

# Tester l'installation
./bin/magic-box --help
```

#### Sur Windows avec Visual Studio

```powershell
# Prérequis : Visual Studio 2019+ avec "Desktop development with C++"
# Prérequis : CMake installé et dans le PATH

# Ouvrir PowerShell dans le dossier du projet
cd 14-boite-magique

# Créer et configurer le build
mkdir build
cd build
cmake ..

# Compiler
cmake --build . --config Release

# Tester
.\bin\Release\magic-box.exe --help
```

### Méthode 2 : Installation système (après compilation)

```bash
# Sur Linux
cd build
sudo cmake --install .

# Le binaire sera installé dans /usr/local/bin/magic-box
# Accessible depuis n'importe où
magic-box --help
```

## Premiers pas

### 1. Vérifier l'installation

```bash
magic-box --help
```

Vous devriez voir la bannière ASCII et la liste des options.

### 2. Scanner le répertoire courant

```bash
# Mode le plus simple
magic-box
```

Cela va :
- Scanner tous les fichiers dans le répertoire courant
- Créer un dossier `workshop-archive` avec les fichiers collectés
- Afficher les statistiques

### 3. Voir les statistiques sans archiver

```bash
magic-box --stats
```

Utile pour avoir une vue d'ensemble avant de créer une archive.

## Cas d'usage avancés

### Scénario 1 : Archiver un projet complet

```bash
# Collecter tous les fichiers sources d'un projet C++
magic-box \
    --root ~/mon-projet \
    --output ~/backups/projet-$(date +%Y%m%d) \
    --ext .cpp,.h,.hpp,.cc,.cxx
```

### Scénario 2 : Collecter la documentation

```bash
# Ne garder que la documentation
magic-box \
    --root ~/workshop \
    --output ~/docs-archive \
    --ext .md,.txt,.pdf,.docx
```

### Scénario 3 : Backup sélectif

```bash
# Archiver le code Python et les configs
magic-box \
    -r ~/projet-python \
    -o ~/backup-python \
    -e .py,.yml,.yaml,.json,.toml,.ini
```

### Scénario 4 : Analyse de projet

```bash
# Compter les fichiers par type dans un grand projet
magic-box -r ~/grand-projet -s -e .cpp,.h,.py,.js,.java
```

### Scénario 5 : Collecte multi-langage

```bash
# Workshop complet avec tous les langages
magic-box \
    -r ~/workshop-poudlard \
    -o ~/workshop-backup-complet \
    -e .cpp,.h,.py,.js,.ts,.java,.go,.rs,.md,.yml,.json
```

## Workflows recommandés

### Workflow 1 : Backup quotidien

Créer un script bash/batch pour automatiser :

**Linux (backup.sh):**
```bash
#!/bin/bash
DATE=$(date +%Y%m%d)
BACKUP_DIR=~/backups/workshop-$DATE

magic-box \
    --root ~/workshop \
    --output $BACKUP_DIR \
    --ext .cpp,.h,.py,.md

echo "Backup créé dans: $BACKUP_DIR"
```

**Windows (backup.bat):**
```batch
@echo off
set DATE=%date:~-4%%date:~3,2%%date:~0,2%
set BACKUP_DIR=C:\backups\workshop-%DATE%

magic-box.exe ^
    --root C:\workshop ^
    --output %BACKUP_DIR% ^
    --ext .cpp,.h,.py,.md

echo Backup cree dans: %BACKUP_DIR%
```

### Workflow 2 : Préparation de livrable

```bash
# 1. Analyser ce qui va être archivé
magic-box -r . -s -e .cpp,.h,.md,.yml

# 2. Créer l'archive
magic-box -r . -o ./livrable-challenge14 -e .cpp,.h,.md,.yml

# 3. Vérifier le contenu
ls -R ./livrable-challenge14
```

### Workflow 3 : Migration de projet

```bash
# Extraire uniquement le code source pour migration
magic-box \
    --root ./ancien-projet \
    --output ./nouveau-projet/sources \
    --ext .cpp,.h,.hpp

# Extraire la doc séparément
magic-box \
    --root ./ancien-projet \
    --output ./nouveau-projet/docs \
    --ext .md,.txt
```

## Résolution de problèmes

### Problème : "Root path does not exist"

**Cause :** Le chemin spécifié n'existe pas

**Solution :**
```bash
# Vérifier le chemin
ls /path/to/directory

# Utiliser un chemin absolu
magic-box -r /home/user/workshop
```

### Problème : Permission denied

**Cause :** Pas les droits pour lire certains fichiers ou créer l'archive

**Solution :**
```bash
# Sur Linux, donner les permissions
chmod +r -R /path/to/scan

# Ou utiliser un répertoire de sortie accessible
magic-box -o ~/mon-archive
```

### Problème : Compilation échoue sur Linux

**Cause :** std::filesystem pas trouvé

**Solution :**
```bash
# S'assurer d'avoir GCC 8+ ou Clang 9+
g++ --version

# Ou installer une version plus récente
sudo apt-get install g++-9
export CXX=g++-9
```

### Problème : Trop de fichiers collectés

**Cause :** Pas de filtrage par extension

**Solution :**
```bash
# Toujours spécifier des extensions
magic-box -e .cpp,.h,.md

# Utiliser --stats d'abord pour voir
magic-box -s
```

## FAQ

### Q : Le programme inclut-il les fichiers .git ?

**R :** Non, les répertoires `.git` et `build` sont automatiquement exclus.

### Q : Puis-je archiver vers un disque réseau ?

**R :** Oui, spécifiez simplement le chemin réseau :
```bash
# Linux
magic-box -o /mnt/nas/archive

# Windows
magic-box.exe -o \\serveur\partage\archive
```

### Q : Comment archiver plusieurs projets en une fois ?

**R :** Pointez vers le répertoire parent :
```bash
magic-box -r ~/tous-mes-projets -o ~/mega-archive
```

### Q : Les liens symboliques sont-ils suivis ?

**R :** Par défaut, oui. std::filesystem::recursive_directory_iterator suit les symlinks.

### Q : Peut-on créer une archive compressée (ZIP) ?

**R :** La version actuelle crée un dossier. Pour compresser :
```bash
# Linux
magic-box -o ./archive
tar -czf archive.tar.gz ./archive

# Windows
magic-box.exe -o .\archive
Compress-Archive -Path .\archive -DestinationPath archive.zip
```

### Q : Comment exclure certains dossiers ?

**R :** Les dossiers `.git` et `build` sont déjà exclus. Pour d'autres exclusions, filtrez par extension ou modifiez le code source.

### Q : Le programme fonctionne-t-il sur macOS ?

**R :** Oui ! Le CMakeLists.txt supporte macOS. Compilez avec les mêmes commandes que Linux.

### Q : Quelle est la taille maximale supportée ?

**R :** Limitée uniquement par la mémoire disponible et l'espace disque. Le programme peut gérer des milliers de fichiers.

## Astuces et bonnes pratiques

### 1. Toujours tester avec --stats d'abord

```bash
magic-box -r /path -s
```

Cela évite de créer des archives non désirées.

### 2. Utiliser des chemins absolus

```bash
# Mieux
magic-box -r /home/user/workshop -o /home/user/backup

# Que
magic-box -r ../workshop -o ./backup
```

### 3. Nommer les archives avec des dates

```bash
# Linux
magic-box -o ~/archives/workshop-$(date +%Y%m%d-%H%M%S)

# Windows PowerShell
$date = Get-Date -Format "yyyyMMdd-HHmmss"
magic-box.exe -o "C:\archives\workshop-$date"
```

### 4. Créer des alias

**Linux/macOS (~/.bashrc ou ~/.zshrc):**
```bash
alias backup-workshop='magic-box -r ~/workshop -o ~/backups/workshop-$(date +%Y%m%d)'
alias count-code='magic-box -s -e .cpp,.h,.py,.js'
```

**Windows PowerShell (Profile):**
```powershell
function Backup-Workshop {
    $date = Get-Date -Format "yyyyMMdd"
    magic-box.exe -r C:\workshop -o "C:\backups\workshop-$date"
}
```

### 5. Intégration dans les scripts de build

**CMake (post-build):**
```cmake
add_custom_command(TARGET magic-box POST_BUILD
    COMMAND magic-box -r ${CMAKE_SOURCE_DIR} -o ${CMAKE_BINARY_DIR}/archive -e .cpp,.h
    COMMENT "Creating source archive..."
)
```

## Support et contribution

Pour des questions ou suggestions :
- Consultez la documentation principale (README.md)
- Ouvrez une issue sur le dépôt Git
- Contactez l'équipe du workshop

---

**Bonne magie ! 🧪✨**
