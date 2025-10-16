# Prompt Copilot : Génération du glue Blender (JSON → Mesh)

## Contexte

Nous avons un fichier `floorplan.json` contenant la description structurée d'un plan d'étage avec :
- Des pièces (polygones en mètres)
- Des portes et fenêtres (segments avec dimensions)

Nous voulons générer un script Blender Python (`bpy`) qui crée un modèle 3D à partir de ces données.

## Prompt utilisé

```
Write a Blender Python (bpy) script that reads a `floorplan.json` file containing:
- rooms with polygons (list of [x,y] coordinates in meters)
- doors and windows (segments with start/end coordinates)

The script should:

1. Clear the scene and set units to METERS

2. For each room:
   - Create a mesh wall from the polygon with uniform thickness (configurable parameter)
   - Extrude the walls to a given height (configurable parameter)
   - Create a floor slab with 20cm thickness

3. For openings:
   - Create boolean cutter cubes for doors (height: 2.05m, at ground level)
   - Create boolean cutter cubes for windows (height: 1.10m, sill at 0.90m)
   - Apply boolean difference to cut the openings in walls

4. Organization:
   - Group objects into Collections per floor (e.g., "RDC", "R+1")
   - Name objects clearly (e.g., "SALLE_103_Walls", "SALLE_103_Floor")

5. Materials:
   - Create simple materials (wall: light beige, floor: gray, openings: wood/glass)

6. Cameras and lights:
   - Add a top-down orthographic camera for QA
   - Add a perspective camera with orbital animation
   - Add 2-3 lights for proper illumination

7. Export:
   - Save as .blend file
   - Export to .glb (glTF 2.0)

The script should be runnable in headless mode:
blender -b -P script.py -- input.json output.blend --wall_thickness 0.20 --wall_height 2.80

Use bmesh for mesh creation, mathutils for vectors, and proper error handling.
```

## Résultat attendu

Un script Python autonome qui :
- Lit le JSON
- Construit la géométrie 3D
- Configure la scène
- Exporte les fichiers

## Notes d'implémentation

- Utiliser `bmesh` pour la création de mesh procédurale
- Utiliser `mathutils.Vector` pour les calculs géométriques
- Appliquer les modificateurs (Solidify, Boolean) correctement
- Gérer les arguments de ligne de commande après le `--`

## Amélioration possibles

- Détecter automatiquement les portes coulissantes vs. battantes
- Générer des poignées de porte
- Ajouter des matériaux PBR réalistes
- Optimiser la topologie pour le rendu temps réel
- Générer des UV maps pour le texturage
