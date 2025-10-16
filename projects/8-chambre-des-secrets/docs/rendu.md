# 🧾 Rendu – Défi 8 : OÙ EST LA CHAMBRE DES SECRETS ?

## 🎯 Objectif

Créer un **plan 3D génératif** de "Poudlard" (bâtiment THALIE Montpellier) dans **Blender**, entièrement construit par script Python à partir du fichier JSON `context/plans/plan.json`. Ce plan met en évidence la **Chambre des Secrets** grâce à un effet lumineux émissif et une étiquette 3D, avec une animation de survol orbital.

---

## 🏗️ Architecture technique

### Stack technologique

- **Blender 4.0+**: Moteur 3D et rendu
- **Python 3.10+**: Script de génération (API bpy de Blender)
- **JSON**: Source de données (plan.json)
- **EEVEE**: Moteur de rendu temps réel
- **FFmpeg**: Encodage vidéo MP4

### Pipeline de génération

```
plan.json → build_hogwarts_plan.py → Blender API (bpy)
                                          ↓
                     Génération procédurale (géométrie + matériaux)
                                          ↓
                     Animation caméra + Configuration rendu
                                          ↓
                     hogwarts_plan.blend + plan_turntable.mp4
```

---

## 📋 Fonctionnalités implémentées

### 1. Lecture et parsing du JSON ✅

**Fichier source**: `context/plans/plan.json`

Le script charge automatiquement:
- Les 3 niveaux (RdC, R+1, R+2)
- Les caractéristiques de chaque pièce (nom, type, surface)
- Les paramètres de construction (hauteur murs, épaisseur, etc.)
- Les règles de layout automatique

```python
data = load_plan_data()
# Accès aux données:
# - data["levels"][0]["rooms"]
# - data["parametric_generation"]["wall_height_m"]
# - data["assumptions"]["floor_to_floor_height_m"]
```

### 2. Génération procédurale de la géométrie ✅

#### A. Structure des niveaux

- **3 collections Blender** créées automatiquement:
  - `Level_RdC`: 18 pièces
  - `Level_R+1`: 24 pièces
  - `Level_R+2`: 27 pièces

- **Espacement vertical**: 3.2m entre chaque niveau (paramètre `floor_to_floor_height_m`)

#### B. Génération de chaque pièce

Pour chaque room du JSON:

1. **Calcul automatique des dimensions**:
   ```python
   # Surface → dimensions (ratio variable selon type)
   ratio = 1.5 if room_type in ["salle_cours", "amphi"] else 1.2
   width = sqrt(area_m2 / ratio)
   length = area_m2 / width
   ```

2. **Création du sol** (cube aplati):
   - Dimension: longueur × largeur × 0.1m
   - Position: grille automatique avec espacement de 15m
   - Matériau: selon type de pièce

3. **Création des 4 murs**:
   - Hauteur: 3.0m (paramètre `wall_height_m`)
   - Épaisseur: 0.15m
   - Matériau: gris neutre

#### C. Disposition spatiale

Les pièces sont arrangées en **grille carrée** par niveau:
- RdC: grille 5×5 (18 pièces)
- R+1: grille 5×5 (24 pièces)
- R+2: grille 6×6 (27 pièces)

Espacement: 15m entre centres de pièces

### 3. Système de matériaux ✅

**11 matériaux distincts** créés avec l'API Shader Nodes:

| Type de pièce | Couleur | RGB | Usage |
|---------------|---------|-----|-------|
| Salles de cours | 🔵 Bleu clair | (0.3, 0.5, 0.8) | SALLE 1, 2, 3, 101-115 |
| Amphithéâtres | 🔵 Bleu foncé | (0.2, 0.3, 0.6) | GRAND SALLE 1 & 2 |
| Bureaux | 🟢 Vert | (0.4, 0.7, 0.4) | PROFS, BUREAU 1/2, DIR, ADMIN |
| Sanitaires | ⚪ Gris clair | (0.7, 0.7, 0.7) | SAN. H, SAN. F |
| Technique | ⚫ Gris foncé | (0.4, 0.4, 0.4) | SERVEUR, STOCK, ARCHIVES |
| Circulation | 🟡 Beige | (0.9, 0.85, 0.7) | ACCUEIL, HALL |
| Coworking | 🟠 Orange | (0.9, 0.6, 0.3) | CO-WORKING ÉTUDIANTS |
| Polyvalente | 🟣 Violet | (0.6, 0.4, 0.7) | POLYVALENTE 1/2, FLEX |
| Laboratoires | 🔵 Cyan | (0.3, 0.8, 0.8) | SAND BOX, MYDIL, ICL |
| Murs | ⚪ Gris | (0.85, 0.85, 0.85) | Tous les murs |
| **Chambre Secrets** | 🟢 **Vert émissif** | **(0.0, 1.0, 0.5)** | **Chambre spéciale** |

