# 📊 Méthodologie de Création du Dataset

## 🎯 Objectif

Créer un dataset audio de qualité pour entraîner un modèle de reconnaissance vocale capable d'identifier 10 formules magiques de l'univers Harry Potter.

## 📋 Formules cibles

1. **Expelliarmus** - Sortilège de désarmement
2. **Lumos** - Sortilège de lumière
3. **Nox** - Éteint la lumière
4. **Wingardium Leviosa** - Sortilège de lévitation
5. **Alohomora** - Sortilège d'ouverture
6. **Expecto Patronum** - Invoque un patronus
7. **Avada Kedavra** - Sort impardonnable
8. **Stupefy** - Sortilège de stupéfixion
9. **Protego** - Bouclier protecteur
10. **Accio** - Sortilège d'attraction

## 🔬 Approches de collecte de données

### 1. Synthèse vocale (TTS) - Approche principale

#### Services recommandés

**Google Text-to-Speech (gTTS)**
```python
from gtts import gTTS
import os

spells = ["expelliarmus", "lumos", "nox", ...]

for spell in spells:
    for lang in ['en', 'en-uk', 'en-us', 'en-au']:
        tts = gTTS(spell, lang=lang)
        tts.save(f"data/raw/{spell}_{lang}.mp3")
```

**Amazon Polly** (qualité supérieure)
```python
import boto3

polly = boto3.client('polly')
voices = ['Matthew', 'Joanna', 'Brian', 'Amy', 'Emma']

for spell in spells:
    for voice in voices:
        response = polly.synthesize_speech(
            Text=spell,
            OutputFormat='mp3',
            VoiceId=voice
        )
        # Sauvegarde...
```

**ElevenLabs** (meilleure qualité, payant)
- Voix naturelles et expressives
- Contrôle de l'intonation
- API simple à utiliser

#### Avantages du TTS
✅ Génération rapide de nombreux échantillons
✅ Contrôle total sur la qualité
✅ Pas de bruit de fond
✅ Cohérence entre les échantillons

#### Inconvénients
❌ Peut manquer de naturel
❌ Intonation parfois robotique
❌ Variations limitées

### 2. Enregistrements humains - Approche idéale

#### Protocole d'enregistrement

**Matériel requis:**
- Microphone de qualité (Blue Yeti, Rode NT-USB, etc.)
- Environnement calme
- Pop filter (recommandé)
- Logiciel d'enregistrement (Audacity, OBS, etc.)

**Protocole:**
1. **Participants**: 20-30 personnes
   - Variété d'âges (20-60 ans)
   - Équilibre hommes/femmes
   - Différents accents si possible

2. **Sessions d'enregistrement**:
   - 5-10 répétitions par formule
   - Varier l'intonation (neutre, excité, sérieux)
   - Varier le volume (normal, chuchoté, crié)
   - Prendre des pauses entre les formules

3. **Configuration technique**:
   - Sample rate: 44100 Hz (on downsample à 16000 Hz après)
   - Format: WAV, mono
   - Bit depth: 16-bit minimum
   - Distance du micro: 15-30 cm

4. **Instructions aux participants**:
   ```
   "Prononcez la formule [spell] comme si vous étiez un sorcier
   qui lance le sort. Vous pouvez être neutre, excité, ou sérieux.
   Répétez 5 fois avec des intonations différentes."
   ```

#### Script d'enregistrement

```python
import sounddevice as sd
import soundfile as sf
import numpy as np

SAMPLE_RATE = 44100
DURATION = 3  # secondes

def record_spell(spell_name, speaker_id, repetition):
    print(f"Enregistrement de '{spell_name}' dans 3... 2... 1...")
    recording = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1
    )
    sd.wait()
    
    filename = f"data/raw/{spell_name}/speaker{speaker_id}_rep{repetition}.wav"
    sf.write(filename, recording, SAMPLE_RATE)
    print(f"✅ Sauvegardé: {filename}")

# Usage
for spell in spells:
    for speaker in range(1, 21):  # 20 speakers
        for rep in range(1, 6):  # 5 répétitions
            record_spell(spell, speaker, rep)
```

### 3. Extraction de médias existants

#### Sources potentielles
- Films Harry Potter (8 films)
- Jeux vidéo Harry Potter
- Audiobooks
- Fan-made content (avec permission)

#### Considérations légales
⚠️ **Important**: Respecter les droits d'auteur
- **Fair use éducatif**: Acceptable pour l'éducation et la recherche
- **Usage commercial**: Nécessite autorisation
- **Attribution**: Toujours citer les sources

#### Extraction audio

```python
import moviepy.editor as mp

def extract_spell_from_video(video_path, start_time, end_time, spell_name):
    """
    Extrait un clip audio d'une vidéo.
    """
    video = mp.VideoFileClip(video_path)
    audio = video.audio.subclip(start_time, end_time)
    audio.write_audiofile(f"data/raw/{spell_name}/movie_clip.wav")
    video.close()

# Exemple: extraire "Expelliarmus" du premier film
extract_spell_from_video(
    "harry_potter_1.mp4",
    start_time=(1, 23, 45),  # 1h 23m 45s
    end_time=(1, 23, 48),
    spell_name="expelliarmus"
)
```

