# 📊 Guide de Création du Dataset - IS IT YOU HARRY?

Guide pratique pour collecter et organiser un dataset d'images de personnages Harry Potter pour l'entraînement du modèle CNN.

---

## 🎯 Objectif

Créer un dataset de **10 personnages** avec **~200 images par personnage** (soit ~2000 images au total) pour entraîner un modèle de reconnaissance avec haute précision.

---

## 👥 Personnages à collecter

1. **Harry Potter** - Le survivant (cicatrice, lunettes, cheveux noirs)
2. **Hermione Granger** - Cheveux bouclés, intelligente
3. **Ron Weasley** - Cheveux roux, meilleur ami
4. **Albus Dumbledore** - Barbe blanche, directeur
5. **Severus Snape** - Cheveux noirs, cape noire
6. **Voldemort** - Pas de nez, chauve, pâle
7. **Draco Malfoy** - Cheveux blond platine, Serpentard
8. **Hagrid** - Demi-géant, barbe, grand
9. **Minerva McGonagall** - Chapeau pointu, strict
10. **Sirius Black** - Cheveux noirs longs, tatouages

---

## 📚 Sources de données

### 1. Web Scraping

**Google Images**
- Recherche: "[Nom personnage] Harry Potter"
- Filtres: Taille > Medium, Usage rights > Labeled for reuse
- Outils: Extensions Chrome (Download All Images, Image Downloader)

**Bing Images**
- Similaire à Google
- Parfois images différentes
- API disponible (Microsoft Cognitive Services)

**Pinterest**
- Beaucoup de fan art et photos de qualité
- Requiert un compte
- Scraping possible avec Beautiful Soup

### 2. Captures d'écran

**Films Harry Potter** (8 films)
- Meilleure qualité pour visages
- Variété d'angles et expressions
- Utiliser VLC ou FFmpeg pour extraire frames

```bash
# Extraire 1 frame toutes les 5 secondes
ffmpeg -i "Harry_Potter_Film.mp4" -vf fps=1/5 output_%04d.jpg
```

### 3. Datasets existants

**Kaggle**
- Rechercher "Harry Potter faces" ou "Character recognition"
- Vérifier licences d'utilisation

**ImageNet / Google Dataset Search**
- Sous-catégories de célébrités (acteurs Harry Potter)

### 4. Génération par IA

**Stable Diffusion**
```
Prompt: "Portrait of [character name] from Harry Potter, 
high quality, detailed face, film still, realistic"
```

**DALL-E / Midjourney**
- Bonne qualité mais peut manquer de réalisme
- Utile pour augmenter dataset

---

## 🛠️ Méthodes de collecte automatisée

### Script Python - Google Images

```python
from google_images_download import google_images_download

response = google_images_download.googleimagesdownload()

characters = [
    "Harry Potter",
    "Hermione Granger", 
    "Ron Weasley",
    # ... etc
]

for char in characters:
    arguments = {
        "keywords": f"{char} Harry Potter face",
        "limit": 200,
        "print_urls": False,
        "format": "jpg",
        "size": "medium",
        "output_directory": "data/raw",
        "image_directory": char.lower().replace(" ", "_")
    }
    response.download(arguments)
```

### Script avec BeautifulSoup

```python
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import os

def download_images(query, num_images=200, output_dir="data/raw"):
    search_url = f"https://www.google.com/search?q={query}&tbm=isch"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extraire URLs d'images
    img_tags = soup.find_all('img')
    
    os.makedirs(output_dir, exist_ok=True)
    count = 0
    
    for img in img_tags[:num_images]:
        try:
            img_url = img.get('src') or img.get('data-src')
            if img_url:
                img_response = requests.get(img_url)
                image = Image.open(BytesIO(img_response.content))
                image.save(f"{output_dir}/image_{count:04d}.jpg")
                count += 1
        except Exception as e:
            print(f"Error downloading image: {e}")
            continue
    
    print(f"Downloaded {count} images")
```

---

## 📁 Organisation du dataset

### Structure recommandée

```
data/
├── raw/                           # Images brutes téléchargées
│   ├── harry_potter/
│   ├── hermione_granger/
│   └── ...
├── cleaned/                       # Images nettoyées
│   └── ...
├── train/                         # 70% - Entraînement
│   ├── harry_potter/
│   │   ├── harry_001.jpg
│   │   ├── harry_002.jpg
│   │   └── ... (~140 images)
│   └── ...
├── val/                          # 15% - Validation
│   └── ... (~30 images par personnage)
└── test/                         # 15% - Test
    └── ... (~30 images par personnage)
```

