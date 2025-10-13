#!/usr/bin/env python3
"""
Script d'inférence pour la reconnaissance de formules magiques.
Usage: python inference.py --audio path/to/audio.wav
"""

import argparse
import json
import numpy as np
import torch
import librosa
from transformers import Wav2Vec2ForSequenceClassification, Wav2Vec2FeatureExtractor
from pathlib import Path


class SpellRecognizer:
    """Classe pour la reconnaissance de formules magiques."""
    
    def __init__(self, model_path="../models/spell-recognition-final"):
        """
        Initialise le recognizer avec le modèle entraîné.
        
        Args:
            model_path: Chemin vers le modèle entraîné
        """
        self.model_path = Path(model_path)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Charge la configuration
        with open(self.model_path / "config.json", 'r') as f:
            self.config = json.load(f)
        
        self.spells = self.config['spells']
        self.id_to_spell = {int(k): v for k, v in self.config['id_to_spell'].items()}
        self.sample_rate = self.config['sample_rate']
        self.max_duration = self.config['max_duration']
        
        # Charge le modèle et le feature extractor
        print(f"Chargement du modèle depuis {self.model_path}...")
        self.feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(str(self.model_path))
        self.model = Wav2Vec2ForSequenceClassification.from_pretrained(str(self.model_path))
        self.model.to(self.device)
        self.model.eval()
        print(f"Modèle chargé sur {self.device}")
    
    def preprocess_audio(self, audio):
        """
        Prétraite l'audio pour l'inférence.
        
        Args:
            audio: Signal audio numpy array
            
        Returns:
            Audio prétraité
        """
        target_length = int(self.sample_rate * self.max_duration)
        
        if len(audio) > target_length:
            # Tronque
            audio = audio[:target_length]
        elif len(audio) < target_length:
            # Padding
            audio = np.pad(audio, (0, target_length - len(audio)), mode='constant')
        
        return audio
    
    def predict(self, audio_path=None, audio_array=None):
        """
        Prédit la formule magique à partir d'un fichier audio ou d'un array.
        
        Args:
            audio_path: Chemin vers le fichier audio (optionnel)
            audio_array: Array numpy du signal audio (optionnel)
            
        Returns:
            tuple: (formule_prédite, confiance, probabilités_toutes_formules)
        """
        # Charge l'audio
        if audio_path is not None:
            audio, sr = librosa.load(audio_path, sr=self.sample_rate)
        elif audio_array is not None:
            audio = audio_array
        else:
            raise ValueError("Fournissez soit audio_path soit audio_array")
        
        # Prétraite l'audio
        audio = self.preprocess_audio(audio)
        
        # Extrait les features
        inputs = self.feature_extractor(
            audio,
            sampling_rate=self.sample_rate,
            return_tensors="pt",
            padding=True
        )
        
        # Prédiction
        with torch.no_grad():
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            outputs = self.model(**inputs)
            logits = outputs.logits
            probabilities = torch.nn.functional.softmax(logits, dim=-1)
            predicted_id = torch.argmax(probabilities, dim=-1).item()
        
        predicted_spell = self.id_to_spell[predicted_id]
        confidence = probabilities[0][predicted_id].item()
        all_probs = {self.id_to_spell[i]: prob.item() 
                    for i, prob in enumerate(probabilities[0])}
        
        return predicted_spell, confidence, all_probs
    
    def predict_batch(self, audio_paths):
        """
        Prédit les formules pour plusieurs fichiers audio.
        
        Args:
            audio_paths: Liste de chemins vers les fichiers audio
            
        Returns:
            Liste de tuples (formule, confiance, probabilités)
        """
        results = []
        for audio_path in audio_paths:
            result = self.predict(audio_path=audio_path)
            results.append(result)
        return results


def main():
    """Fonction principale pour l'utilisation en ligne de commande."""
    parser = argparse.ArgumentParser(
        description="Reconnaissance de formules magiques Harry Potter"
    )
    parser.add_argument(
        '--audio',
        type=str,
        required=True,
        help="Chemin vers le fichier audio (.wav, .mp3, etc.)"
    )
    parser.add_argument(
        '--model',
        type=str,
        default="../models/spell-recognition-final",
        help="Chemin vers le modèle entraîné"
    )
    parser.add_argument(
        '--top-k',
        type=int,
        default=3,
        help="Nombre de prédictions à afficher"
    )
    
    args = parser.parse_args()
    
    # Initialise le recognizer
    recognizer = SpellRecognizer(model_path=args.model)
    
    # Fait la prédiction
    print(f"\n🔮 Analyse du fichier audio: {args.audio}")
    print("=" * 60)
    
    predicted_spell, confidence, all_probs = recognizer.predict(audio_path=args.audio)
    
    # Affiche le résultat principal
    print(f"\n✨ Formule détectée: {predicted_spell.upper()}")
    print(f"🎯 Confiance: {confidence:.2%}")
    
    # Affiche les top-k prédictions
    print(f"\n📊 Top {args.top_k} prédictions:")
    sorted_probs = sorted(all_probs.items(), key=lambda x: x[1], reverse=True)
    for i, (spell, prob) in enumerate(sorted_probs[:args.top_k], 1):
        bar = "█" * int(prob * 40)
        print(f"{i}. {spell:20s} {bar} {prob:.2%}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
