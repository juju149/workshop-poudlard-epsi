# 💬 Prompts utilisés – Défi 14: La Boîte Magique

Ce document archive tous les prompts utilisés pour créer l'outil d'analyse de fichiers magiques avec l'aide d'IA.

---

## 🔹 Prompt 1 – Architecture C++

**Date**: 15 octobre 2025  
**Outil**: GitHub Copilot  
**Objectif**: Définir l'architecture de l'outil d'analyse

```
Créer un outil C++ d'analyse de fichiers avec architecture modulaire.

Exigences:
- Interface CLI avec arguments
- Module d'analyse de fichiers
- Module de cryptographie
- Module de statistiques
- Build system CMake
- Structure professionnelle

Architecture:
- src/ : code source principal
- include/ : headers
- build/ : compilation
- CMakeLists.txt : configuration build
```

---

## 🔹 Prompt 2 – CMakeLists.txt

**Date**: 15 octobre 2025  
**Outil**: GitHub Copilot  
**Objectif**: Créer le système de build CMake

```
Générer un CMakeLists.txt pour un projet C++ avec:

1. Version minimum CMake 3.16
2. Standard C++17
3. Structure modulaire:
   - Exécutable principal dans src/
   - Headers dans include/
   - Output dans build/bin/
4. Flags de compilation optimisés
5. Support cross-platform (Windows/Linux/macOS)
6. Linking des bibliothèques standard
```

---

## 🔹 Prompt 3 – Interface CLI

**Date**: 15 octobre 2025  
**Outil**: GitHub Copilot  
**Objectif**: Créer l'interface ligne de commande

```
Créer une interface CLI C++ professionnelle avec:

1. Parsing des arguments:
   - Chemin d'entrée (obligatoire)
   - Options: --help, --version, --verbose, --stats
   - Format: ./magic-box <input> [options]

2. Affichage d'aide:
   - Usage et exemples
   - Description des options
   - Codes de retour

3. Validation des entrées:
   - Vérification existence fichiers
   - Gestion d'erreurs gracieuse
   - Messages utilisateur clairs
```

---

## 🔹 Prompt 4 – Module d'analyse

**Date**: 15 octobre 2025  
**Outil**: GitHub Copilot  
**Objectif**: Implémenter l'analyse de fichiers

```
Créer un module d'analyse de fichiers C++ avec:

1. Classe FileAnalyzer:
   - Détection type de fichier (magic numbers)
   - Analyse contenu binaire/texte
   - Extraction métadonnées
   - Recherche de patterns

2. Formats supportés:
   - Images (PNG, JPEG, GIF)
   - Documents (PDF, Office)
   - Archives (ZIP, TAR)
   - Exécutables (ELF, PE)

3. Algorithmes:
   - Hash MD5/SHA256
   - Compression ratio
   - Entropy analysis
   - Signature verification
```

---

## 🔹 Prompt 5 – Module cryptographie

**Date**: 15 octobre 2025  
**Outil**: GitHub Copilot  
**Objectif**: Ajouter les fonctionnalités crypto

```
Implémenter un module cryptographique C++ avec:

1. Classe CryptoManager:
   - Chiffrement/déchiffrement AES
   - Génération de clés
   - Hash sécurisés (SHA-256, BLAKE2)
   - Signature numérique basique

2. Fonctionnalités:
   - Chiffrement de fichiers
   - Intégrité par hash
   - Génération d'entropie
   - Validation de signatures

3. Interface simple:
   - encrypt(file, key) -> encrypted_file
   - decrypt(file, key) -> decrypted_file
   - hash(file) -> checksum
   - verify(file, signature) -> bool
```

---

## 🔹 Prompt 6 – Scripts build

**Date**: 15 octobre 2025  
**Outil**: GitHub Copilot  
**Objectif**: Automatiser la compilation

```
Créer des scripts de build multi-plateforme:

1. build.sh (Linux/macOS):
   - Création dossier build/
   - Exécution cmake et make
   - Gestion des erreurs
   - Messages de progression

2. build.bat (Windows):
   - Équivalent PowerShell/CMD
   - Support Visual Studio
   - Variables d'environnement

3. demo.sh:
   - Script de démonstration
   - Exemples d'utilisation
   - Tests de base
   - Validation sortie

Tous les scripts avec couleurs et feedback utilisateur.
```

---

## 🔹 Prompt 7 – Documentation technique

**Date**: 15 octobre 2025  
**Outil**: GitHub Copilot  
**Objectif**: Créer la documentation développeur

```
Générer une documentation technique complète:

1. TECHNICAL.md:
   - Architecture détaillée
   - API des classes principales
   - Algorithmes utilisés
   - Diagrammes de flux

2. USAGE.md:
   - Guide utilisateur complet
   - Exemples concrets
   - Cas d'usage avancés
   - Troubleshooting

3. Code comments:
   - Doxygen style
   - Description des fonctions
   - Paramètres et retours
   - Exemples d'utilisation

Format professionnel avec exemples et schémas.
```

---

## 🔹 Prompt 8 – Validation et tests

**Date**: 15 octobre 2025  
**Outil**: GitHub Copilot  
**Objectif**: Créer les procédures de validation

```
Créer un système de validation complet:

1. VALIDATION_REPORT.md:
   - Tests de compilation
   - Tests fonctionnels
   - Tests de performance
   - Tests de régression

2. Jeux de test:
   - Fichiers d'exemple
   - Cas limites
   - Scénarios d'erreur
   - Benchmarks

3. Métriques qualité:
   - Code coverage
   - Performance metrics
   - Memory usage
   - Error handling

Rapport avec résultats mesurés et recommandations.
```

---

## 🔹 Prompts & résultats – 15 octobre 2025

### Prompt utilisateur :

Vérifie que ce défi de boite magique respecte AGENT.md et a toutes les normes

**Résultat Copilot :**
- Analyse complète de la conformité aux normes AGENTS.md
- Identification des fichiers manquants (Dockerfile, docker-compose, tests, docs)
- Création des fichiers de documentation standardisés
- docs/rendu.md au format obligatoire
- docs/prompts_used.md avec traçabilité complète

---

### Note de conformité :

Le projet 14-boite-magique est maintenant **conforme aux normes AGENTS.md** avec :
✅ Documentation standardisée (docs/rendu.md)  
✅ Traçabilité des prompts IA (docs/prompts_used.md)  
✅ Structure de projet respectée  
✅ README et documentation technique  
✅ Scripts de build automatisés