#### Matériau spécial: Chambre des Secrets

```python
# Shader Emission pur (sans BSDF)
emission = nodes.new(type="ShaderNodeEmission")
emission.inputs["Color"].default_value = (0.0, 1.0, 0.5, 1.0)  # Vert émeraude
emission.inputs["Strength"].default_value = 2.0  # Intensité lumineuse
```

**Effet**: La pièce émet sa propre lumière (halo vert visible dans toute la scène)

### 4. La Chambre des Secrets ✅

#### Position

- **Coordonnées**: (0, 0, -5.0) → 5 mètres **sous** le niveau RdC
- **Surface**: 150 m² (grande salle mystérieuse)
- **Hauteur**: 4.0m (plus haute que les autres)

#### Collection dédiée

`ChambreDesSecrets` isolée des autres niveaux pour mise en évidence

#### Éléments visuels

1. **Sol et murs émissifs**: 
   - Matériau `Mat_ChambreSecrets`
   - Vert émeraude lumineux (RGB: 0, 1.0, 0.5)
   - Strength: 2.0

2. **Texte 3D identifiant**:
   - Objet: `Text_ChambreSecrets`
   - Texte: "Chambre des Secrets"
   - Position: 1m au-dessus du sol de la chambre (z = -5 + 4 + 1 = 0m)
   - Taille: 1.5 unités
   - Extrusion: 0.1 (relief 3D)
   - Alignement: centré
   - Matériau: émissif identique (Strength: 3.0)

**Effet visuel**: Le texte flotte au-dessus de la chambre et brille intensément

### 5. Animation caméra orbitale ✅

#### Configuration

- **Type**: Caméra avec contrainte Track-To
- **Centre**: (30, 30, 0) - centre approximatif du plan
- **Rayon**: 60 unités
- **Hauteur**: 25 unités
- **Rotation**: 360° complet
- **Durée**: 240 frames (10 secondes à 24 fps)

#### Implémentation

```python
# Création de la caméra
camera = bpy.ops.object.camera_add(location=(center + radius, center, height))

# Objet vide pour le suivi
target = bpy.ops.object.empty_add(type='PLAIN_AXES', location=center)

# Contrainte de suivi
constraint = camera.constraints.new(type='TRACK_TO')
constraint.target = target

# Animation en boucle (keyframes sur chaque frame)
for frame in range(1, 241):
    angle = (frame / 240) * 2 * pi
    x = center_x + radius * cos(angle)
    y = center_y + radius * sin(angle)
    camera.location = (x, y, height)
    camera.keyframe_insert(data_path="location", frame=frame)
```

**Résultat**: Rotation fluide continue autour du plan

### 6. Éclairage de la scène ✅

#### Deux sources lumineuses

1. **Sun (Key Light)**:
   - Type: Directionnelle
   - Position: (10, 10, 20)
   - Énergie: 1.5
   - Angle: 45° en XZ

2. **Area Light (Fill)**:
   - Type: Aire
   - Position: (0, 0, 30) - au-dessus du centre
   - Énergie: 500
   - Taille: 50 unités

**Effet**: Éclairage doux et uniforme style "plan d'architecte"

### 7. Configuration du rendu ✅

#### Paramètres EEVEE

```python
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100

# Bloom pour les émissifs
scene.eevee.use_bloom = True
scene.eevee.bloom_intensity = 0.1
```

#### Export vidéo

```python
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'
scene.render.ffmpeg.constant_rate_factor = 'HIGH'
scene.render.filepath = "renders/plan_turntable.mp4"
```

**Qualité**: 1080p, H264, qualité élevée

---

## 🚀 Utilisation

### Commande d'exécution

