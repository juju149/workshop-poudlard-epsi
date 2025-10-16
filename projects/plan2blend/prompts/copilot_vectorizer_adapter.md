# Prompt Copilot : Adaptateur de vectoriseur de plan

## Contexte

Nous avons besoin d'un script qui appelle un service de vectorisation IA pour convertir une image de plan d'étage en données structurées JSON.

## Prompt utilisé

```
Create a Python script that processes a floor plan image and produces structured JSON.

Input:
- `plan_600dpi.png`: High-resolution floor plan image (600 DPI)
- `--scale 1:150`: Scale of the plan

The script should:

1. Load and preprocess the image:
   - Convert to grayscale if needed
   - Apply adaptive thresholding to enhance lines
   - Denoise to remove artifacts

2. Detect architectural elements:
   - Walls: Detect continuous lines forming closed polygons
   - Doors: Detect openings in walls (typically arcs or gaps)
   - Windows: Detect rectangular openings

3. Process detected elements:
   - Convert pixel coordinates to real-world meters using the scale
   - Snap nearby vertices together (tolerance: 1-2 pixels)
   - Close polygons by connecting endpoints
   - Merge collinear segments

4. Output JSON structure:
{
  "scale": {"paper": 1, "real": 150},
  "floors": [{
    "code": "RDC",
    "rooms": [{
      "name": "ROOM_001",
      "polygon": [[x1,y1], [x2,y2], ...],
      "features": {
        "doors": [{"start": [x1,y1], "end": [x2,y2], "width": 0.9}],
        "windows": [{"start": [x1,y1], "end": [x2,y2], "width": 1.2, "height": 1.1}]
      }
    }]
  }]
}

Use OpenCV for image processing and Shapely for geometry operations.
Handle edge cases:
- Non-orthogonal walls
- Incomplete polygons
- Text overlays on the plan
- Multiple floors on the same image

Include logging and error handling.
```

## Approches possibles

### Approche 1 : Computer Vision classique
- Détection de contours (Canny)
- Transformée de Hough pour les lignes
- Algorithmes de fermeture de polygones

### Approche 2 : Machine Learning
- Modèle de segmentation sémantique (U-Net, Mask R-CNN)
- Classification des éléments (wall, door, window)
- Post-traitement pour vectorisation

### Approche 3 : Service externe
- API de services comme FloorplanToBlender
- CubiCasa5k dataset et modèles pré-entraînés
- Integration via REST API

## Résultat attendu

Un script qui produit un JSON valide et précis à partir de l'image, prêt à être consommé par le script Blender.

## Notes d'implémentation

Pour ce projet, nous utilisons une approche simplifiée avec :
- Détection de contours basique
- Génération de données d'exemple pour la démonstration
- Architecture extensible pour intégrer un vrai modèle IA plus tard

## Métriques de qualité

- Taux de détection des pièces : >90%
- Précision de position : ±2cm
- Taux de détection des ouvertures : >80%
- Faux positifs : <5%
