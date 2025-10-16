# Fichiers de sortie

Ce répertoire contient les fichiers générés par le pipeline plan2blend.

## Fichiers générés

### Modèles 3D
- **`*.blend`** : Fichier Blender natif (ouvrable avec Blender)
- **`*.glb`** : Export glTF 2.0 (visualisable dans navigateur web)

### Contrôle qualité
- **`overlays/`** : Visualisations de contrôle
  - `original_plan.png` : Plan source
  - `detected_edges.png` : Détection des contours
  - `overlay_preview.png` : Superposition plan/rendu
  - `metrics.txt` : Métriques de qualité

## Visualisation

### Blender
```bash
blender thalie.blend
```

### glTF (web)
Glisser-déposer le fichier `.glb` sur :
- https://gltf-viewer.donmccurdy.com/
- https://sandbox.babylonjs.com/
- https://threejs.org/editor/

### Overlays
Ouvrir les images PNG dans n'importe quel visualiseur d'images.

## Note

Ces fichiers sont générés automatiquement et ne devraient pas être versionnés (ils sont dans `.gitignore`).
