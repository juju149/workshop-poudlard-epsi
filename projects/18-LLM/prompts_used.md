# Historique des Prompts - Déploiement LLM Local

## Date : 16 octobre 2025

---

## 1. Demande initiale

**Prompt utilisateur :**
> Je veux déployer la plus petite version de ChatGPT en local c'est possible ?

**Réponse GitHub Copilot :**
Oui, il est possible de déployer une version locale d'un modèle similaire à ChatGPT, mais les modèles officiels d'OpenAI (GPT-3/4) ne sont pas disponibles pour une installation locale. Alternatives open source proposées :
- GPT-2 (OpenAI, version réduite)
- Llama 2 (Meta, plusieurs tailles)
- Mistral (Mistral AI, très léger et performant)
- Phi-2 (Microsoft, petit modèle performant)
- TinyLlama (très compact)

Recommandation : TinyLlama ou Mistral 7B pour un déploiement local simple.

---

## 2. Recherche du plus petit modèle GPT

**Prompt utilisateur :**
> Chat GPT y a pas plus petit que cette version ?

**Réponse GitHub Copilot :**
Oui, modèles plus petits que ChatGPT :
- **TinyLlama** (1,1B paramètres) : très léger
- **Phi-2** (2,7B paramètres, Microsoft) : performant et compact
- **GPT-2 Small** (124M paramètres, OpenAI) : très basique
- **DistilGPT2** (82M paramètres, HuggingFace) : version distillée, encore plus légère

Ces modèles fonctionnent sur un ordinateur classique sans GPU haut de gamme.

---

## 3. Version officielle la plus petite

**Prompt utilisateur :**
> Moi je veux la version officielle la plus petite

**Réponse GitHub Copilot :**
La version officielle la plus petite de la famille GPT proposée par OpenAI est **GPT-2 Small (124M paramètres)**. C'est le plus léger des modèles GPT disponibles publiquement par OpenAI pour une utilisation locale.

Options proposées :
1. Un script Python prêt à l'emploi pour lancer GPT-2 Small en local
2. Une interface web minimaliste pour chatter avec le modèle
3. Des instructions pour l'intégrer dans le projet actuel

---

## 4. Mise en place initiale

**Prompt utilisateur :**
> Aide moi à mettre en place cette version

**Réponse GitHub Copilot :**
Plan d'installation :
1. Installer les dépendances Python nécessaires (transformers, torch)
2. Créer un script Python pour utiliser GPT-2 Small en mode chat simple

Installation tentée via `install_python_packages` (annulée par l'utilisateur).

---

## 5. Création d'un environnement virtuel

**Prompt utilisateur :**
> on va créer un venv aussi

**Réponse GitHub Copilot :**
Étapes pour mettre en place GPT-2 Small dans un environnement virtuel :
1. Créer un venv dans `projects/18-LLM`
2. Activer le venv avec `source venv/bin/activate`
3. Installer les dépendances (`transformers`, `torch`)
4. Créer le script d'exemple

Commande exécutée : `python3 -m venv venv`

---

## 6. Suite de l'installation

**Prompt utilisateur :**
> c'est bon ensuite

**Réponse GitHub Copilot :**
Actions effectuées :
1. Installation des packages : `transformers` et `torch`
2. Création du fichier `gpt2_chat.py` avec un script de chat utilisant GPT-2 Small
3. Note sur les erreurs d'import (venv non activé dans l'éditeur)

Script créé avec fonction de chat simple utilisant GPT-2.

---

## 7. Création du requirements.txt

**Prompt utilisateur :**
> ajoute un requirements et installe tout

**Réponse GitHub Copilot :**
Actions effectuées :
1. Création du fichier `requirements.txt` avec :
   - transformers
   - torch
2. Installation via `pip install -r requirements.txt`
3. Téléchargement et installation réussis de tous les packages (PyTorch 2.9.0, Transformers 4.57.1, etc.)

---

## 8. Premier test - Bus Error