## 🔄 Data Augmentation

### Techniques appliquées

#### 1. Ajout de bruit
```python
def add_noise(audio, noise_factor=0.005):
    """Ajoute du bruit gaussien."""
    noise = np.random.normal(0, noise_factor, len(audio))
    return audio + noise
```

**Types de bruit à ajouter:**
- Bruit blanc (général)
- Bruit ambiant (café, rue)
- Bruit électronique (micro)

#### 2. Pitch shifting
```python
import librosa

def pitch_shift(audio, sr, n_steps):
    """Change le pitch de ±n semi-tons."""
    return librosa.effects.pitch_shift(audio, sr=sr, n_steps=n_steps)

# Variations: -2, -1, +1, +2 semi-tons
```

**Simule:**
- Différentes voix (graves/aiguës)
- Différents âges
- Effets magiques

#### 3. Time stretching
```python
def time_stretch(audio, rate):
    """Accélère ou ralentit l'audio."""
    return librosa.effects.time_stretch(audio, rate=rate)

# Variations: 0.9x, 0.95x, 1.05x, 1.1x
```

**Simule:**
- Vitesse de parole différente
- Urgence/calme

#### 4. Réverbération
```python
import pyroomacoustics as pra

def add_reverb(audio, sr, room_dim=[10, 8, 3]):
    """Ajoute de la réverbération."""
    room = pra.ShoeBox(room_dim, fs=sr, max_order=3)
    room.add_source([2, 2, 1.5], signal=audio)
    room.add_microphone([5, 5, 1.5])
    room.simulate()
    return room.mic_array.signals[0, :]
```

**Simule:**
- Différents environnements (salle, extérieur)
- Scènes de combat magique

#### 5. Changement de volume
```python
def change_volume(audio, factor):
    """Augmente ou diminue le volume."""
    return audio * factor

# Variations: 0.7x, 0.85x, 1.15x, 1.3x
```

### Pipeline d'augmentation complet

```python
def augment_dataset(audio, sr):
    """
    Applique toutes les augmentations à un échantillon.
    Retourne une liste d'échantillons augmentés.
    """
    augmented = [audio]  # Original
    
    # Ajout de bruit
    for noise_factor in [0.003, 0.005, 0.01]:
        augmented.append(add_noise(audio, noise_factor))
    
    # Pitch shifting
    for n_steps in [-2, -1, 1, 2]:
        augmented.append(pitch_shift(audio, sr, n_steps))
    
    # Time stretching
    for rate in [0.9, 0.95, 1.05, 1.1]:
        stretched = time_stretch(audio, rate)
        # Ajuste la longueur
        if len(stretched) > len(audio):
            stretched = stretched[:len(audio)]
        else:
            stretched = np.pad(stretched, (0, len(audio) - len(stretched)))
        augmented.append(stretched)
    
    # Changement de volume
    for factor in [0.7, 0.85, 1.15]:
        augmented.append(change_volume(audio, factor))
    
    # Combinaisons (ex: bruit + pitch)
    noise_pitch = pitch_shift(add_noise(audio, 0.005), sr, 1)
    augmented.append(noise_pitch)
    
    return augmented
```

## 📐 Prétraitement

### 1. Normalisation

```python
def normalize_audio(audio):
    """Normalise l'audio entre -1 et 1."""
    return audio / np.max(np.abs(audio))
```

### 2. Resampling

```python
import librosa

def resample_audio(audio, orig_sr, target_sr=16000):
    """Resample à 16kHz (standard pour la parole)."""
    return librosa.resample(audio, orig_sr=orig_sr, target_sr=target_sr)
```

### 3. Padding/Truncation

```python
def fix_length(audio, target_length):
    """Fixe la longueur de l'audio."""
    if len(audio) > target_length:
        return audio[:target_length]
    else:
        return np.pad(audio, (0, target_length - len(audio)))
```

### 4. Filtrage

```python
def remove_silence(audio, sr, threshold=0.01):
    """Retire les silences au début et à la fin."""
    # Détecte les parties non-silencieuses
    non_silent = librosa.effects.split(audio, top_db=20)
    
    # Garde seulement la partie parlée
    if len(non_silent) > 0:
        start, end = non_silent[0][0], non_silent[-1][1]
        return audio[start:end]
    return audio
```

## 📊 Structure finale du dataset

```
data/
├── raw/                           # Données brutes
│   ├── expelliarmus/
│   │   ├── tts_google_en.wav
│   │   ├── tts_polly_matthew.wav
│   │   ├── speaker001_rep1.wav
│   │   ├── speaker001_rep2.wav
│   │   └── ...
│   ├── lumos/
│   └── ...
│
├── processed/                     # Données prétraitées
│   ├── train/
│   │   ├── expelliarmus/
│   │   │   ├── 0001.wav
│   │   │   ├── 0002.wav
│   │   │   └── ...
│   │   └── ...
│   └── test/
│       └── ...
│
└── metadata/
    ├── train_metadata.csv        # Label, speaker, duration, etc.
    └── test_metadata.csv
```

