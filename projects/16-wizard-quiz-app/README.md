# 🧙‍♂️ TU ES UN SORCIER, HARRY ! - Quiz Mobile App

Application mobile cross-platform (Android/iOS) avec QCM de 20 questions pour déterminer votre type de sorcier.

## 🎯 Objectif

Créer une application mobile Flutter permettant de déterminer le type de sorcier d'un utilisateur à travers un questionnaire de 20 questions à choix multiples.

## 🚀 Lancement rapide

### Prérequis
- Flutter SDK (3.0+)
- Android Studio / Xcode
- Docker (pour le build)

### Installation locale

```bash
cd src/wizard_quiz
flutter pub get
flutter run
```

### Build avec Docker

```bash
docker compose -f docker-compose.snippet.yml up -d
```

## 📱 Génération des builds

### Android APK
```bash
cd src/wizard_quiz
flutter build apk --release
# APK généré dans : build/app/outputs/flutter-apk/app-release.apk
```

### iOS IPA
```bash
cd src/wizard_quiz
flutter build ios --release
# Nécessite un Mac avec Xcode
```

## 🧪 Tests

```bash
bash tests/test_smoke.sh
```

## 📚 Documentation

- [Rendu complet](docs/rendu.md)
- [Document de gamification](docs/gamification.md)
- [Prompts IA utilisés](docs/prompts_used.md)

## 🎮 Fonctionnalités

- ✅ 20 questions QCM thématiques Harry Potter
- ✅ 6 types de sorciers (Gryffindor, Slytherin, Ravenclaw, Hufflepuff, Auror, Mangemort)
- ✅ Système de scoring intelligent
- ✅ Animations et transitions fluides
- ✅ Design responsive
- ✅ Gamification (badges, progression)

## 🏗️ Architecture

```
src/wizard_quiz/
├── lib/
│   ├── main.dart              # Point d'entrée
│   ├── models/
│   │   ├── question.dart      # Modèle de question
│   │   └── wizard_type.dart   # Modèle de type de sorcier
│   ├── screens/
│   │   ├── welcome_screen.dart
│   │   ├── quiz_screen.dart
│   │   └── result_screen.dart
│   └── utils/
│       └── quiz_data.dart     # Données des questions
├── test/
│   └── widget_test.dart
├── pubspec.yaml
└── android/
    └── app/
        └── build.gradle
```
