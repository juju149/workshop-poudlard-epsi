# 🧩 DÉFI 8: OÙ EST LA CHAMBRE DES SECRETS ?

## 🎯 Objectif

Créer avec **un script Blender (Python)** un **plan 3D de Poudlard**, dans lequel la **Chambre des Secrets** est clairement mise en évidence par un matériau lumineux et un label 3D. Le script génère automatiquement les murs, sols, portes et une animation de caméra turntable.

## 📦 Livrables

- ✅ `build_hogwarts_plan.py` → Script Blender complet et commenté
- ✅ `hogwarts_plan.blend` → Fichier Blender généré (créé après exécution)
- ✅ `renders/plan_turntable.mp4` → Animation du plan (10 secondes)
- ✅ `README.md` → Ce fichier d'instructions
- 🎁 Support pour objets décoratifs (bureaux, tableaux) extensible

## 🚀 Installation et Prérequis

### Prérequis
- **Blender 3.0+** (testé avec Blender 3.3 et supérieur)
- **Python 3.9+** (inclus avec Blender)
- Système: Linux, macOS ou Windows

### Installation de Blender

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install blender
```

#### macOS
```bash
brew install --cask blender
```

#### Windows
Télécharger depuis: https://www.blender.org/download/

## 🎮 Utilisation

### Méthode 1: Exécution en mode background (recommandé pour génération automatique)

```bash
cd projects/08-chambre-secrets-3d
blender --background --python build_hogwarts_plan.py
```

Cette commande:
1. Lance Blender en mode background (sans interface)
2. Exécute le script Python
3. Génère le fichier `hogwarts_plan.blend`
4. Le fichier peut ensuite être ouvert dans Blender pour le rendu

### Méthode 2: Exécution dans Blender GUI

1. Ouvrir Blender
2. Aller dans `Scripting` workspace
3. Ouvrir le fichier `build_hogwarts_plan.py`
4. Cliquer sur "Run Script" (▶️) ou `Alt+P`

### Génération de la vidéo d'animation

#### Option A: Depuis l'interface Blender
1. Ouvrir `hogwarts_plan.blend` dans Blender
2. Vérifier que la caméra est bien configurée (View > Cameras > Active Camera)
3. Aller dans `Render` > `Render Animation` (ou `Ctrl+F12`)
4. La vidéo sera générée dans `renders/plan_turntable.mp4`

#### Option B: En ligne de commande (batch rendering)
```bash
blender hogwarts_plan.blend --background --render-anim
```

## 🏗️ Architecture du Script

### Structure du code

```
build_hogwarts_plan.py
├── 1. CONFIGURATION & PARAMÈTRES GLOBAUX
│   └── Constantes (dimensions, couleurs, animation)
├── 2. INITIALISATION
│   └── initialize_scene() - Nettoie et configure la scène
├── 3. MATÉRIAUX
│   ├── create_material() - Crée matériaux standard ou émissifs
│   └── setup_materials() - Génère tous les matériaux
├── 4. GÉOMÉTRIE
│   ├── create_wall() - Génère un mur paramétrique
│   ├── create_floor() - Génère un sol
│   ├── create_door() - Génère une porte
│   ├── create_room() - Assemble une pièce complète
│   └── create_3d_text() - Crée du texte 3D
├── 5. PLAN DE POUDLARD
│   └── build_hogwarts_layout() - Construit le plan complet
├── 6. ÉCLAIRAGE
│   └── setup_lighting() - Configure lumières Sun et Area
├── 7. CAMÉRA ET ANIMATION
│   └── setup_camera_animation() - Animation turntable 360°
├── 8. RENDU
│   └── setup_render_settings() - Configure Eevee et export MP4
└── 9. MAIN
    └── main() - Orchestration du pipeline complet
```

### Paramètres configurables

Dans la section `CONFIGURATION & PARAMÈTRES GLOBAUX`, vous pouvez ajuster:

```python
# Dimensions
WALL_THICKNESS = 0.3      # Épaisseur des murs (mètres)
WALL_HEIGHT = 3.0         # Hauteur des murs (mètres)
DOOR_WIDTH = 1.0          # Largeur des portes
DOOR_HEIGHT = 2.2         # Hauteur des portes

# Animation
ANIMATION_FRAMES = 240    # Durée en frames (240 = 10s à 24fps)
CAMERA_RADIUS = 30.0      # Distance caméra du centre
CAMERA_HEIGHT = 20.0      # Hauteur de la caméra