```bash
# Mode background (recommandé pour production)
blender --background --python projects/8-chambre-des-secrets/build_hogwarts_plan.py

# Mode interface (pour debug/visualisation)
blender --python projects/8-chambre-des-secrets/build_hogwarts_plan.py
```

### Workflow

1. **Chargement** (1s):
   - Lecture de `context/plans/plan.json`
   - Parsing des 3 niveaux et 69 pièces

2. **Génération** (10-30s):
   - Nettoyage de la scène
   - Création de 11 matériaux
   - Génération de 69 pièces × 5 objets (sol + 4 murs) = 345 objets
   - Chambre des Secrets + texte 3D
   - Configuration caméra et éclairage

3. **Rendu** (5-15 min):
   - 240 frames à 1080p
   - Temps variable selon GPU

4. **Export** (1s):
   - Sauvegarde `hogwarts_plan.blend`
   - Fichier vidéo `renders/plan_turntable.mp4`

### Temps d'exécution total

- **Génération seule**: ~30 secondes
- **Génération + Rendu**: ~10 minutes (selon matériel)

---

## 📊 Statistiques de la scène

| Élément | Quantité | Détails |
|---------|----------|---------|
| Niveaux | 3 | RdC, R+1, R+2 |
| Pièces totales | 69 | Incluant la Chambre |
| Objets 3D | ~350 | 69 × 5 + caméra + lights + texte |
| Collections | 4 | 3 levels + ChambreDesSecrets |
| Matériaux | 12 | 11 types + texte émissif |
| Lumières | 2 | Sun + Area |
| Keyframes | 240 | Animation caméra |
| Résolution | 1920×1080 | Full HD |
| Format sortie | MP4 H264 | Vidéo compressée |

---

## ✅ Validation des critères

### Critères obligatoires

| Critère | Statut | Implémentation |
|---------|--------|----------------|
| Script lit `plan.json` sans modif manuelle | ✅ | `load_plan_data()` ligne 54 |
| Plan 3D généré dynamiquement | ✅ | `generate_level()` ligne 267 |
| Chambre positionnée sous niveau principal | ✅ | Position z=-5.0, ligne 370 |
| Matériau émissif (halo bleu/vert) | ✅ | Emission vert (0, 1, 0.5), ligne 180 |
| Texte 3D "Chambre des Secrets" | ✅ | `bpy.ops.object.text_add()` ligne 393 |
| Caméra animée orbitale | ✅ | `create_animated_camera()` ligne 430 |
| Vidéo MP4 fluide | ✅ | 240 frames H264, ligne 497 |
| Script relançable sans erreur | ✅ | Nettoyage complet en début |

### Critères bonus

| Bonus | Statut | Notes |
|-------|--------|-------|
| Éléments de décor 3D | ⚠️ | Structure `props/` prête (non implémenté) |
| Trappe animée | ❌ | Non implémenté |
| Icônes 3D pièces | ❌ | Non implémenté |
| Export GLTF/FBX | ⚠️ | Code prêt (commenté) |
| Carte du Maraudeur | ❌ | Non implémenté |

---

## 🔧 Paramètres configurables

### Dans le script

```python
# Ligne 277: Paramètres globaux
WALL_HEIGHT = data["parametric_generation"]["wall_height_m"]  # 3.0m
WALL_THICKNESS = 0.15  # Modifiable
SPACING = 15.0  # Espacement grille

# Ligne 370: Chambre des Secrets
CHAMBER_Z = -5.0  # Profondeur sous le RdC
CHAMBER_HEIGHT = 4.0  # Hauteur des murs

# Ligne 450: Caméra
CAMERA_RADIUS = 60  # Distance
CAMERA_HEIGHT = 25  # Altitude
FRAMES = 240  # Durée animation

# Ligne 475: Résolution
RESOLUTION_X = 1920
RESOLUTION_Y = 1080
```

### Dans le JSON

Le script respecte automatiquement:
- `parametric_generation.wall_height_m`
- `assumptions.floor_to_floor_height_m`
- `assumptions.wall_thickness_m`
- Surfaces de chaque pièce (`area_m2`)

---

## 🧪 Tests et validation

### Script de test

`tests/test_validation.sh` vérifie:

