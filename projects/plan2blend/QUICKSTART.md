# 🚀 QUICKSTART — plan2blend

Guide de démarrage rapide pour générer un modèle 3D Blender à partir d'un plan 2D.

## Installation rapide

### Option 1 : Local (Python + Blender)

```bash
# 1. Installer les dépendances Python
cd projects/plan2blend
pip install -r requirements.txt

# 2. Installer Blender 3.6+ depuis https://www.blender.org/download/
```

### Option 2 : Docker (Recommandé)

```bash
cd projects/plan2blend
docker compose -f docker/docker-compose.yml build
```

## Utilisation rapide

### Pipeline complet avec données d'exemple

```bash
# Créer les répertoires nécessaires
mkdir -p data/work build/out

# 1. Générer un floorplan JSON d'exemple
python scripts/10_floorplan_vectorizer.py \
  --image data/work/plan_600dpi.png \
  --scale 1:150 \
  --out data/work/floorplan.json \
  --sample

# 2. Générer le modèle Blender (nécessite Blender installé)
blender -b -P scripts/20_json_to_blender.py \
  -- data/work/floorplan.json build/out/thalie.blend \
  --wall_thickness 0.20 --wall_height 2.80

# 3. Générer les overlays de contrôle
python scripts/30_quality_overlays.py \
  --plan data/work/plan_600dpi.png \
  --blend build/out/thalie.blend \
  --out build/out/overlays
```

### Avec Docker

```bash
# Pipeline complet en une commande
docker compose -f docker/docker-compose.yml up pipeline
```

## Avec votre propre PDF

```bash
# 1. Placer votre PDF dans data/input/
cp /path/to/your/plan.pdf data/input/

# 2. Convertir en PNG haute résolution
python scripts/00_export_pdf_to_png.py \
  --pdf data/input/plan.pdf \
  --out data/work/plan_600dpi.png \
  --dpi 600

# 3. Suivre les étapes du pipeline ci-dessus
```

## Vérification rapide

```bash
# Lancer les tests
pytest tests/test_metrics.py -v

# Vérifier les fichiers générés
ls -lh build/out/
# Vous devriez voir :
# - thalie.blend (modèle Blender)
# - thalie.glb (export glTF)
# - overlays/ (contrôles qualité)
```

## Structure des fichiers après exécution

```
plan2blend/
├── data/
│   ├── input/
│   │   └── votre_plan.pdf
│   └── work/
│       ├── plan_600dpi.png      ← Image haute résolution
│       └── floorplan.json       ← Données vectorisées
└── build/
    └── out/
        ├── thalie.blend         ← Modèle 3D Blender
        ├── thalie.glb           ← Export glTF
        └── overlays/            ← Contrôles visuels
            ├── original_plan.png
            ├── detected_edges.png
            └── overlay_preview.png
```

## Visualiser le résultat

### Blender
```bash
blender build/out/thalie.blend
```

### glTF (dans un navigateur)
Ouvrir https://gltf-viewer.donmccurdy.com/ et glisser-déposer `thalie.glb`

## Personnalisation

### Changer l'échelle du plan
```bash
python scripts/10_floorplan_vectorizer.py \
  --scale 1:100  # Au lieu de 1:150
```

### Ajuster les dimensions
```bash
blender -b -P scripts/20_json_to_blender.py \
  -- data/work/floorplan.json build/out/thalie.blend \
  --wall_thickness 0.25 \  # Murs plus épais
  --wall_height 3.00        # Plafond plus haut
```

## Problèmes courants

### Blender n'est pas trouvé
```bash
# Ajouter Blender au PATH
export PATH="/Applications/Blender.app/Contents/MacOS:$PATH"  # macOS
export PATH="/usr/bin/blender:$PATH"  # Linux
```

### Erreur de dépendances Python
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Docker ne construit pas
```bash
docker compose -f docker/docker-compose.yml build --no-cache
```

## Prochaines étapes

- Consulter le [README.md](README.md) pour la documentation complète
- Explorer les [prompts Copilot](prompts/) utilisés
- Consulter les [tests](tests/) pour les critères de qualité

## Support

Pour toute question, consulter la documentation complète dans README.md