**Prompt utilisateur :**
> (Sortie d'erreur du terminal)
> [1] 30694 bus error python gpt2_chat.py

**Réponse GitHub Copilot :**
Diagnostic :
- "Bus error" indique un problème de mémoire ou d'incompatibilité
- Problème lié à Python 3.13 (très récent) avec PyTorch
- PyTorch et Transformers mieux supportés sur Python 3.10 ou 3.11

Solutions proposées :
1. Adapter le script pour forcer l'utilisation du CPU et corriger l'avertissement
2. Recréer le venv avec Python 3.10 ou 3.11

---

## 9. Tentative de correction

**Prompt utilisateur :**
> fais ça

**Réponse GitHub Copilot :**
Corrections apportées au script `gpt2_chat.py` :
1. Ajout de `model.to('cpu')` pour forcer l'utilisation du CPU
2. Ajout de `attention_mask = torch.ones_like(inputs)` pour éviter l'avertissement
3. Correction de l'indentation dans la fonction chat

Problème : le bus error persiste malgré les corrections.

---

## 10. Recherche d'un modèle plus petit

**Prompt utilisateur :**
> Je veux utiliser un Chat GPT2 Small pour faire une mini IA en locale, y a un modèle GPT plus petit ou pas ?

**Réponse GitHub Copilot :**
Modèles GPT plus petits que GPT-2 Small :
- **DistilGPT-2** (82M paramètres) - version distillée de GPT-2, plus légère et rapide
- **GPT-Neo 125M** (EleutherAI) - similaire à GPT-2 Small
- **Pythia 70M** (EleutherAI) - encore plus petit

Note : le bus error risque de persister avec Python 3.13.

Solutions proposées :
1. Utiliser DistilGPT-2
2. Changer vers Python 3.11
3. Utiliser Ollama (plus stable)

---

## 11. Confirmation du plus petit modèle officiel

**Prompt utilisateur :**
> Et le plus petit modèle GPT officiel c'est lequel ?

**Réponse GitHub Copilot :**
Le plus petit modèle GPT officiel d'OpenAI disponible publiquement est **DistilGPT-2** avec **82M de paramètres**.

Hiérarchie des modèles GPT officiels (du plus petit au plus grand) :
1. **DistilGPT-2** - 82M paramètres (le plus petit)
2. **GPT-2 Small** - 124M paramètres
3. **GPT-2 Medium** - 355M paramètres
4. **GPT-2 Large** - 774M paramètres
5. **GPT-2 XL** - 1,5B paramètres

---

## 12. Setup de DistilGPT-2

**Prompt utilisateur :**
> Okay aide moi à setup une version DistilGPT-2 de cette IA en local

**Réponse GitHub Copilot :**
Modifications apportées au script `gpt2_chat.py` :
1. Changement du modèle : `gpt2` → `distilgpt2`
2. Ajout d'informations sur le nombre de paramètres au démarrage
3. Mise à jour des messages de bienvenue

Résultat du test :
- Modèle téléchargé avec succès (353 MB)
- Chargement réussi : 81,912,576 paramètres
- **Bus error persiste** - problème de compatibilité Python 3.13 / PyTorch 2.9.0 / macOS ARM

---

## 13. Passage à Ollama

**Prompt utilisateur :**
> Oui aide moi

**Réponse GitHub Copilot :**
Solution proposée : installer **Ollama**, solution plus stable pour faire tourner des LLM en local sur Mac.

Plan :
1. Installer Ollama (via Homebrew)
2. Télécharger un petit modèle
3. Créer un script Python pour interagir avec Ollama

Découverte : Ollama est déjà installé (version 0.12.5) et Mistral (4.1 GB) est déjà disponible.

---

## 14. Recherche de GPT-2 sur Ollama

**Prompt utilisateur :**
> y a pas chatgpt2 avec DistilGPT ?

**Réponse GitHub Copilot :**
Non, Ollama n'a pas de modèle GPT-2 ou DistilGPT-2 officiel. Ollama se concentre sur des modèles open-source plus récents :
- **TinyLlama** (1.1B paramètres, ~600 MB) - le plus petit
- **Phi-2** (2.7B paramètres)
- **Mistral** (7B paramètres) - déjà installé
- **Llama 3.2** (plusieurs tailles)

Options proposées :
1. Résoudre le problème PyTorch en changeant vers Python 3.11
2. Utiliser TinyLlama avec Ollama (beaucoup plus stable)

---

## 15. Choix de TinyLlama

**Prompt utilisateur :**
> okay go tinyllama

**Réponse GitHub Copilot :**
Actions effectuées :
1. Téléchargement de TinyLlama via `ollama pull tinyllama` (637 MB)
2. Installation du package Python `ollama` via pip
3. Création du script `tinyllama_chat.py` avec :
   - Interface de chat interactive
   - Streaming des réponses en temps réel
   - Historique de conversation
   - Gestion des erreurs

**Fichiers créés :**
- `tinyllama_chat.py` - Script de chat avec TinyLlama
- `gpt2_chat.py` - Script avec DistilGPT-2 (pour réessayer plus tard)
- `requirements.txt` - Dépendances Python (transformers, torch, ollama)

**Avantages de TinyLlama via Ollama :**
✅ Fonctionne parfaitement sur Mac (pas de bus error)
✅ Mieux optimisé que GPT-2
✅ Meilleure qualité de réponses
✅ Streaming des réponses
✅ Historique de conversation

---

## Résumé de la solution finale

**Objectif initial :** Déployer la plus petite version de ChatGPT en local

**Solution finale :** TinyLlama (1.1B paramètres) via Ollama

**Raison du changement :**
- GPT-2 Small et DistilGPT-2 causent un "bus error" avec Python 3.13 sur macOS ARM
- TinyLlama via Ollama est plus stable et performant
- Meilleure expérience utilisateur avec streaming et historique

**Commande pour lancer :**
```bash
python3 tinyllama_chat.py
```

---

## Technologies utilisées

- **Python** : Langage de programmation
- **Ollama** : Serveur pour faire tourner des LLM en local
- **TinyLlama** : Modèle de langage (1.1B paramètres)
- **Bibliothèques Python** : ollama, transformers, torch
- **Environnement** : macOS ARM (Apple Silicon)

---

## Fichiers du projet

```
18-LLM/
├── venv/                    # Environnement virtuel Python
├── tinyllama_chat.py       # Script TinyLlama (fonctionnel) ✅
├── requirements.txt        # Dépendances Python
└── prompts_used.md        # Ce fichier
```