1. ✅ Présence de `context/plans/plan.json`
2. ✅ Installation de Blender
3. ✅ Exécution sans erreur du script Python
4. ✅ Génération de `hogwarts_plan.blend`
5. ✅ Présence de `renders/plan_turntable.mp4`

### Exécution des tests

```bash
cd projects/8-chambre-des-secrets/tests/
bash test_validation.sh
```

---

## 🎨 Style visuel

### Rendu "Blueprint Moderne"

- **Fond**: Noir (défaut Blender)
- **Éclairage**: Doux et uniforme
- **Couleurs**: Pastels saturés par type
- **Effet spécial**: Bloom sur émissifs (Chambre)
- **Vue**: Aérienne dynamique (orbital)

### Inspiration

- Plans d'architecte 3D modernes
- Style "ligne épurée" avec matériaux plats
- Mise en valeur par la couleur et la lumière

---

## 📈 Évolutions possibles

### Court terme (1-2h)

1. **Props mobilier**:
   - Tables: `bpy.ops.mesh.primitive_cube_add()` + scale
   - Tableaux: Planes texturés
   - Stockage: Petits cubes

2. **Export multi-format**:
   ```python
   bpy.ops.export_scene.gltf(filepath="hogwarts_plan.glb")
   bpy.ops.export_scene.fbx(filepath="hogwarts_plan.fbx")
   ```

3. **Portes visibles**:
   - Découpes dans les murs (Boolean Modifier)
   - Chambranles colorés

### Moyen terme (1 journée)

1. **Trappe animée**:
   - Objet hatch avec rotation keyframes
   - Ouverture progressive révélant la Chambre

2. **Chemins de circulation**:
   - Couloirs entre pièces
   - Escaliers entre niveaux

3. **Signalétique**:
   - Textes 3D pour chaque pièce
   - Panneaux directionnels

### Long terme (multi-jours)

1. **Textures réalistes**:
   - PBR materials (bois, pierre, métal)
   - Normal maps pour relief

2. **Éclairage dynamique**:
   - Torches animées
   - Fenêtres avec lumière extérieure

3. **Carte du Maraudeur**:
   - Overlay 2D parchemin
   - Traces de pas animées
   - Style "vieil anglais"

---

## 🐛 Problèmes connus et solutions

### 1. Blender non trouvé

**Symptôme**: `command not found: blender`

**Solution**:
```bash
# Ubuntu/Debian
sudo snap install blender --classic

# macOS
brew install --cask blender

# Vérifier
blender --version
```

### 2. Fichier JSON introuvable

**Symptôme**: `FileNotFoundError: context/plans/plan.json`

**Solution**: Exécuter depuis la racine du projet:
```bash
cd /path/to/workshop-poudlard-epsi/
blender --background --python projects/8-chambre-des-secrets/build_hogwarts_plan.py
```

### 3. Rendu trop lent

**Solution temporaire**: Réduire la qualité
```python
# Dans le script, ligne 475
scene.render.resolution_percentage = 50  # 50% résolution
bpy.context.scene.frame_end = 120       # Moitié des frames
```

### 4. Vidéo ne se génère pas

**Cause**: FFmpeg non installé avec Blender

**Solution**:
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg
```

---

## 📝 Conclusion

Ce projet démontre:

1. ✅ **Génération procédurale** complète à partir de données JSON
2. ✅ **Automatisation** totale du workflow (JSON → 3D → Animation → Vidéo)
3. ✅ **Organisation** claire du code en sections fonctionnelles
4. ✅ **Respect des spécifications** (Chambre émissive, texte, animation)
5. ✅ **Reproductibilité** garantie (script autonome)

**Points forts**:
- Script documenté et commenté
- Paramètres configurables
- Architecture extensible
- Rendu performant (EEVEE)

**Améliorations futures**:
- Props 3D détaillés
- Interactions (trappe, portes)
- Export multi-format
- Optimisation performance

---

## 📚 Références

- [Blender Python API (bpy)](https://docs.blender.org/api/current/)
- [EEVEE Render Engine](https://docs.blender.org/manual/en/latest/render/eevee/)
- [FFmpeg Video Encoding](https://trac.ffmpeg.org/wiki/Encode/H.264)

---

**🏰 "Le plan de Poudlard révèle ses secrets à ceux qui savent chercher."**

*Document généré pour le Workshop EPSI/WIS 2025-2026 - Défi 8*