### Metadata format (CSV)

```csv
filename,spell,label,speaker_id,duration,augmentation,split
0001.wav,expelliarmus,0,speaker001,2.3,original,train
0002.wav,expelliarmus,0,speaker001,2.3,noise_0.005,train
0003.wav,expelliarmus,0,speaker001,2.3,pitch_+2,train
...
```

## 📈 Statistiques recommandées

### Dataset idéal

| Métrique | Valeur cible | Minimum acceptable |
|----------|--------------|-------------------|
| Échantillons par formule | 100-200 | 50 |
| Speakers uniques | 20-30 | 10 |
| Répétitions par speaker | 5-10 | 3 |
| Durée moyenne | 2-3s | 1-4s |
| Total d'échantillons (bruts) | 1000-2000 | 500 |
| Total (avec augmentation) | 5000-10000 | 2000 |

### Distribution train/test

- **Train**: 80% (avec augmentation complète)
- **Validation**: 10% (augmentation limitée)
- **Test**: 10% (pas d'augmentation)

**Important**: Les speakers du test set ne doivent PAS être dans le train set (split par speaker, pas par échantillon).

## ✅ Checklist de qualité

### Avant l'entraînement

- [ ] Tous les fichiers sont au même sample rate (16kHz)
- [ ] Tous les fichiers sont mono
- [ ] Durées cohérentes (1-4 secondes)
- [ ] Pas de silences au début/fin
- [ ] Volume normalisé
- [ ] Distribution équilibrée des classes
- [ ] Metadata complète et correcte
- [ ] Train/test split sans fuite de données

### Validation du dataset

```python
def validate_dataset(data_dir):
    """Valide la qualité du dataset."""
    issues = []
    
    for spell_dir in os.listdir(data_dir):
        spell_path = os.path.join(data_dir, spell_dir)
        files = os.listdir(spell_path)
        
        for file in files:
            filepath = os.path.join(spell_path, file)
            audio, sr = librosa.load(filepath)
            
            # Vérifie le sample rate
            if sr != 16000:
                issues.append(f"{file}: Wrong sample rate ({sr})")
            
            # Vérifie la durée
            duration = len(audio) / sr
            if duration < 0.5 or duration > 5:
                issues.append(f"{file}: Duration issue ({duration:.2f}s)")
            
            # Vérifie le volume
            max_amp = np.max(np.abs(audio))
            if max_amp < 0.1:
                issues.append(f"{file}: Too quiet ({max_amp:.3f})")
            elif max_amp > 1.0:
                issues.append(f"{file}: Clipping ({max_amp:.3f})")
    
    return issues
```

## 🚀 Pipeline automatisé

```python
def create_complete_dataset(spells, config):
    """
    Pipeline complet de création de dataset.
    """
    print("📊 Création du dataset...")
    
    # 1. Génération TTS
    print("1️⃣ Génération TTS...")
    generate_tts_samples(spells, config['tts_services'])
    
    # 2. Prétraitement
    print("2️⃣ Prétraitement...")
    preprocess_all_files(config['raw_dir'], config['sample_rate'])
    
    # 3. Augmentation
    print("3️⃣ Data augmentation...")
    augment_all_samples(config['raw_dir'], config['augmentation_params'])
    
    # 4. Split train/test
    print("4️⃣ Split train/test...")
    split_dataset(config['raw_dir'], config['processed_dir'], test_size=0.2)
    
    # 5. Validation
    print("5️⃣ Validation...")
    issues = validate_dataset(config['processed_dir'])
    if issues:
        print(f"⚠️ {len(issues)} issues trouvés")
        for issue in issues[:10]:
            print(f"  - {issue}")
    else:
        print("✅ Dataset validé!")
    
    # 6. Génération des métadonnées
    print("6️⃣ Génération des métadonnées...")
    generate_metadata(config['processed_dir'])
    
    print("🎉 Dataset créé avec succès!")
```

## 📚 Ressources et outils

### Bibliothèques Python
- `librosa` - Traitement audio
- `soundfile` - I/O audio
- `sounddevice` - Enregistrement
- `pydub` - Manipulation audio simple
- `pyroomacoustics` - Acoustique et réverbération

### Services TTS
- Google Text-to-Speech (gratuit, limité)
- Amazon Polly (payant, haute qualité)
- Microsoft Azure TTS (payant)
- ElevenLabs (payant, très haute qualité)

### Outils d'enregistrement
- Audacity (gratuit, open source)
- Adobe Audition (professionnel, payant)
- OBS Studio (gratuit, streaming)

## 💡 Conseils pratiques

1. **Commencez petit**: Créez d'abord un dataset de 50 échantillons pour tester le pipeline
2. **Itérez**: Entraînez un premier modèle, identifiez les faiblesses, complétez le dataset
3. **Documentez**: Gardez trace de chaque source de données
4. **Versionnez**: Utilisez Git LFS pour versionner les données
5. **Partagez**: Considérez publier le dataset (avec permissions appropriées)

---

✨ *"La qualité du dataset détermine la qualité du modèle"*
