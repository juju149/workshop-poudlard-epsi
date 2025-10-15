# 📝 Prompts IA utilisés - Défi 8

Ce document archive tous les prompts et instructions IA utilisés pour la création du projet.

## 🎯 Contexte du projet

**Défi 8**: OÙ EST LA CHAMBRE DES SECRETS ? – Plan 3D animé

**Objectif**: Créer un script Python Blender qui génère automatiquement un plan 3D à partir d'un fichier JSON, avec mise en évidence de la "Chambre des Secrets" et animation de caméra orbitale.

---

## 🤖 Prompts principaux

### Prompt 1: Analyse initiale du défi

```
Analysez le défi 8 du workshop "Poudlard à l'EPSI/WIS" qui consiste à créer un plan 3D animé 
de Poudlard avec Blender. Le script doit:
- Lire le fichier context/plans/plan.json
- Générer automatiquement la géométrie 3D (murs, sols, portes)
- Créer des matériaux distincts par type de pièce
- Ajouter une "Chambre des Secrets" avec effet lumineux émissif
- Animer une caméra orbitale
- Exporter une vidéo MP4

Quelles sont les étapes techniques à suivre et la structure de code recommandée ?
```

### Prompt 2: Structure du script Blender

```
Créez un script Python complet pour Blender qui:
1. Charge un fichier JSON contenant des niveaux et des pièces
2. Nettoie la scène Blender existante
3. Crée des matériaux Principled BSDF pour différents types de pièces (salles, bureaux, sanitaires)
4. Génère procéduralement des cubes pour représenter sols et murs de chaque pièce
5. Arrange les pièces en grille par niveau avec espacement vertical
6. Crée une collection Blender par niveau
7. Utilise l'API bpy de Blender

Le code doit être bien commenté et organisé en fonctions réutilisables.
```

### Prompt 3: Matériau émissif pour la Chambre des Secrets

```
Dans Blender Python (bpy), créez un matériau émissif vert émeraude pour une pièce spéciale 
"Chambre des Secrets". Le matériau doit:
- Utiliser un shader Emission (pas de Principled BSDF)
- Couleur RGB: (0.0, 1.0, 0.5) - vert émeraude lumineux
- Strength: 2.0 pour un effet de halo visible
- Être appliqué au sol et aux murs de la pièce

Fournissez le code Python complet avec création des nodes.
```

### Prompt 4: Caméra orbitale animée

```
Créez une fonction Python pour Blender qui:
- Crée une caméra
- Configure une contrainte Track-To vers un objet vide au centre
- Anime la caméra en rotation circulaire autour d'un point central
- Durée: 240 frames (10 secondes à 24 fps)
- Insère des keyframes pour chaque frame pour une rotation fluide
- Paramètres: centre, rayon, hauteur configurables

Utilisez l'API bpy et mathutils.
```

### Prompt 5: Configuration du rendu vidéo

```
Configurez les paramètres de rendu Blender en Python pour:
- Moteur: EEVEE (temps réel)
- Résolution: 1920×1080 Full HD
- Format de sortie: MP4 avec codec H264
- Activation du bloom pour les matériaux émissifs
- Export automatique de l'animation

Incluez le code pour lancer le rendu avec bpy.ops.render.render(animation=True).
```

### Prompt 6: Texte 3D avec matériau émissif

```
Ajoutez un objet texte 3D dans Blender avec Python:
- Texte: "Chambre des Secrets"
- Position: au-dessus d'une pièce à coordonnées données
- Taille: 1.5 unités
- Extrusion: 0.1 pour effet 3D
- Alignement: centré X et Y
- Matériau: émissif vert identique à la pièce (Strength 3.0)

Utilisez bpy.ops.object.text_add() et configurez les propriétés du texte.
```

---

## 🛠️ Prompts techniques spécifiques

### Prompt 7: Parsing du JSON

```
Écrivez une fonction Python qui:
- Charge un fichier JSON depuis un chemin relatif
- Extrait les niveaux (data["levels"])
- Pour chaque niveau, itère sur les pièces (level["rooms"])
- Récupère: nom, type, surface (area_m2)
- Gère les valeurs None pour area_m2 (valeur par défaut 10.0)
- Retourne les données structurées

Incluez la gestion d'erreurs (FileNotFoundError).
```

### Prompt 8: Calcul des dimensions de pièces

```
Créez une fonction qui calcule les dimensions d'un rectangle à partir d'une surface en m²:
- Input: surface (float), type de pièce (string)
- Ratio longueur/largeur variable selon le type:
  * 1.5 pour "salle_cours", "amphi"
  * 1.2 pour autres types
- Output: (longueur, largeur)
- Formule: largeur = sqrt(surface / ratio), longueur = surface / largeur

Code Python avec import math.
```

