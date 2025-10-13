# 🗺️ Parcours Utilisateur - Wizard Quiz App

## Vue d'ensemble du flux

```
┌─────────────────┐
│  Lancement App  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Écran d'Accueil │ ◄─────────────┐
│   (Welcome)     │                │
└────────┬────────┘                │
         │                         │
         │ [Clic "COMMENCER"]      │
         ▼                         │
┌─────────────────┐                │
│  Question 1/20  │                │
└────────┬────────┘                │
         │                         │
         ▼                         │
┌─────────────────┐                │
│  Question 2/20  │                │
└────────┬────────┘                │
         │                         │
         ▼                         │
       [...]                       │
         │                         │
         ▼                         │
┌─────────────────┐                │
│ Question 20/20  │                │
└────────┬────────┘                │
         │                         │
         │ [Dernière réponse]      │
         ▼                         │
┌─────────────────┐                │
│  Calcul Scores  │                │
└────────┬────────┘                │
         │                         │
         ▼                         │
┌─────────────────┐                │
│ Écran Résultat  │                │
│  + Type révélé  │                │
└────────┬────────┘                │
         │                         │
         │ [Clic "RECOMMENCER"]    │
         └─────────────────────────┘
```

## Écran 1 : Welcome Screen

```
╔═══════════════════════════════════════╗
║              ⚡                        ║
║                                       ║
║      TU ES UN SORCIER,                ║
║          HARRY !                      ║
║                                       ║
║  ┌─────────────────────────────┐     ║
║  │ 🧙‍♂️ Découvre ton type        │     ║
║  │    de sorcier                │     ║
║  │                              │     ║
║  │ Réponds à 20 questions       │     ║
║  │ pour découvrir quel type     │     ║
║  │ de sorcier sommeille en toi! │     ║
║  │                              │     ║
║  │ 6 types possibles :          │     ║
║  │ 🦁 Gryffondor • 🐍 Serpentard │     ║
║  │ 🦅 Serdaigle • 🦡 Poufsouffle │     ║
║  │ ⚡ Auror • 💀 Mage Noir       │     ║
║  └─────────────────────────────┘     ║
║                                       ║
║    ┌──────────────────────┐          ║
║    │ COMMENCER LE QUIZ ▶  │          ║
║    └──────────────────────┘          ║
║                                       ║
║        ⏱️ Environ 5 minutes           ║
╚═══════════════════════════════════════╝
```

**Éléments clés :**
- Logo/emoji central (⚡)
- Titre accrocheur
- Description courte et claire
- Liste des 6 types avec emojis
- Call-to-action visible (bouton rouge)
- Indication du temps nécessaire

**Émotions visées :** Curiosité, excitation

## Écran 2 : Quiz Screen

```
╔═══════════════════════════════════════╗
║ Question 7/20                     35% ║
║ [▓▓▓▓▓▓▓░░░░░░░░░░░░░] ──────────    ║
║                                       ║
║  ┌─────────────────────────────┐     ║
║  │                              │     ║
║  │ Quelle est votre qualité     │     ║
║  │      principale ?             │     ║
║  │                              │     ║
║  └─────────────────────────────┘     ║
║                                       ║
║    ┌──────────────────────┐          ║
║    │      Courage         │          ║
║    └──────────────────────┘          ║
║                                       ║
║    ┌──────────────────────┐          ║
║    │      Ambition        │          ║
║    └──────────────────────┘          ║
║                                       ║
║    ┌──────────────────────┐          ║
║    │    Intelligence      │          ║
║    └──────────────────────┘          ║
║                                       ║
║    ┌──────────────────────┐          ║
║    │      Loyauté         │          ║
║    └──────────────────────┘          ║
║                                       ║
╚═══════════════════════════════════════╝
```

**Éléments clés :**
- Barre de progression visible
- Compteur de question
- Question dans une card centrée
- 4 boutons de réponse espacés
- Design cohérent avec l'écran précédent

**Émotions visées :** Engagement, anticipation

## Écran 3 : Result Screen

```
╔═══════════════════════════════════════╗
║           ✨ 🎉 ✨                     ║
║                                       ║
║          Tu es un...                  ║
║                                       ║
║              🦁                       ║
║                                       ║
║    Sorcier de Gryffondor             ║
║                                       ║
║        🔴 Rouge et Or                 ║
║                                       ║
║  ┌─────────────────────────────┐     ║
║  │ 📜 Description               │     ║
║  │                              │     ║
║  │ Courageux, audacieux et      │     ║
║  │ chevaleresque                │     ║
║  │                              │     ║
║  │ Vous êtes brave, déterminé   │     ║
║  │ et prêt à défendre vos amis. │     ║
║  └─────────────────────────────┘     ║
║                                       ║
║  ┌─────────────────────────────┐     ║
║  │ ⭐ Sorciers célèbres          │     ║
║  │                              │     ║
║  │ Harry Potter, Hermione       │     ║
║  │ Granger, Albus Dumbledore    │     ║
║  └─────────────────────────────┘     ║
║                                       ║
║  ┌─────────────────────────────┐     ║
║  │ 📊 Détail des scores         │     ║
║  │                              │     ║
║  │ 🦁 Gryffondor  42 pts (35%)  │     ║
║  │ [▓▓▓▓▓▓▓░░░░░░░]             │     ║
║  │                              │     ║
║  │ 🐍 Serpentard  28 pts (23%)  │     ║
║  │ [▓▓▓▓░░░░░░░░░░]             │     ║
║  │                              │     ║
║  │ 🦅 Serdaigle   25 pts (21%)  │     ║
║  │ [▓▓▓░░░░░░░░░░░]             │     ║
║  │                              │     ║
║  │ ... (autres types)           │     ║
║  └─────────────────────────────┘     ║
║                                       ║
║    ┌──────────────────────┐          ║
║    │  🔄 RECOMMENCER      │          ║
║    └──────────────────────┘          ║
║                                       ║
╚═══════════════════════════════════════╝
```