### Convention de nommage

```
[personnage]_[numéro].jpg

Exemples:
- harry_potter_0001.jpg
- hermione_granger_0042.jpg
- ron_weasley_0158.jpg
```

### Script de split automatique

```python
import os
import shutil
from pathlib import Path
import random

def split_dataset(source_dir, dest_dir, train_ratio=0.7, val_ratio=0.15):
    """
    Split dataset into train/val/test sets.
    """
    random.seed(42)
    
    for character_dir in Path(source_dir).iterdir():
        if not character_dir.is_dir():
            continue
            
        character_name = character_dir.name
        images = list(character_dir.glob('*.jpg'))
        random.shuffle(images)
        
        # Calculate splits
        n = len(images)
        train_n = int(n * train_ratio)
        val_n = int(n * val_ratio)
        
        train_images = images[:train_n]
        val_images = images[train_n:train_n + val_n]
        test_images = images[train_n + val_n:]
        
        # Create directories
        for split in ['train', 'val', 'test']:
            split_dir = Path(dest_dir) / split / character_name
            split_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy files
        for i, img in enumerate(train_images):
            shutil.copy(img, Path(dest_dir) / 'train' / character_name / f"{character_name}_{i:04d}.jpg")
        
        for i, img in enumerate(val_images):
            shutil.copy(img, Path(dest_dir) / 'val' / character_name / f"{character_name}_{i:04d}.jpg")
        
        for i, img in enumerate(test_images):
            shutil.copy(img, Path(dest_dir) / 'test' / character_name / f"{character_name}_{i:04d}.jpg")
        
        print(f"{character_name}: {len(train_images)} train, {len(val_images)} val, {len(test_images)} test")

# Usage
split_dataset('data/cleaned', 'data')
```

---

## 🧹 Nettoyage du dataset

### 1. Supprimer les duplicatas

```python
from PIL import Image
import imagehash
import os

def remove_duplicates(directory):
    """
    Remove duplicate images using perceptual hashing.
    """
    hashes = {}
    duplicates = []
    
    for img_path in Path(directory).rglob('*.jpg'):
        try:
            img = Image.open(img_path)
            img_hash = imagehash.average_hash(img)
            
            if img_hash in hashes:
                duplicates.append(img_path)
            else:
                hashes[img_hash] = img_path
        except Exception as e:
            print(f"Error processing {img_path}: {e}")
    
    # Remove duplicates
    for dup in duplicates:
        os.remove(dup)
        print(f"Removed duplicate: {dup}")
    
    print(f"Removed {len(duplicates)} duplicates")

remove_duplicates('data/raw/harry_potter')
```

### 2. Vérifier la qualité

```python
from PIL import Image

def check_image_quality(directory, min_size=(128, 128)):
    """
    Remove images below minimum size.
    """
    for img_path in Path(directory).rglob('*.jpg'):
        try:
            img = Image.open(img_path)
            if img.size[0] < min_size[0] or img.size[1] < min_size[1]:
                print(f"Removing {img_path}: size {img.size} < {min_size}")
                os.remove(img_path)
        except Exception as e:
            print(f"Error with {img_path}: {e}")
            os.remove(img_path)
```

### 3. Validation manuelle

- Parcourir les images visuellement
- Supprimer images floues, mal cadrées
- Vérifier que le bon personnage est présent
- Supprimer images avec watermarks

---

## 🔄 Preprocessing et augmentation

### Redimensionnement

```python
from PIL import Image
from pathlib import Path

def resize_images(directory, size=(128, 128)):
    """
    Resize all images to target size.
    """
    for img_path in Path(directory).rglob('*.jpg'):
        try:
            img = Image.open(img_path)
            img_resized = img.resize(size, Image.LANCZOS)
            img_resized.save(img_path)
        except Exception as e:
            print(f"Error resizing {img_path}: {e}")

resize_images('data/train', (128, 128))
```

### Data Augmentation

L'augmentation est gérée automatiquement par `ImageDataGenerator` dans le notebook, mais vous pouvez pré-générer des images:

```python
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
import numpy as np

datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

# Augmenter une image
img = load_img('data/train/harry_potter/harry_001.jpg')
x = img_to_array(img)
x = x.reshape((1,) + x.shape)

i = 0
for batch in datagen.flow(x, batch_size=1, save_to_dir='data/train/harry_potter',
                          save_prefix='aug', save_format='jpg'):
    i += 1
    if i > 5:  # Générer 5 variantes
        break
```

