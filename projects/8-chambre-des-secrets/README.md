# 🏰 DÉFI 8 - OÙ EST LA CHAMBRE DES SECRETS ?

Plan 3D animé de Poudlard généré automatiquement avec Blender

## 🎯 Objectif

Générer un plan 3D de "Poudlard" (basé sur les données du bâtiment THALIE à Montpellier) avec mise en évidence de la **Chambre des Secrets** grâce à un effet lumineux émissif et une animation orbitale.

## 📦 Contenu du projet

```
8-chambre-des-secrets/
├── build_hogwarts_plan.py      # Script Python pour Blender
├── README.md                    # Ce fichier
├── docs/
│   └── rendu.md                # Documentation détaillée
├── tests/
│   └── test_validation.sh      # Script de test
├── renders/
│   └── plan_turntable.mp4      # Animation générée (après exécution)
├── props/                       # Props 3D optionnels
└── hogwarts_plan.blend         # Fichier Blender généré (après exécution)
```

## 🚀 Installation et utilisation

### Prérequis

- **Blender 4.0+** installé et accessible via la ligne de commande
- Python 3.10+ (généralement inclus avec Blender)
- Le fichier `context/plans/plan.json` à la racine du projet

### Installation de Blender

#### Ubuntu/Debian
```bash
sudo snap install blender --classic
```

#### macOS
```bash
brew install --cask blender
```

#### Windows
Télécharger depuis https://www.blender.org/download/

### Exécution du script

#### Mode background (sans interface)
```bash
# Depuis la racine du projet workshop-poudlard-epsi/
blender --background --python projects/8-chambre-des-secrets/build_hogwarts_plan.py
```

#### Mode interface (pour visualiser en direct)
```bash
# Depuis la racine du projet
blender --python projects/8-chambre-des-secrets/build_hogwarts_plan.py
```

#### Depuis le répertoire du défi
```bash
cd projects/8-chambre-des-secrets/
blender --background --python build_hogwarts_plan.py
```

### Temps d'exécution

- **Génération du plan**: ~10-30 secondes
- **Rendu de l'animation** (240 frames): ~5-15 minutes selon la machine

## 📋 Fonctionnalités

### ✅ Implémenté

- ✅ Lecture automatique du fichier `context/plans/plan.json`
- ✅ Génération dynamique des 3 niveaux (RdC, R+1, R+2)
- ✅ Création automatique des pièces avec murs, sols
- ✅ Matériaux distincts par type de pièce:
  - 🔵 Bleu: salles de cours et amphithéâtres
  - 🟢 Vert: bureaux et administration
  - ⚪ Gris: sanitaires et technique
  - 🟡 Beige: circulation et accueil
  - 🟠 Orange: coworking
  - 🟣 Violet: espaces polyvalents
  - 🔵 Cyan: laboratoires
- ✅ **Chambre des Secrets**:
  - Positionnée sous le niveau principal (z=-5m)
  - Matériau émissif vert émeraude lumineux
  - Texte 3D "Chambre des Secrets" au-dessus
- ✅ Caméra orbitale animée (240 frames = 10 secondes à 24 fps)
- ✅ Éclairage adapté (Sun + Area light)
- ✅ Export automatique en MP4 (H264)
- ✅ Sauvegarde du fichier .blend

### 🎨 Style visuel

- Rendu EEVEE (temps réel, performant)
- Effet bloom pour les éléments émissifs
- Vue aérienne avec rotation complète à 360°
- Éclairage style "plan d'architecte moderne"

## 🎬 Résultat attendu

Après exécution, vous obtiendrez:

1. **hogwarts_plan.blend**: Fichier Blender complet avec:
   - Collections organisées par niveau
   - Collection spéciale "ChambreDesSecrets"
   - Tous les matériaux et objets
   - Animation de caméra configurée

2. **renders/plan_turntable.mp4**: Vidéo de 10 secondes montrant:
   - Vue d'ensemble des 3 niveaux empilés
   - Rotation orbitale complète
   - Chambre des Secrets visible en dessous avec son halo vert

## 🧪 Tests

Pour valider l'exécution:

```bash
cd tests/
bash test_validation.sh
```

Le script vérifie:
- Présence du fichier JSON source
- Existence de Blender
- Génération du fichier .blend
- Présence de la vidéo de rendu

## 🔧 Personnalisation

### Modifier les paramètres de la caméra

Dans `build_hogwarts_plan.py`, ligne ~450:

```python
create_animated_camera(
    center=(30, 30, 0),  # Centre de rotation
    radius=60,            # Distance de la caméra
    height=25,            # Hauteur de la caméra
    frames=240            # Nombre de frames (10s à 24fps)
)
```

### Changer la résolution

Ligne ~475:

```python
scene.render.resolution_x = 1920  # Largeur
scene.render.resolution_y = 1080  # Hauteur
```

### Modifier les matériaux

Section "CRÉATION DES MATÉRIAUX" ligne ~120:

```python
nodes["Principled BSDF"].inputs["Base Color"].default_value = (R, G, B, A)
```

## 📚 Structure du code

Le script est organisé en sections:

1. **Configuration**: Chemins et paramètres
2. **Chargement**: Lecture du JSON
3. **Nettoyage**: Reset de la scène
4. **Matériaux**: Création des shaders
5. **Géométrie**: Génération des pièces, murs
6. **Chambre des Secrets**: Création spéciale avec effet
7. **Animation**: Caméra orbitale
8. **Éclairage**: Setup des lumières
9. **Rendu**: Configuration et export

## 🐛 Dépannage

### Erreur "FileNotFoundError: plan.json"

Assurez-vous d'être dans le bon répertoire:

```bash
# Le chemin doit être valide:
ls context/plans/plan.json
```

Ou exécutez depuis la racine du projet.

### Blender non trouvé

Vérifier l'installation:

```bash
blender --version
```

Si non installé, suivre les instructions d'installation ci-dessus.

### Le rendu est lent

Mode rapide (basse qualité):

```python
scene.render.resolution_percentage = 50  # 50% de la résolution
bpy.context.scene.frame_end = 120       # Moitié moins de frames
```

## 🌟 Extensions possibles (Bonus)

- [ ] Ajout de props 3D (bureaux, tableaux, torches) dans `props/`
- [ ] Trappe animée qui s'ouvre pour révéler la Chambre
- [ ] Icônes 3D pour les pièces importantes
- [ ] Export GLTF/FBX pour visualisation web
- [ ] Style "Carte du Maraudeur" en post-processing
- [ ] Chemins de circulation entre les pièces

## 📖 Documentation complète

Voir `docs/rendu.md` pour la documentation détaillée destinée au jury.

## 🏆 Critères de validation

- [x] Script Python lit le JSON sans modification manuelle
- [x] Plan 3D généré dynamiquement
- [x] Chambre des Secrets sous le niveau principal
- [x] Matériau émissif (halo vert)
- [x] Texte 3D identifiant la chambre
- [x] Caméra animée orbitale
- [x] Vidéo MP4 fluide exportée
- [x] Script relançable sans erreur

## 📝 Licence et contexte

Projet réalisé dans le cadre du Workshop EPSI/WIS "Poudlard à l'EPSI" 2025-2026.

---

**🐍 "La Chambre des Secrets a été ouverte. Les ennemis de l'héritier, prenez garde."**
