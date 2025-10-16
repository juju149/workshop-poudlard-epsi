# Reconnaissance de formules magiques Harry Potter
# Nécessite : pip install speechrecognition pyaudio


# IA de reconnaissance vocale pour formules magiques Harry Potter
# NLU/NLP/NLG : dataset local, similarité sémantique, génération de réponse
# Nécessite : pip install speechrecognition transformers torch

import speech_recognition as sr
from transformers import pipeline
import os

# Mini-dataset : exemples pour chaque formule
SPELLS_DATASET = {
    "Expelliarmus": [
        "expelliarmus", "désarmement", "je te désarme", "sort de désarmement"
    ],
    "Lumos": [
        "lumos", "allume la lumière", "éclaire", "fait de la lumière"
    ],
    "Alohomora": [
        "alohomora", "ouvre la porte", "déverrouille", "sort d'ouverture"
    ],
    "Wingardium Léviosa": [
        "wingardium leviosa", "fait léviter", "lève l'objet", "sort de lévitation"
    ],
    "Avada Kedavra": [
        "avada kedavra", "sort de mort", "tue", "sortilège de mort"
    ],
    "Expecto Patronum": [
        "expecto patronum", "invoque un patronus", "chasse les détraqueurs", "patronus"
    ],
    "Accio": [
        "accio", "viens à moi", "rapproche", "sort d'attraction"
    ],
    "Stupéfix": [
        "stupefy", "paralyse", "étourdit", "sort d'étourdissement"
    ]
}

# Réponses générées pour chaque formule (NLG)
SPELLS_RESPONSES = {
    "Expelliarmus": "Sort de désarmement lancé !",
    "Lumos": "La lumière jaillit au bout de ta baguette.",
    "Alohomora": "La porte s'ouvre comme par magie !",
    "Wingardium Léviosa": "L'objet s'élève doucement dans les airs.",
    "Avada Kedavra": "Un éclair vert fuse... (sort interdit !)",
    "Spero Patronum": "Un Patronus lumineux apparaît pour te protéger.",
    "Accio": "L'objet vient à toi !",
    "Stupéfix": "L'adversaire est étourdi sur le champ."
}

# Sorts offensifs
OFFENSIVE_SPELLS = ["Avada Kedavra", "Stupéfix", "Expelliarmus"]

# Réponse défensive
DEFENSE_RESPONSE = "Protego ! Bouclier magique activé pour te protéger."

# Pipeline NLP pour la similarité sémantique
nlp = pipeline("feature-extraction", model="sentence-transformers/all-MiniLM-L6-v2")
import numpy as np

def sentence_embedding(text):
    # Retourne l'embedding moyen de la phrase
    emb = nlp(text)
    return np.mean(emb[0], axis=0)

def recognize_spell(text):
    text = text.lower()
    text_emb = sentence_embedding(text)
    best_spell = None
    best_score = 0.0
    for spell, examples in SPELLS_DATASET.items():
        for ex in examples:
            ex_emb = sentence_embedding(ex)
            score = np.dot(text_emb, ex_emb) / (np.linalg.norm(text_emb) * np.linalg.norm(ex_emb))
            if score > best_score:
                best_score = score
                best_spell = spell
    # Seuil de confiance
    if best_score > 0.7:
        return best_spell, best_score
    return None, best_score

def main():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    def speak(text):
        os.system(f'say "{text}"')
    print("Bienvenue dans la reconnaissance vocale Harry Potter !")
    print("Dites une formule magique, ou 'quitter' pour arrêter.")
    while True:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Parlez maintenant...")
            audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language="fr-FR")
            print(f"Vous avez dit : {text}")
            if text.strip().lower() in ["quitter", "exit", "stop"]:
                print("Arrêt de l'application. À bientôt !")
                speak("Arrêt de l'application. À bientôt !")
                break
            spell, score = recognize_spell(text)
            if spell:
                print(f"Formule magique reconnue : {spell} (confiance {score:.2f})")
                # Ajout d'émotions dans la voix
                response = SPELLS_RESPONSES.get(spell, spell)
                print(f"Réponse : {response}")
                if spell in OFFENSIVE_SPELLS:
                    print(f"Réponse défensive : {DEFENSE_RESPONSE}")
                    speak(f"{response} Attention ! {DEFENSE_RESPONSE}")
                else:
                    speak(f"{response} Bravo, c'est réussi !")
            else:
                print("Aucune formule magique reconnue.")
                speak("Aucune formule magique reconnue.")
        except sr.UnknownValueError:
            print("Impossible de comprendre l'audio.")
            speak("Impossible de comprendre l'audio.")
        except sr.RequestError as e:
            print(f"Erreur du service de reconnaissance vocale : {e}")
            speak("Erreur du service de reconnaissance vocale.")

if __name__ == "__main__":
    main()