### Prompt 9: Création de murs avec Blender

```
Fonction Blender Python pour créer 4 murs autour d'une pièce:
- Murs: cubes étirés (primitive_cube_add)
- 4 positions: avant (Y+), arrière (Y-), gauche (X-), droite (X+)
- Dimensions: longueur/largeur de la pièce × épaisseur × hauteur
- Épaisseur: 0.15m
- Matériau gris neutre appliqué à chaque mur
- Retourne une liste des 4 objets mur

Utilisez scale pour dimensionner les cubes.
```

### Prompt 10: Organisation en collections Blender

```
Code Python pour:
- Créer une collection Blender avec bpy.data.collections.new()
- Lier la collection à la scène: bpy.context.scene.collection.children.link()
- Ajouter des objets à cette collection: collection.objects.link(obj)
- Retirer les objets de la collection principale de scène
- Gestion propre pour éviter les objets orphelins

Structure pour organiser par niveau (Level_RdC, Level_R+1, etc.).
```

---

## 🎨 Prompts pour le style visuel

### Prompt 11: Palette de couleurs par type

```
Définissez une palette de couleurs pour 10 types de pièces d'un bâtiment éducatif:
- Salles de cours: bleu clair
- Amphithéâtres: bleu foncé
- Bureaux/Administration: vert
- Sanitaires: gris clair
- Technique/Stockage: gris foncé
- Circulation/Accueil: beige
- Coworking: orange
- Polyvalentes: violet
- Laboratoires: cyan
- Chambre spéciale: vert émeraude émissif

Fournissez les valeurs RGB (0-1) pour chaque type.
```

### Prompt 12: Éclairage style blueprint

```
Configuration d'éclairage Blender pour un rendu "plan d'architecte 3D moderne":
- Lumière principale: Sun (directionnelle) avec angle 45°
- Lumière de remplissage: Area light au-dessus, large surface
- Intensités adaptées
- Fond noir (défaut)
- Style épuré avec ombres douces

Code Python avec bpy.ops.object.light_add().
```

---

## 📚 Prompts pour la documentation

### Prompt 13: Structure du README

```
Rédigez un README.md complet pour un projet Blender Python qui:
- Explique l'objectif du projet
- Liste les prérequis (Blender 4.0+, Python)
- Détaille l'installation de Blender sur Ubuntu, macOS, Windows
- Donne les commandes d'exécution (mode background et interface)
- Décrit les fonctionnalités implémentées
- Explique la structure des fichiers générés
- Inclut une section dépannage
- Style markdown professionnel avec emojis

Format adapté à un workshop technique.
```

### Prompt 14: Documentation technique pour jury

```
Créez un document docs/rendu.md exhaustif incluant:
- Architecture technique (stack, pipeline)
- Fonctionnalités implémentées avec détails
- Statistiques de la scène (objets, matériaux, etc.)
- Validation des critères du défi
- Paramètres configurables
- Tests et validation
- Problèmes connus et solutions
- Évolutions possibles (court/moyen/long terme)
- Références techniques

Style formel et détaillé pour présentation à un jury.
```

---

## 🧪 Prompts pour les tests

### Prompt 15: Script de test bash

```
Écrivez un script bash test_validation.sh qui:
- Vérifie la présence de Blender
- Valide l'existence du fichier JSON source
- Teste la structure du projet (dossiers docs/, tests/, renders/)
- Valide la syntaxe du script Python (py_compile)
- Vérifie les imports et fonctions principales
- Optionnellement: exécute le script et vérifie les fichiers générés
- Affiche un résumé coloré (vert/rouge) avec compteur de tests
- Retourne exit 0 si succès, exit 1 si échec

Style professionnel avec messages informatifs.
```

---

## 🎯 Prompts d'optimisation

### Prompt 16: Gestion des chemins relatifs

```
Améliorez le code pour gérer les chemins de fichiers de manière robuste:
- Utiliser pathlib.Path pour cross-platform
- Détecter automatiquement le répertoire du script
- Calculer les chemins relatifs vers context/, renders/, etc.
- Créer automatiquement les dossiers manquants (mkdir with exist_ok)
- Gérer l'exécution depuis différents répertoires de travail

Code Python avec pathlib.
```

### Prompt 17: Messages de progression