**Éléments clés :**
- Célébration visuelle (confetti textuel)
- Emoji du type de sorcier (large)
- Nom du type
- Couleurs de la maison
- Description personnalisée
- Liste de sorciers célèbres
- Graphique des scores
- Bouton pour recommencer

**Émotions visées :** Satisfaction, validation, fierté

## Timeline typique

```
0:00 ────► Lancement de l'app
0:10 ────► Lecture de l'écran d'accueil
0:30 ────► Clic "Commencer le quiz"
0:31 ────► Question 1
0:45 ────► Question 2
...
4:30 ────► Question 19
4:45 ────► Question 20 (dernière)
5:00 ────► Calcul + Animation
5:05 ────► Révélation du type
5:10 ────► Lecture des détails
6:00 ────► Fin de session (ou recommencer)
```

**Durée moyenne totale :** 5-6 minutes

## Interactions utilisateur

### Touch Targets

Toutes les zones interactives respectent les guidelines :
- Taille minimale : 48x48 dp (Android) / 44x44 pt (iOS)
- Espacement : 8dp minimum entre éléments

### Feedback visuel

1. **Hover effect** : Changement de couleur au survol
2. **Press effect** : Légère réduction de taille
3. **Disabled state** : Opacité réduite

### Animations

```
Welcome → Quiz : Slide transition (300ms)
Quiz questions : Fade in/out (300ms)
Quiz → Result : Fade + Scale (500ms)
Progress bar : Linear interpolation
```

## Points de décision

### Point 1 : Commencer ou non ?

**Facteurs influençant :**
- ✅ Design attractif
- ✅ Temps estimé visible (5 min)
- ✅ Curiosité éveillée
- ❌ Trop long perçu
- ❌ Pas intéressé par le thème

### Point 2 : Continuer ou abandonner ?

**Facteurs influençant :**
- ✅ Progression visible
- ✅ Questions intéressantes
- ✅ Animations fluides
- ❌ Questions ennuyeuses
- ❌ Interruption externe

### Point 3 : Recommencer ou quitter ?

**Facteurs influençant :**
- ✅ Résultat satisfaisant
- ✅ Curiosité ("et si je réponds différemment ?")
- ✅ Comparaison avec amis
- ❌ Trop long
- ❌ Pas de variations perçues

## Métriques de succès par étape

| Étape | Métrique | Objectif |
|-------|----------|----------|
| Welcome | Taux de démarrage | > 80% |
| Question 5 | Taux de rétention | > 90% |
| Question 10 | Taux de rétention | > 80% |
| Question 20 | Taux de completion | > 70% |
| Result | Temps de lecture | > 30s |
| Retry | Taux de recommencement | > 30% |

## Personas

### Persona 1 : "Le Curieux"
**Profil :** Fan de Harry Potter, 18-25 ans  
**Motivation :** Découvrir sa maison  
**Comportement :** Lit tout, partage le résultat  
**Probabilité de retry :** 40%

### Persona 2 : "Le Rapide"
**Profil :** Utilisateur casual, 15-18 ans  
**Motivation :** Tuer le temps  
**Comportement :** Répond rapidement, lit en diagonale  
**Probabilité de retry :** 20%

### Persona 3 : "L'Analyste"
**Profil :** Adulte méticuleux, 25-35 ans  
**Motivation :** Comprendre le système de scoring  
**Comportement :** Lit tout, teste différentes réponses  
**Probabilité de retry :** 60%

## Optimisations UX appliquées

✅ **Chargement instantané** : Pas d'écran de loading  
✅ **Pas de connexion requise** : Expérience complète offline  
✅ **Pas de publicité** : Expérience fluide  
✅ **Dark mode** : Confort visuel  
✅ **Animations subtiles** : Pas de fatigue visuelle  
✅ **Texte lisible** : Contraste élevé, taille adaptée  
✅ **Feedback immédiat** : Réponse instantanée aux actions  

---

> 🧙‍♂️ *"L'UX est comme un sort d'Oubliettes : l'utilisateur ne doit jamais remarquer la complexité technique."*
