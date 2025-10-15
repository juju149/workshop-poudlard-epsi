# 🚀 QUICKSTART - Défi 8: Chambre des Secrets 3D

## ⚡ Génération rapide (5 minutes)

### 1️⃣ Installation de Blender

```bash
# Ubuntu/Debian
sudo apt install blender

# macOS
brew install --cask blender

# Windows: Télécharger depuis https://www.blender.org/download/
```

### 2️⃣ Génération du plan 3D

```bash
cd projects/08-chambre-secrets-3d

# Exécuter le script
blender --background --python build_hogwarts_plan.py
```

**Sortie attendue**: `hogwarts_plan.blend` créé

### 3️⃣ Génération de la vidéo

#### Option A: Interface graphique
```bash
# Ouvrir le fichier dans Blender
blender hogwarts_plan.blend

# Dans Blender: Render > Render Animation (Ctrl+F12)
```

#### Option B: Ligne de commande
```bash
blender hogwarts_plan.blend --background --render-anim
```

**Sortie attendue**: `renders/plan_turntable.mp4` (10 secondes, 1920x1080)

---

## 📋 Vérification

### Fichiers générés
- ✅ `hogwarts_plan.blend` - Scène Blender complète
- ✅ `renders/plan_turntable.mp4` - Animation turntable

### Dans Blender (vérification visuelle)
1. Ouvrir `hogwarts_plan.blend`
2. Vérifier que la Chambre des Secrets **brille en vert**
3. Vérifier le texte 3D "Chambre des Secrets"
4. Tester l'animation: Espace (lecture)

---

## 🎯 Caractéristiques principales

| Élément | Description |
|---------|-------------|
| **Plan** | Grande Salle + 4 salles de classe + couloirs + bibliothèque + tour |
| **Chambre** | Sous le sol principal (-4m), matériau vert lumineux |
| **Animation** | Rotation 360° en 10 secondes |
| **Résolution** | 1920x1080, 24 FPS |
| **Format** | MP4 (H.264) |

---

## 🔧 Personnalisation rapide

### Modifier la durée de l'animation
```python
# Dans build_hogwarts_plan.py, ligne ~25
ANIMATION_FRAMES = 480  # 20 secondes au lieu de 10
```

### Changer la couleur de la Chambre
```python
# Dans build_hogwarts_plan.py, ligne ~27
COLOR_CHAMBER = (1.0, 0.0, 0.0, 1.0)  # Rouge au lieu de vert
```

### Ajuster la hauteur de caméra
```python
# Dans build_hogwarts_plan.py, ligne ~32
CAMERA_HEIGHT = 25.0  # Plus haut pour vue d'ensemble
```

---

## 🆘 Dépannage express

| Problème | Solution |
|----------|----------|
| `blender: command not found` | Installer Blender ou utiliser chemin complet |
| Pas de rendu vidéo | Créer le dossier: `mkdir -p renders` |
| Rendu trop lent | Réduire résolution à 1280x720 dans le script |
| Chambre invisible | Elle est sous le sol, ajuster angle caméra |

---

## 📚 Documentation complète

Pour plus de détails, voir [README.md](README.md)

---

**Temps total**: ~5-15 minutes (selon puissance machine)  
**Niveau**: Débutant à Intermédiaire Blender  
**Dépendances**: Blender 3.0+ uniquement

✨ **C'est parti !** ⚡
