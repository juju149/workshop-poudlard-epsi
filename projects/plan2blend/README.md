# plan2blend — Générer un `.blend` 3D à partir d'un PDF de plan 2D

> **But** : Entrer un plan 2D (PDF) du bâtiment **THALIE** et produire automatiquement un **projet Blender** (`.blend`) fidèle (murs, pièces, ouvertures, échelle réelle), avec un pipeline **scriptable** (Python/Blender) et **assisté par IA** (vectorisation des murs/portes/fenêtres).

## 🎯 Objectif

* **Entrée** : `PRIVE_Plans_THALIE_Montpellier.pdf` (ou image exportée du PDF)
* **Sortie principale** : `build/out/thalie.blend` (unités **mètres**)
* **Sorties bonus** : `build/out/thalie.glb` (glTF) + `build/out/overlays/` (contrôles visuels)
* **Fidélité** : Erreur d'échelle < **1%** et erreur d'épaisseur de mur < **5 cm** vs. plan
* **Couverture** : 100% des pièces fermées **identifiées** et extrudées ; portes/fenêtres détectées et **percées** sur ≥ **80%** des cas lisibles

## 📦 Structure du projet

```
plan2blend/
├── README.md                          # Ce fichier
├── data/
│   ├── input/                         # Placez vos PDFs ici
│   │   └── PRIVE_Plans_THALIE_Montpellier.pdf
│   └── work/                          # Fichiers intermédiaires
│       ├── plan_600dpi.png
│       └── floorplan.json
├── build/
│   └── out/                           # Sorties finales
│       ├── thalie.blend
│       ├── thalie.glb
│       └── overlays/
├── scripts/
│   ├── 00_export_pdf_to_png.py       # Conversion PDF → PNG haute résolution
│   ├── 10_floorplan_vectorizer.py    # Vectorisation IA → JSON
│   ├── 20_json_to_blender.py         # Génération du modèle 3D Blender
│   ├── 30_quality_overlays.py        # Contrôle qualité par superposition
│   └── utils/
│       ├── geom.py                   # Utilitaires géométriques
│       └── io.py                     # Utilitaires I/O
├── docker/
│   ├── docker-compose.yml            # Services IA + Blender headless
│   └── Dockerfile.blender            # Image Blender personnalisée
├── prompts/
│   ├── copilot_glue_blender.md      # Prompts pour génération code Blender
│   └── copilot_vectorizer_adapter.md # Prompts pour adapter vectoriseur
└── tests/
    ├── test_metrics.py               # Tests de validation
    └── snapshots/                    # Images de référence
```

## 🚀 Installation et prérequis

### Option A : Installation locale (Blender + Python)

**Prérequis** :
- Python 3.11+
- Blender 3.6+ installé localement
- pip pour les dépendances Python

```bash
# Installer les dépendances Python
pip install -r requirements.txt
```

### Option B : Docker (Recommandé)

**Prérequis** :
- Docker
- Docker Compose

```bash
# Construire les images Docker
docker compose -f docker/docker-compose.yml build
```

## 📖 Utilisation

### Pipeline complet (local)

#### 1. Convertir le PDF en image haute résolution

```bash
python scripts/00_export_pdf_to_png.py \
  --pdf data/input/PRIVE_Plans_THALIE_Montpellier.pdf \
  --out data/work/plan_600dpi.png \
  --dpi 600
```

#### 2. Vectoriser le plan (détection des murs/portes/fenêtres)

```bash
python scripts/10_floorplan_vectorizer.py \
  --image data/work/plan_600dpi.png \
  --scale 1:150 \
  --out data/work/floorplan.json
```

#### 3. Générer le modèle Blender 3D

```bash
blender -b -P scripts/20_json_to_blender.py \
  -- data/work/floorplan.json build/out/thalie.blend \
  --wall_thickness 0.20 --wall_height 2.80
```

#### 4. Générer les overlays de contrôle qualité

```bash
python scripts/30_quality_overlays.py \
  --plan data/work/plan_600dpi.png \
  --blend build/out/thalie.blend \
  --out build/out/overlays
```

### Pipeline complet (Docker)

```bash
# 1. Vectorisation
docker compose -f docker/docker-compose.yml up --build vectorizer

# 2. Génération Blender
docker compose -f docker/docker-compose.yml run blender \
  -b -P /app/scripts/20_json_to_blender.py -- \
  /app/data/work/floorplan.json /app/build/out/thalie.blend \
  --wall_thickness 0.20 --wall_height 2.80

# 3. Overlays QA
docker compose -f docker/docker-compose.yml run blender \
  -b /app/build/out/thalie.blend -P /app/scripts/30_quality_overlays.py
```

## 🔍 Format JSON intermédiaire

Le fichier `floorplan.json` généré par l'étape de vectorisation suit ce schéma :

```json
{
  "scale": {
    "paper": 1,
    "real": 150
  },
  "floors": [
    {
      "code": "RDC",
      "rooms": [
        {
          "name": "SALLE 103",
          "polygon": [[x1, y1], [x2, y2], ...],
          "features": {
            "doors": [
              {"start": [x1, y1], "end": [x2, y2], "width": 0.9}
            ],
            "windows": [
              {"start": [x1, y1], "end": [x2, y2], "width": 1.2, "height": 1.1}
            ]
          }
        }
      ]
    }
  ]
}
```

Toutes les coordonnées sont en **mètres**.

## ✅ Tests et validation

### Exécuter les tests

```bash
# Tests de métriques (échelle, surfaces, ouvertures)
pytest tests/test_metrics.py -v
```

### Critères d'acceptation

- [x] **Échelle** : Erreur < 1% sur les distances mesurées
- [x] **Murs** : Continuité topologique, épaisseur ± 5 cm
- [x] **Ouvertures** : ≥ 80% des portes/fenêtres détectées et percées
- [x] **Export** : `.blend` et `.glb` générés et fonctionnels
- [x] **Overlays** : Superposition plan/rendu avec erreur moyenne < 1%

## 🛠️ Architecture technique

### Pipeline hybride

1. **Pré-traitement** : PDF → PNG 600 DPI avec optimisation de contraste
2. **Vectorisation IA** : Détection automatique des éléments architecturaux
3. **Génération 3D** : Construction du modèle Blender avec Python (bpy)
4. **QA** : Validation par superposition et métriques

### Choix techniques

- **Découplage** : IA (reconnaissance) séparée de la 3D (construction)
- **Scriptable** : Tout en Python pour faciliter l'automatisation
- **Extensible** : Facile d'ajouter de nouvelles features (meubles, escaliers, etc.)
- **Validable** : Overlays et métriques pour garantir la qualité

## 📚 Documentation complémentaire

- [Prompts Copilot](prompts/) : Prompts utilisés pour générer le code
- [Tests](tests/) : Suite de tests pour valider la fidélité

## 🎨 Extensions possibles (facultatif)

- [ ] Meubles placeholders (tables, chaises) selon features détectées
- [ ] Caméra visite avec path animation et DOF
- [ ] Rendu Eevee/Cycles pour visualisation réaliste
- [ ] Export IFC ou OBJ pour interopérabilité BIM
- [ ] Détection automatique de l'échelle dans le cartouche

## 📝 Licence

Ce projet est open-source. Les dépendances et modèles IA utilisés conservent leurs licences respectives.

## 🙏 Crédits

- Blender Foundation pour Blender
- Communautés open-source pour les outils de vectorisation
- GitHub Copilot pour l'assistance au développement
