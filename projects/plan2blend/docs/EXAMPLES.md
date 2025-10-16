# Exemples d'utilisation — plan2blend

## Exemple 1 : Pipeline complet avec données d'exemple

```bash
# 1. Générer un floorplan JSON d'exemple
python scripts/10_floorplan_vectorizer.py \
  --image data/work/plan_600dpi.png \
  --scale 1:150 \
  --out data/work/floorplan.json \
  --sample

# 2. Générer le modèle Blender
blender -b -P scripts/20_json_to_blender.py \
  -- data/work/floorplan.json build/out/example.blend \
  --wall_thickness 0.20 --wall_height 2.80

# 3. Ouvrir dans Blender (interface graphique)
blender build/out/example.blend
```

## Exemple 2 : À partir d'un PDF réel

```bash
# 1. Convertir le PDF en image
python scripts/00_export_pdf_to_png.py \
  --pdf data/input/mon_plan.pdf \
  --out data/work/plan_600dpi.png \
  --dpi 600

# 2. Vectoriser (utilise des données d'exemple pour l'instant)
python scripts/10_floorplan_vectorizer.py \
  --image data/work/plan_600dpi.png \
  --scale 1:100 \
  --out data/work/floorplan.json \
  --sample

# 3. Éditer le JSON manuellement si nécessaire
# Ouvrir data/work/floorplan.json et ajuster les coordonnées

# 4. Générer le modèle
blender -b -P scripts/20_json_to_blender.py \
  -- data/work/floorplan.json build/out/mon_batiment.blend

# 5. Générer les overlays de contrôle
python scripts/30_quality_overlays.py \
  --plan data/work/plan_600dpi.png \
  --blend build/out/mon_batiment.blend \
  --out build/out/overlays
```

## Exemple 3 : Personnalisation des dimensions

```bash
# Bureaux avec plafonds hauts
blender -b -P scripts/20_json_to_blender.py \
  -- data/work/floorplan.json build/out/bureaux.blend \
  --wall_thickness 0.25 --wall_height 3.20

# Habitation avec murs légers
blender -b -P scripts/20_json_to_blender.py \
  -- data/work/floorplan.json build/out/maison.blend \
  --wall_thickness 0.15 --wall_height 2.50
```

## Exemple 4 : Édition manuelle du JSON

Créer un fichier `custom_plan.json` :

```json
{
  "scale": {
    "paper": 1,
    "real": 100
  },
  "floors": [
    {
      "code": "RDC",
      "rooms": [
        {
          "name": "SALON",
          "polygon": [
            [0, 0], [7, 0], [7, 5], [0, 5]
          ],
          "features": {
            "doors": [
              {"start": [3, 0], "end": [4, 0], "width": 1.0}
            ],
            "windows": [
              {"start": [0, 2], "end": [0, 3], "width": 1.0, "height": 1.2}
            ]
          }
        },
        {
          "name": "CUISINE",
          "polygon": [
            [7, 0], [12, 0], [12, 5], [7, 5]
          ],
          "features": {
            "doors": [
              {"start": [7, 2], "end": [7, 3], "width": 1.0}
            ],
            "windows": [
              {"start": [12, 1], "end": [12, 3], "width": 2.0, "height": 1.2}
            ]
          }
        }
      ]
    }
  ]
}
```

Puis générer :

```bash
blender -b -P scripts/20_json_to_blender.py \
  -- custom_plan.json build/out/custom.blend
```

## Exemple 5 : Pipeline Docker

```bash
# Build les images
docker compose -f docker/docker-compose.yml build

# Exécuter le pipeline complet
docker compose -f docker/docker-compose.yml up pipeline

# Ou étape par étape
docker compose -f docker/docker-compose.yml up vectorizer
docker compose -f docker/docker-compose.yml run blender \
  -b -P /app/scripts/20_json_to_blender.py -- \
  /app/data/work/floorplan.json /app/build/out/thalie.blend
```

## Exemple 6 : Batch processing

Pour traiter plusieurs plans :

```bash
#!/bin/bash
# process_plans.sh

for pdf in data/input/*.pdf; do
    name=$(basename "$pdf" .pdf)
    
    echo "Processing $name..."
    
    python scripts/00_export_pdf_to_png.py \
        --pdf "$pdf" \
        --out "data/work/${name}.png"
    
    python scripts/10_floorplan_vectorizer.py \
        --image "data/work/${name}.png" \
        --out "data/work/${name}.json" \
        --sample
    
    blender -b -P scripts/20_json_to_blender.py \
        -- "data/work/${name}.json" "build/out/${name}.blend"
done
```

## Exemple 7 : Utilisation en Python

```python
# custom_pipeline.py
import sys
sys.path.insert(0, 'scripts')

from scripts.utils import io, geom

# Charger un JSON existant
data = io.load_json('data/work/floorplan.json')

# Modifier les données
for floor in data['floors']:
    for room in floor['rooms']:
        # Augmenter la taille de toutes les pièces de 10%
        polygon = room['polygon']
        center_x = sum(p[0] for p in polygon) / len(polygon)
        center_y = sum(p[1] for p in polygon) / len(polygon)
        
        new_polygon = []
        for x, y in polygon:
            dx = x - center_x
            dy = y - center_y
            new_x = center_x + dx * 1.1
            new_y = center_y + dy * 1.1
            new_polygon.append([new_x, new_y])
        
        room['polygon'] = new_polygon

# Sauvegarder
io.save_json(data, 'data/work/floorplan_scaled.json')
```

## Exemple 8 : Export pour Unity/Unreal

```bash
# Générer avec optimisations pour jeux vidéo
blender -b -P scripts/20_json_to_blender.py \
  -- data/work/floorplan.json build/out/game_ready.blend

# Puis dans Blender (mode GUI) :
# 1. Ouvrir build/out/game_ready.blend
# 2. File > Export > FBX
# 3. Cocher "Selected Objects" et exporter
```

## Troubleshooting

### Problème : Blender ne trouve pas le script
```bash
# Solution : Utiliser le chemin absolu
blender -b -P /full/path/to/scripts/20_json_to_blender.py -- ...
```

### Problème : JSON invalide
```bash
# Valider le JSON
python -c "import json; json.load(open('data/work/floorplan.json'))"
```

### Problème : Sortie vide
```bash
# Vérifier les logs Blender
blender -b -P scripts/20_json_to_blender.py -- ... 2>&1 | tee blender.log
```