# Couleurs (RGBA)
COLOR_CHAMBER = (0.0, 1.0, 0.3, 1.0)  # Vert lumineux pour la Chambre
```

## 🎨 Caractéristiques

### ✅ Critères de validation

- ✅ **Plan 3D entièrement généré par script** (pas de modélisation manuelle)
- ✅ **Bâtiment lisible** : murs, sols, portes bien distincts
- ✅ **Chambre des Secrets mise en évidence** :
  - Matériau lumineux vert (émission = 3.0)
  - Positionnée sous le sol principal (-4m)
  - Label 3D "Chambre des Secrets" en jaune lumineux
- ✅ **Caméra animée** : rotation 360° autour du plan (turntable)
- ✅ **Vidéo finale MP4** : 1920x1080, 24fps, 10 secondes
- ✅ **Script réutilisable** : peut être relancé dans une scène vide sans erreur
- 🎁 **Architecture extensible** pour ajout de mobilier (bonus)

### 📐 Plan de Poudlard (simplifié)

Le script génère un plan architectural comprenant:

- **Grande Salle** (centre) - 15x20m
- **4 Salles de classe** autour de la Grande Salle - 8x8m chacune
- **2 Couloirs** (Nord/Sud) - 10x4m
- **Bibliothèque** (Ouest) - 10x12m
- **Tour** (Est) - 6x6m
- **⭐ Chambre des Secrets** (sous la Grande Salle) - 10x10m
  - Positionnée 4m sous le niveau principal
  - Murs et sol en matériau vert lumineux
  - Label 3D flottant au-dessus

### 🎬 Animation

- **Type**: Turntable (rotation 360°)
- **Durée**: 10 secondes (240 frames à 24 FPS)
- **Caméra**: Position élevée (20m) avec vue plongeante
- **Interpolation**: Linéaire pour une rotation fluide

### 🎨 Style visuel

- **Style Blueprint** : couleurs sobres (gris/bleu)
- **Éclairage**: Sun light + Area light pour ambiance douce
- **Moteur de rendu**: Blender Eevee (temps réel, rapide)
- **Effets**: Bloom et soft shadows activés

## 📂 Structure des fichiers

```
08-chambre-secrets-3d/
├── build_hogwarts_plan.py    # Script principal
├── README.md                  # Ce fichier
├── requirements.txt           # Dépendances (optionnel)
├── .gitignore                 # Exclut fichiers temporaires
├── hogwarts_plan.blend        # Généré après exécution
├── renders/
│   └── plan_turntable.mp4     # Animation finale (généré)
├── props/                      # Objets décoratifs (bonus, vide initialement)
└── docs/
    └── screenshots/            # Captures d'écran (optionnel)
```

## 🔧 Dépannage

### Problème: "blender: command not found"
**Solution**: Installer Blender ou utiliser le chemin complet:
```bash
/path/to/blender --background --python build_hogwarts_plan.py
```

### Problème: "No module named 'bpy'"
**Solution**: Le script doit être exécuté via Blender, pas Python directement:
```bash
# ❌ Incorrect
python build_hogwarts_plan.py

# ✅ Correct
blender --background --python build_hogwarts_plan.py
```

### Problème: Le rendu est trop lent
**Solution**: Réduire la résolution dans `setup_render_settings()`:
```python
scene.render.resolution_x = 1280  # Au lieu de 1920
scene.render.resolution_y = 720   # Au lieu de 1080
```

### Problème: La Chambre des Secrets n'est pas visible
**Solution**: 
1. Ouvrir `hogwarts_plan.blend`
2. Vérifier les calques/collections
3. Ajuster `CAMERA_HEIGHT` pour une meilleure vue
4. La Chambre est 4m sous le sol, vérifier l'angle de caméra

## 🚀 Extensions possibles (Bonus)

### Ajouter du mobilier

Modifier `build_hogwarts_layout()` pour ajouter des objets:

```python
def create_desk(location, materials, collection):
    """Crée un bureau simple."""
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    desk = bpy.context.active_object
    desk.scale = (1.5, 0.8, 0.7)
    desk.data.materials.append(materials['Door'])
    collection.objects.link(desk)
    return desk

# Dans build_hogwarts_layout(), ajouter:
create_desk((-10, 10, 0.35), materials, collection)
```

### Ajouter des tableaux aux murs

```python
def create_painting(location, materials, collection):
    """Crée un tableau mural."""
    bpy.ops.mesh.primitive_plane_add(size=1, location=location)
    painting = bpy.context.active_object
    painting.scale = (1.0, 1.5, 1.0)
    painting.rotation_euler = (math.radians(90), 0, 0)
    # Ajouter texture/image ici
    collection.objects.link(painting)
    return painting
```

### Améliorer l'animation

Ajouter des keyframes pour variation de hauteur:
```python
# Dans setup_camera_animation()
camera.location.z = CAMERA_HEIGHT
camera.keyframe_insert(data_path="location", frame=1)

camera.location.z = CAMERA_HEIGHT + 5
camera.keyframe_insert(data_path="location", frame=ANIMATION_FRAMES // 2)

camera.location.z = CAMERA_HEIGHT
camera.keyframe_insert(data_path="location", frame=ANIMATION_FRAMES)
```

## 📚 Ressources

- [Blender Python API Documentation](https://docs.blender.org/api/current/)
- [Blender Scripting Tutorial](https://docs.blender.org/manual/en/latest/advanced/scripting/index.html)
- [Blender Eevee Rendering](https://docs.blender.org/manual/en/latest/render/eevee/index.html)

## 👤 Auteur

**Workshop Poudlard EPSI/WIS 2025-2026**  
Défi 8: Où est la Chambre des Secrets ?

## 📄 Licence

Usage éducatif uniquement - Workshop EPSI

---

> *"La Chambre des Secrets a été ouverte. Ennemis de l'héritier, prenez garde."*
> – Harry Potter et la Chambre des Secrets

✨ Bonne génération 3D ! ⚡