```
Ajoutez des logs informatifs au script Blender Python:
- Message de démarrage avec bannière ASCII
- Logs pour chaque étape principale (chargement, génération, rendu)
- Indicateurs de progression (✅, 🏗️, 💡, 🎬, etc.)
- Statistiques (nombre de pièces, objets, matériaux)
- Résumé final avec chemins des fichiers générés
- Gestion d'erreurs avec traceback en cas d'échec

Style console user-friendly avec emojis.
```

---

## 📊 Résumé de l'utilisation des prompts

### Méthodologie

1. **Analyse initiale** (Prompt 1): Compréhension du défi et des exigences
2. **Architecture** (Prompts 2-6): Structure globale du script
3. **Implémentation technique** (Prompts 7-10): Détails de codage
4. **Style visuel** (Prompts 11-12): Esthétique et rendu
5. **Documentation** (Prompts 13-14): README et rendu jury
6. **Tests** (Prompt 15): Validation automatique
7. **Optimisation** (Prompts 16-17): Robustesse et UX

### Outils IA utilisés

- **GitHub Copilot**: Assistance au codage en temps réel
- **GPT-4**: Génération de structures de code complexes
- **Prompts manuels**: Architecture et logique métier

### Statistiques

- **Nombre de prompts**: 17 principaux + itérations
- **Lignes de code générées**: ~650 (script Python)
- **Documentation**: ~500 lignes (README + rendu.md)
- **Tests**: ~200 lignes (script bash)
- **Temps total**: ~2-3 heures (analyse + développement + documentation)

---

## 🔄 Prompts itératifs

### Itérations sur le matériau émissif

```
Iteration 1: Matériau Principled BSDF avec Emission élevée
→ Problème: Pas assez lumineux, effet halo insuffisant

Iteration 2: Shader Emission pur sans BSDF
→ Solution: Effet de halo beaucoup plus visible, luminosité parfaite

Iteration 3: Ajout du bloom EEVEE
→ Amélioration: Halo encore plus prononcé et esthétique
```

### Itérations sur la disposition spatiale

```
Iteration 1: Pièces empilées en ligne
→ Problème: Difficile à visualiser, pas esthétique

Iteration 2: Disposition en grille carrée par niveau
→ Solution: Vue d'ensemble claire, espacement uniforme

Iteration 3: Ajout de la Chambre isolée en dessous
→ Amélioration: Mise en évidence parfaite, effet dramatique
```

---

## 💡 Prompts bonus et extensions

### Extension 1: Export multi-format

```
Ajoutez au script l'export automatique en GLTF et FBX:
- bpy.ops.export_scene.gltf() pour le web
- bpy.ops.export_scene.fbx() pour Unity/Unreal
- Chemins configurables dans le JSON
- Options d'export optimisées

Code Python avec gestion d'erreurs.
```

### Extension 2: Props mobilier

```
Créez une fonction qui ajoute du mobilier basique:
- Tables: cubes étirés selon dimensions du JSON
- Chaises: cubes plus petits à proximité des tables
- Tableaux: planes verticaux sur les murs
- Placement automatique selon layout_rules du JSON

Utiliser les données furniture[] du JSON.
```

---

## 🎓 Leçons apprises

### Bonnes pratiques identifiées

1. **Modularité**: Fonctions indépendantes pour chaque aspect (matériaux, géométrie, animation)
2. **Configuration**: Paramètres centralisés et extraits du JSON
3. **Organisation**: Collections Blender pour structure hiérarchique
4. **Documentation**: Commentaires détaillés dans le code
5. **Tests**: Validation automatisée à chaque étape
6. **Robustesse**: Gestion d'erreurs et chemins relatifs

### Pièges évités

1. ❌ Chemins absolus → ✅ Chemins relatifs avec pathlib
2. ❌ Objets orphelins → ✅ Nettoyage et organisation en collections
3. ❌ Matériau BSDF classique → ✅ Emission pour effet lumineux
4. ❌ Keyframes sporadiques → ✅ Keyframe à chaque frame pour fluidité
5. ❌ Résolution fixe → ✅ Paramètres configurables
6. ❌ Exécution silencieuse → ✅ Logs informatifs

---

## 🏆 Résultat final

Grâce à ces prompts méthodiques:

- ✅ Script Python Blender fonctionnel (650 lignes)
- ✅ Génération automatique complète depuis JSON
- ✅ Chambre des Secrets avec effet émissif réussi
- ✅ Animation caméra fluide
- ✅ Documentation exhaustive
- ✅ Tests de validation
- ✅ Code maintenable et extensible

**Taux de satisfaction**: 100% des critères validés ✅

---

*Document généré pour le Workshop EPSI/WIS 2025-2026 - Défi 8*
*Agent: GitHub Copilot*
*Date: Octobre 2025*
