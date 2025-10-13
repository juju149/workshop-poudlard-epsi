# Guide d'installation et de build

## 🚀 Installation locale

### Prérequis

1. **Flutter SDK** (version 3.0 ou supérieure)
   ```bash
   # Télécharger depuis https://flutter.dev/docs/get-started/install
   # Ou avec snap (Linux)
   sudo snap install flutter --classic
   ```

2. **Android Studio** (pour Android)
   - Télécharger depuis https://developer.android.com/studio
   - Installer Android SDK
   - Configurer un émulateur

3. **Xcode** (pour iOS, macOS uniquement)
   - Installer depuis Mac App Store
   - Installer Command Line Tools : `xcode-select --install`

### Configuration

```bash
# Vérifier l'installation Flutter
flutter doctor

# Accepter les licences Android
flutter doctor --android-licenses

# Configurer Flutter
flutter config --android-sdk /path/to/android/sdk
```

### Installation du projet

```bash
# Cloner le repository
git clone https://github.com/juju149/workshop-poudlard-epsi.git
cd workshop-poudlard-epsi/services/wizard_quiz_app/src/wizard_quiz

# Installer les dépendances
flutter pub get
```

## 📱 Lancement en développement

### Sur émulateur Android

```bash
# Lister les émulateurs disponibles
flutter emulators

# Lancer un émulateur
flutter emulators --launch <emulator_id>

# Lancer l'application
flutter run
```

### Sur device Android physique

```bash
# Activer le mode développeur sur le téléphone
# Activer le débogage USB
# Connecter via USB

# Vérifier que le device est détecté
flutter devices

# Lancer l'application
flutter run
```

### Sur iOS Simulator (macOS uniquement)

```bash
# Ouvrir le simulateur
open -a Simulator

# Lancer l'application
flutter run
```

### Sur iOS device physique (macOS uniquement)

```bash
# Nécessite un compte Apple Developer
# Configurer le signing dans Xcode

flutter run
```

## 🏗️ Build production

### Android APK (release)

```bash
cd src/wizard_quiz

# Build APK
flutter build apk --release

# APK généré ici :
# build/app/outputs/flutter-apk/app-release.apk
```

### Android App Bundle (pour Play Store)

```bash
flutter build appbundle --release

# Bundle généré ici :
# build/app/outputs/bundle/release/app-release.aab
```

### iOS (macOS uniquement)

```bash
# Build iOS
flutter build ios --release

# Ensuite, utiliser Xcode pour archiver et exporter l'IPA
```

### Build Web

```bash
flutter build web --release

# Files générés dans : build/web/
```

## 🐳 Build avec Docker

### Build APK Android

```bash
cd services/wizard_quiz_app

# Build l'image et générer l'APK
docker compose -f docker-compose.snippet.yml up flutter_build

# L'APK sera dans : build/app/outputs/flutter-apk/
```

### Preview Web

```bash
# Lancer le service web
docker compose -f docker-compose.snippet.yml up web_preview

# Ouvrir dans le navigateur :
# http://localhost:8080
```

## 🔧 Configuration avancée

### Signing Android

1. Créer un keystore :
```bash
keytool -genkey -v -keystore ~/wizard-quiz-key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias wizard-quiz
```

2. Créer `android/key.properties` :
```properties
storePassword=<password>
keyPassword=<password>
keyAlias=wizard-quiz
storeFile=/path/to/wizard-quiz-key.jks
```

3. Modifier `android/app/build.gradle` :
```gradle
def keystoreProperties = new Properties()
def keystorePropertiesFile = rootProject.file('key.properties')
if (keystorePropertiesFile.exists()) {
    keystoreProperties.load(new FileInputStream(keystorePropertiesFile))
}

android {
    ...
    signingConfigs {
        release {
            keyAlias keystoreProperties['keyAlias']
            keyPassword keystoreProperties['keyPassword']
            storeFile keystoreProperties['storeFile'] ? file(keystoreProperties['storeFile']) : null
            storePassword keystoreProperties['storePassword']
        }
    }
    buildTypes {
        release {
            signingConfig signingConfigs.release
        }
    }
}
```

### Obfuscation

Le code Dart est automatiquement obfusqué en mode release. Pour plus de sécurité :

```bash
flutter build apk --release --obfuscate --split-debug-info=build/debug-info
```

### Optimisation de la taille

```bash
# Build APK split par architecture (génère plusieurs APK plus légers)
flutter build apk --release --split-per-abi

# Résultat :
# - app-armeabi-v7a-release.apk
# - app-arm64-v8a-release.apk
# - app-x86_64-release.apk
```

## 🧪 Tests

### Tests unitaires

```bash
flutter test
```

### Tests d'intégration

```bash
flutter test integration_test/
```

### Coverage

```bash
flutter test --coverage
genhtml coverage/lcov.info -o coverage/html
open coverage/html/index.html
```

## 📊 Analyse

### Analyse statique

```bash
flutter analyze
```

### Formattage

```bash
flutter format lib/
```

## 🚀 Publication

### Google Play Store

1. Créer un compte Google Play Developer
2. Build App Bundle : `flutter build appbundle --release`
3. Upload sur Google Play Console
4. Remplir les informations de l'app
5. Soumettre pour review

### Apple App Store

1. Créer un compte Apple Developer
2. Build iOS : `flutter build ios --release`
3. Utiliser Xcode pour archiver
4. Upload via App Store Connect
5. Soumettre pour review

## 🔍 Dépannage

### Problème : Flutter command not found

```bash
# Ajouter Flutter au PATH
export PATH="$PATH:`pwd`/flutter/bin"
```

### Problème : Android licenses not accepted

```bash
flutter doctor --android-licenses
```

### Problème : Gradle build failed

```bash
cd android
./gradlew clean
cd ..
flutter clean
flutter pub get
```

### Problème : iOS build failed

```bash
cd ios
pod install
cd ..
flutter clean
flutter run
```

### Problème : Out of memory during build

```bash
# Augmenter la mémoire Gradle
# Modifier android/gradle.properties
org.gradle.jvmargs=-Xmx4g
```

## 📚 Ressources

- [Flutter Documentation](https://flutter.dev/docs)
- [Android Developer Guide](https://developer.android.com/)
- [iOS Developer Guide](https://developer.apple.com/)
- [Flutter DevTools](https://flutter.dev/docs/development/tools/devtools)