---

## ✅ Critères de qualité

### Checklist par image

- [ ] Résolution ≥ 128x128 pixels
- [ ] Visage clairement visible
- [ ] Bon éclairage (pas trop sombre/clair)
- [ ] Pas de watermark
- [ ] Format JPEG ou PNG
- [ ] Bon personnage labellisé
- [ ] Pas de duplicata

### Checklist globale

- [ ] 10 personnages complets
- [ ] ~200 images par personnage
- [ ] Variété d'angles (face, profil, 3/4)
- [ ] Variété d'expressions (sourire, sérieux, etc.)
- [ ] Variété de scènes (différents films/moments)
- [ ] Équilibre entre classes (±10%)
- [ ] Split train/val/test effectué
- [ ] Aucun overlap entre splits

---

## 🎯 Validation du dataset

### Statistiques

```python
import pandas as pd
from pathlib import Path

def dataset_statistics(data_dir):
    """
    Print dataset statistics.
    """
    stats = {}
    
    for split in ['train', 'val', 'test']:
        split_dir = Path(data_dir) / split
        stats[split] = {}
        
        for char_dir in split_dir.iterdir():
            if char_dir.is_dir():
                count = len(list(char_dir.glob('*.jpg')))
                stats[split][char_dir.name] = count
    
    df = pd.DataFrame(stats)
    df['Total'] = df.sum(axis=1)
    print(df)
    print(f"\nTotal images: {df['Total'].sum()}")
    
    return df

stats = dataset_statistics('data')
```

### Visualisation

```python
import matplotlib.pyplot as plt
import random

def visualize_samples(data_dir, split='train', n_samples=5):
    """
    Visualize random samples from each class.
    """
    split_dir = Path(data_dir) / split
    characters = [d.name for d in split_dir.iterdir() if d.is_dir()]
    
    fig, axes = plt.subplots(len(characters), n_samples, figsize=(15, 20))
    
    for i, char in enumerate(characters):
        char_dir = split_dir / char
        images = list(char_dir.glob('*.jpg'))
        samples = random.sample(images, min(n_samples, len(images)))
        
        for j, img_path in enumerate(samples):
            img = plt.imread(img_path)
            axes[i, j].imshow(img)
            axes[i, j].axis('off')
            if j == 0:
                axes[i, j].set_title(char, fontsize=10)
    
    plt.tight_layout()
    plt.savefig('dataset_samples.png')
    plt.show()

visualize_samples('data')
```

---

## 🛠️ Outils recommandés

### Python Libraries

```bash
pip install google-images-download
pip install pillow
pip install imagehash
pip install beautifulsoup4
pip install requests
pip install selenium  # Pour scraping dynamique
```

### Autres outils

- **Bulk Image Downloader** (Chrome extension)
- **FFmpeg** (extraction de frames vidéo)
- **ImageMagick** (manipulation d'images en batch)
- **LabelImg** (annotation manuelle si besoin)

---

## 📝 Checklist finale

Avant de commencer l'entraînement:

- [ ] 10 personnages collectés
- [ ] ~2000 images totales (200 par personnage)
- [ ] Images nettoyées (pas de duplicatas)
- [ ] Qualité vérifiée (taille, netteté)
- [ ] Labellisation correcte
- [ ] Split train/val/test (70/15/15)
- [ ] Aucun overlap entre splits
- [ ] Structure de dossiers conforme
- [ ] Statistiques vérifiées
- [ ] Samples visuels validés

---

## 💡 Conseils pratiques

✅ **Commencer petit** - Testez avec 50 images/personnage d'abord  
✅ **Variété > Quantité** - 150 images variées > 300 images similaires  
✅ **Qualité > Quantité** - Nettoyer plutôt que collecter plus  
✅ **Backup** - Sauvegarder dataset brut avant preprocessing  
✅ **Documentation** - Noter sources et méthodes de collecte  
✅ **Légalité** - Respecter copyrights et licences  

---

## ⚠️ Problèmes courants

**Trop de duplicatas**
→ Utiliser imagehash pour détection automatique

**Images basse résolution**
→ Filtrer par taille minimum avant collecte

**Mauvaise labellisation**
→ Validation manuelle après collecte automatique

**Déséquilibre entre classes**
→ Sous-échantillonner classe majoritaire ou sur-échantillonner minoritaire

**Overfitting sur test set**
→ S'assurer que test set n'a pas été vu durant validation

---

> 📊 *"Un bon dataset vaut mieux qu'un excellent modèle sur des données médiocres!"*
