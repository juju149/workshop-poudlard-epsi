# 🧾 Rendu – Défi 16 : "TU ES UN SORCIER, HARRY !"

## 🎯 Objectif

Application mobile cross-platform (Android/iOS) avec QCM de 20 questions pour déterminer le type de sorcier de l'utilisateur. L'application offre une expérience immersive inspirée de l'univers Harry Potter avec un système de scoring intelligent.

## 🧩 Architecture

### Services et modules
- **Frontend Flutter** : Application mobile cross-platform
- **Modèles de données** :
  - `Question` : Représente une question avec ses réponses
  - `WizardType` : Définit les 6 types de sorciers
  - `Answer` : Gère les scores associés à chaque réponse

### Structure du projet
```
wizard_quiz/
├── lib/
│   ├── main.dart                    # Point d'entrée
│   ├── models/
│   │   ├── question.dart            # Modèle Question/Answer
│   │   └── wizard_type.dart         # 6 types de sorciers
│   ├── screens/
│   │   ├── welcome_screen.dart      # Écran d'accueil
│   │   ├── quiz_screen.dart         # Quiz interactif
│   │   └── result_screen.dart       # Résultats détaillés
│   └── utils/
│       └── quiz_data.dart           # 20 questions QCM
├── test/
│   └── widget_test.dart
└── pubspec.yaml                     # Dépendances
```

### Flux utilisateur
1. **Écran d'accueil** : Présentation du quiz et des 6 types de sorciers
2. **Quiz** : 20 questions avec progression visuelle
3. **Résultats** : Type de sorcier déterminé + détail des scores

## ⚙️ Technologies utilisées

- **Flutter 3.0+** : Framework cross-platform
- **Dart** : Langage de programmation
- **Material Design** : Interface utilisateur
- **Animations Flutter** : Transitions fluides entre questions

### Dépendances principales
```yaml
dependencies:
  flutter:
    sdk: flutter
  cupertino_icons: ^1.0.2
```

## 🚀 Lancement rapide

### Installation locale

```bash
# Installer les dépendances
cd src/wizard_quiz
flutter pub get

# Lancer en mode debug
flutter run

# Lancer sur un émulateur Android spécifique
flutter run -d emulator-5554

# Lancer sur iOS Simulator
flutter run -d iPhone
```

### Build production

```bash
# Android APK
cd src/wizard_quiz
flutter build apk --release
# APK disponible : build/app/outputs/flutter-apk/app-release.apk

# Android App Bundle (pour Play Store)
flutter build appbundle --release

# iOS (nécessite macOS + Xcode)
flutter build ios --release
```

### Build avec Docker

```bash
docker compose -f docker-compose.snippet.yml up -d
```

## 🧪 Tests

```bash
# Tests unitaires et widgets
cd src/wizard_quiz
flutter test

# Script de vérification automatique
bash tests/test_smoke.sh
```

## 🎮 Fonctionnalités

### Types de sorciers (6)

1. **🦁 Gryffondor** - Courage et bravoure
2. **🐍 Serpentard** - Ambition et ruse
3. **🦅 Serdaigle** - Intelligence et sagesse
4. **🦡 Poufsouffle** - Loyauté et travail
5. **⚡ Auror** - Protection et justice
6. **💀 Mage Noir** - Puissance et mystère

### Questions QCM (20)

Les questions couvrent différents aspects :
- Qualités personnelles
- Réactions face aux situations
- Préférences magiques
- Ambitions et valeurs
- Choix moraux

### Système de scoring

- Chaque réponse attribue des points à un ou plusieurs types de sorciers
- Le type avec le plus de points est révélé
- Affichage du détail des scores en pourcentage

### Gamification

- ⏱️ Progression visuelle (barre de progression)
- 🎨 Thème dynamique selon le résultat
- ✨ Animations de transition entre questions
- 🏆 Écran de résultat célébratoire
- 📊 Graphique de répartition des scores
- 🔄 Possibilité de recommencer le quiz

## 💾 PRA / Backup

### Données
- Aucune donnée persistante stockée
- Quiz complet en local (pas de connexion requise)
- Possibilité d'ajouter SharedPreferences pour historique

### Stratégie de sauvegarde
- Code source sur GitHub
- APK/IPA archivés avec releases
- Documentation versionnée

## 📱 Compatibilité

- **Android** : API 21+ (Android 5.0 Lollipop)
- **iOS** : iOS 11.0+
- **Web** : Compatible (build web possible)

## 🎨 Design

### Palette de couleurs
- Fond sombre : `#1a1a2e` / `#16213e` / `#0f3460`
- Accent : `#e94560` (rouge-rose)
- Couleurs maisons selon résultat

### Typography
- Titres : Bold, 24-36px
- Corps : Regular, 14-18px
- Police système Material Design

## 🧠 Notes & Retours

### Points forts
✅ Interface intuitive et immersive  
✅ 20 questions variées et thématiques  
✅ 6 types de sorciers au lieu de 4 (dépassement des attentes)  
✅ Système de scoring sophistiqué  
✅ Animations fluides  
✅ Design responsive  
✅ Pas de dépendances externes complexes  

### Limitations actuelles
- Pas de sauvegarde de l'historique des quiz
- Questions en français uniquement
- Pas d'intégration réseaux sociaux pour partage

### Améliorations possibles
- 🌐 Internationalisation (i18n)
- 💾 Historique local des résultats
- 📤 Partage sur réseaux sociaux
- 🎵 Musique et effets sonores
- 🏅 Système de badges et achievements
- 👥 Mode multijoueur
- 📊 Analytics pour voir distribution des types
- 🎨 Personnalisation des avatars

## 📊 Métriques du projet

- **Lignes de code** : ~600 lignes Dart
- **Nombre de fichiers** : 8 fichiers principaux
- **Taille APK** : ~15-20 MB (release)
- **Temps de développement** : ~2-3 heures
- **Nombre de questions** : 20
- **Nombre de types** : 6

## 🔗 Liens utiles

- [Documentation Flutter](https://flutter.dev/docs)
- [Material Design Guidelines](https://material.io/design)
- [Harry Potter Wikia](https://harrypotter.fandom.com/)

---

> 🧙‍♂️ *"Le Choixpeau magique ne se trompe jamais... mais notre algorithme non plus !"*
