# ML Plan2Blend — Générer un `.blend` exact depuis un plan 2D

> **Machine Learning** pour reconstruire automatiquement un bâtiment 3D fidèle (Blender `.blend`) à partir d'un plan 2D (PDF/PNG).

## 🎯 Objectif

À partir d'un **plan 2D** (PDF/PNG) du bâtiment THALIE, produire **automatiquement** un fichier **Blender** (`.blend`) **exact** (murs, pièces, portes, fenêtres, escaliers placeholders) avec **unités réelles** et **échelle respectée**, exportable en **glTF**.

### KPI / Definition of Done

* **Échelle** : erreur moyenne < **1%** (mesures aléatoires vs. cotations plan).
* **Murs** : IoU masque ≥ **0.95** ; épaisseur moyenne correcte à ± **5 cm**.
* **Portes/Fenêtres** : AP50 ≥ **0.90** ; position/largeur à ± **5 cm**.
* **Pièces** : couverture ≥ **99%** des zones fermées.
* **QA overlay** : distance Hausdorff normalisée ≤ **0.02**.
* Assets livrés : `.blend`, `.glb`, overlays QA, logs, Model Card.

## 🏗️ Architecture

### Pipeline Overview

1. **Input**: Plan 2D (PDF/PNG) → Prétraitement (600 DPI)
2. **ML Inference**: Segmentation (murs) + Détection (portes/fenêtres)
3. **Vectorisation**: Post-traitement → JSON structuré (mètres)
4. **3D Generation**: Blender script (bpy) → `.blend` + `.glb`
5. **QA**: Métriques + overlays de validation

### Modules

* `src/utils/` - Utilitaires IO, géométrie, conversion d'échelle
* `src/training/` - Scripts d'entraînement ML (segmentation, détection)
* `src/inference/` - Pipeline d'inférence et vectorisation
* `src/blender/` - Génération 3D avec Blender (bpy)
* `tests/` - Tests unitaires et d'intégration

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# For Blender integration, ensure Blender 3.x+ is installed
```

### Usage

#### 1. Convert PDF to PNG (600 DPI)

```bash
python -m src.utils.io pdf2png \
  --pdf data/input/PRIVE_Plans_THALIE_Montpellier.pdf \
  --out data/work/plan_600dpi.png \
  --dpi 600
```

#### 2. Run Inference (Image → JSON)

```bash
python -m src.inference.infer \
  --image data/work/plan_600dpi.png \
  --scale 1:150 \
  --out build/out/floorplan.json
```

#### 3. Generate Blender File

```bash
blender -b -P src/blender/json_to_blender.py -- \
  build/out/floorplan.json \
  build/out/thalie.blend \
  --wall_thickness 0.20 \
  --wall_height 2.80
```

#### 4. Run QA Metrics

```bash
python -m src.inference.metrics \
  --plan data/work/plan_600dpi.png \
  --blend build/out/thalie.blend \
  --out build/reports
```

## 📦 Directory Structure

```
ml-plan2blend/
├── README.md
├── requirements.txt
├── MODEL_CARD.md
├── data/
│   ├── input/           # Input PDFs
│   └── work/            # Processed PNGs
├── datasets/
│   ├── images/          # Training images
│   └── labels/          # Annotations (CVAT export)
├── src/
│   ├── training/
│   │   ├── train_segmentation.py
│   │   ├── train_detection.py
│   │   └── augments.py
│   ├── inference/
│   │   ├── infer.py           # End-to-end pipeline
│   │   ├── vectorize.py       # Post-processing
│   │   └── metrics.py         # QA metrics
│   ├── blender/
│   │   └── json_to_blender.py # JSON → .blend/.glb
│   └── utils/
│       ├── io.py              # PDF conversion, JSON I/O
│       └── geometry.py        # Geometric operations
├── docker/
│   ├── Dockerfile.train
│   ├── Dockerfile.blender
│   └── docker-compose.yml
├── build/
│   ├── out/                   # Generated .blend/.glb files
│   └── reports/               # QA metrics and overlays
└── tests/
    ├── test_vectorize.py
    └── test_metrics.py
```

## 🧩 JSON Schema

Le format JSON intermédiaire pour la vectorisation:

```json
{
  "scale": {
    "paper": 1,
    "real": 150
  },
  "floors": [
    {
      "code": "RDC",
      "name": "Rez-de-chaussée",
      "walls": [
        {
          "poly": [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
        }
      ],
      "doors": [
        {
          "pos": [[x1, y1], [x2, y2]],
          "width": 0.90
        }
      ],
      "windows": [
        {
          "pos": [[x1, y1], [x2, y2]],
          "width": 1.20,
          "sill": 0.90
        }
      ],
      "rooms": [
        {
          "name": "SALLE 101",
          "poly": [[x1, y1], [x2, y2], ...],
          "area_m2": 45.5
        }
      ]
    }
  ]
}
```

**Unités** : Toutes les coordonnées sont en **mètres** (origine = bas-gauche de l'image).

## 🧪 Testing

```bash
# Run unit tests
python -m pytest tests/ -v

# Run specific test
python -m pytest tests/test_vectorize.py -v
```

## 📊 Model Training

### Segmentation (Walls)

```bash
python -m src.training.train_segmentation \
  --data datasets/ \
  --epochs 100 \
  --batch-size 8 \
  --model unet
```

### Detection (Doors/Windows)

```bash
python -m src.training.train_detection \
  --data datasets/ \
  --epochs 100 \
  --batch-size 16 \
  --model yolo
```

## 🐳 Docker

### Build Images

```bash
docker-compose -f docker/docker-compose.yml build
```

### Run Pipeline

```bash
docker-compose -f docker/docker-compose.yml up
```

## 📝 Model Card

See [MODEL_CARD.md](MODEL_CARD.md) for detailed information about:
- Training data and annotations
- Model architecture and hyperparameters
- Performance metrics
- Limitations and biases
- Licensing information

## ⚠️ Limitations

**Version 1.0** :
- Plans noir/blanc ou niveaux de gris uniquement
- Murs rectilignes (courbes non garanties)
- Épaisseur de mur uniforme par défaut
- Escaliers en placeholder simple
- Pas de détails MEP (électrique, CVC)
- Pas de textures réalistes

## 🤝 Contributing

Pour contribuer au projet:
1. Fork le repository
2. Créer une branche feature
3. Commiter les changements
4. Push et créer une Pull Request

## 📄 License

[À définir selon les besoins du projet]

## 📞 Contact

Pour toute question sur le projet ML Plan2Blend, contactez l'équipe de développement.
