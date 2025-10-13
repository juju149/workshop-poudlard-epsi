# 💬 Prompts utilisés – Défi 16 : "TU ES UN SORCIER, HARRY !"

Ce document archive tous les prompts utilisés pour la génération de code, documentation et contenus de ce projet.

---

## 📋 Table des matières

1. [Prompts de planification](#prompts-de-planification)
2. [Prompts de code](#prompts-de-code)
3. [Prompts de documentation](#prompts-de-documentation)
4. [Prompts de contenu](#prompts-de-contenu)

---

## 🎯 Prompts de planification

### 🔹 Prompt 1 – Analyse des exigences

> "Analyse le défi 16 'TU ES UN SORCIER, HARRY !' du workshop Poudlard. Il faut créer une application mobile cross-platform avec un QCM de 20 questions pour déterminer le type de sorcier. Les exigences sont : au moins 4 types de sorciers, documenter la gamification et les chemins utilisateurs. Les livrables sont un APK/IPA, le code Flutter complet et un document de gamification. Propose une structure de projet suivant les standards AGENTS.md."

### 🔹 Prompt 2 – Architecture technique

> "Conçois l'architecture d'une application Flutter pour un quiz de personnalité Harry Potter. L'app doit gérer 20 questions, calculer des scores pour différents types de sorciers, et afficher des résultats personnalisés. Propose une structure de dossiers avec modèles, écrans et utilitaires."

---

## 💻 Prompts de code

### 🔹 Prompt 3 – Modèle de données WizardType

> "Crée une classe Dart 'WizardType' pour représenter un type de sorcier avec les propriétés : id, name, description, characteristics, famousWizards, houseColors, et emoji. Puis crée une classe statique 'WizardTypes' qui contient 6 types prédéfinis : Gryffondor, Serpentard, Serdaigle, Poufsouffle, Auror et Mage Noir, avec des descriptions complètes en français inspirées de l'univers Harry Potter."

### 🔹 Prompt 4 – Modèle Question et Answer

> "Crée deux classes Dart simples : 'Question' avec une propriété 'text' et une liste d'objets 'Answer', et 'Answer' avec une propriété 'text' et une Map 'scores' qui associe des identifiants de types de sorciers à des scores numériques."

### 🔹 Prompt 5 – Données des 20 questions

> "Génère 20 questions de quiz thématiques Harry Potter en français pour déterminer le type de sorcier. Chaque question doit avoir 4 réponses possibles, et chaque réponse doit attribuer des points à un ou plusieurs types parmi : gryffindor, slytherin, ravenclaw, hufflepuff, auror, dark_wizard. Les questions doivent couvrir : qualités personnelles, réactions face au danger, préférences magiques, ambitions, valeurs morales. Utilise le format de la classe Question créée précédemment."

### 🔹 Prompt 6 – Écran d'accueil (WelcomeScreen)

> "Crée un écran d'accueil Flutter (WelcomeScreen) pour une app de quiz Harry Potter. L'écran doit avoir : un fond dégradé sombre (bleu/noir), un titre 'TU ES UN SORCIER, HARRY !', une description du quiz avec les 6 types possibles affichés avec des emojis, un bouton CTA 'COMMENCER LE QUIZ' rouge-rose qui navigue vers QuizScreen, et une indication du temps nécessaire (5 minutes). Design moderne et immersif."

### 🔹 Prompt 7 – Écran de quiz (QuizScreen)

> "Crée un écran de quiz Flutter (QuizScreen) qui : affiche une barre de progression en haut, montre la question courante dans une card, affiche 4 boutons pour les réponses possibles, accumule les scores dans une Map, utilise des animations de transition (fade) entre les questions, et navigue vers ResultScreen à la fin des 20 questions en passant les scores. Le design doit être cohérent avec l'écran d'accueil (fond dégradé sombre)."

### 🔹 Prompt 8 – Écran de résultats (ResultScreen)

> "Crée un écran de résultats Flutter (ResultScreen) qui : calcule le type de sorcier avec le score le plus élevé, affiche un écran de célébration avec l'emoji du type, montre le nom et la description du type de sorcier, liste les sorciers célèbres associés, affiche un graphique de répartition des scores avec des barres de progression, adapte le thème de couleurs selon le type (rouge pour Gryffondor, vert pour Serpentard, etc.), et inclut un bouton 'RECOMMENCER' qui retourne à l'écran d'accueil."

### 🔹 Prompt 9 – Fichier main.dart

> "Crée le fichier main.dart d'une application Flutter avec un MaterialApp configuré avec : thème sombre (fond #1a1a2e), couleur primaire violet foncé, configuration des cards et boutons avec bordures arrondies, et WelcomeScreen comme écran d'accueil. Désactive le banner de debug."

### 🔹 Prompt 10 – Fichier pubspec.yaml

> "Crée un fichier pubspec.yaml pour une application Flutter nommée 'wizard_quiz' avec Flutter SDK 3.0+, les dépendances de base (flutter, cupertino_icons), les dev_dependencies (flutter_test, flutter_lints), et la configuration pour Material Design avec un dossier d'assets pour images et fonts."

---

## 📚 Prompts de documentation

### 🔹 Prompt 11 – README.md principal

> "Rédige un README.md professionnel pour une application Flutter de quiz Harry Potter. Inclus : objectif, instructions de lancement local et avec Docker, génération des builds APK/IPA, exécution des tests, liste des fonctionnalités (20 questions, 6 types, scoring intelligent, animations), architecture du projet avec arborescence, et liens vers la documentation complète. Style markdown propre avec emojis."

### 🔹 Prompt 12 – Document rendu.md

> "Rédige le document de rendu complet (docs/rendu.md) suivant le format standard AGENTS.md pour le défi 'TU ES UN SORCIER, HARRY !'. Inclus toutes les sections obligatoires : objectif, architecture (services, flux utilisateur), technologies utilisées, lancement rapide, tests, fonctionnalités (6 types de sorciers détaillés, 20 questions, scoring, gamification), compatibilité, design (palette de couleurs), notes et retours (points forts, limitations, améliorations possibles), et métriques du projet."

### 🔹 Prompt 13 – Document de gamification

> "Rédige un document de gamification complet et détaillé (docs/gamification.md) pour l'application quiz sorcier. Couvre : vue d'ensemble, objectifs de gamification (engagement initial, maintien attention, satisfaction finale), mécaniques de jeu (progression, scoring invisible, choix multiples, révélation progressive), parcours utilisateur en 4 phases (découverte, immersion, révélation, partage/rétention), psychologie de l'engagement (effet Barnum, biais de confirmation, identité sociale, curiosité, récompenses variables), métriques de succès (KPIs, indicateurs qualité, A/B tests), stratégies d'optimisation (court/moyen/long terme), éléments visuels, boucles d'engagement et chemins utilisateurs détaillés. Utilise des émojis, tableaux, diagrammes textuels. Format markdown avancé."

### 🔹 Prompt 14 – Notes de développement

> "Crée un fichier docs/notes.md avec des notes de développement incluant : choix techniques justifiés, difficultés rencontrées et solutions, optimisations effectuées, et pistes d'amélioration future."

---

## 🎨 Prompts de contenu

### 🔹 Prompt 15 – Descriptions des types de sorciers

> "Rédige des descriptions immersives et personnalisées pour 6 types de sorciers basés sur Harry Potter : Gryffondor (courage), Serpentard (ambition), Serdaigle (intelligence), Poufsouffle (loyauté), Auror (justice), et Mage Noir (pouvoir). Chaque description doit inclure : une phrase d'accroche, les caractéristiques principales, 3 sorciers célèbres, et les couleurs de la maison. Ton positif et valorisant, sauf pour Mage Noir (mystérieux mais pas négatif)."

### 🔹 Prompt 16 – Questions thématiques variées

> "Génère 20 questions de quiz variées sur l'univers Harry Potter qui permettent de déterminer la personnalité magique. Les questions doivent porter sur : qualités (bravoure, intelligence, loyauté, ambition), réactions face au danger, préférences magiques (sorts, créatures, matières), lieux favoris, ambitions personnelles, choix moraux, style de combat, reliques de la mort, carrières magiques, et vision du monde. Chaque question 4 choix équilibrés entre les 6 types."

### 🔹 Prompt 17 – Slogans et textes UI

> "Génère des textes courts et percutants pour l'interface de l'app quiz sorcier : titre principal ('TU ES UN SORCIER, HARRY !'), sous-titre accrocheur, description du quiz (2 phrases max), labels des boutons (commencer, suivant, recommencer), messages de progression ('Question X/20', 'X%'), texte de célébration pour les résultats, et phrases inspirantes de conclusion. Style Harry Potter, enthousiaste, en français."

---

## 🧪 Prompts de tests

### 🔹 Prompt 18 – Script de test smoke

> "Crée un script bash tests/test_smoke.sh qui vérifie : présence des fichiers Flutter essentiels (pubspec.yaml, lib/main.dart), structure des dossiers (lib/models, lib/screens, lib/utils), présence de tous les fichiers Dart nécessaires, et affiche un rapport de vérification avec émojis. Le script doit retourner exit code 0 si tout est OK, 1 sinon."

### 🔹 Prompt 19 – Tests unitaires Flutter

> "Crée des tests unitaires Flutter (test/widget_test.dart) pour tester : le chargement de WizardQuizApp, la présence des 6 types de sorciers dans WizardTypes, le chargement des 20 questions depuis QuizData, et la logique de calcul du type gagnant dans ResultScreen. Utilise flutter_test avec testWidgets et expect."

---

## 🐳 Prompts Docker

### 🔹 Prompt 20 – Dockerfile Flutter

> "Crée un Dockerfile pour build une application Flutter Android. Base image : Ubuntu avec Flutter SDK, Java, Android SDK. Le Dockerfile doit : installer les dépendances, copier le code source dans /app, exécuter 'flutter pub get', builder l'APK avec 'flutter build apk --release', et exposer l'APK en volume. Multi-stage si possible pour optimiser la taille."

### 🔹 Prompt 21 – docker-compose.snippet.yml

> "Crée un fichier docker-compose.snippet.yml pour builder l'application Flutter. Service 'flutter_build' basé sur le Dockerfile, avec volumes pour : code source (src/wizard_quiz), outputs (./build), et un service optionnel 'web_preview' avec nginx pour servir la version web sur port 8080."

---

## 📦 Prompts de build

### 🔹 Prompt 22 – Instructions build Android

> "Rédige des instructions détaillées pour builder l'APK Android d'une app Flutter : prérequis (Flutter SDK, Android Studio), commandes pour debug et release, signing de l'APK, optimisations (ProGuard, obfuscation), et troubleshooting des erreurs courantes."

### 🔹 Prompt 23 – Instructions build iOS

> "Rédige des instructions pour builder l'IPA iOS d'une app Flutter : prérequis (macOS, Xcode, Apple Developer account), configuration du certificat et provisioning profile, commandes Flutter build, archivage Xcode, et export IPA pour TestFlight ou App Store."

---

## 🎨 Prompts design

### 🔹 Prompt 24 – Palette de couleurs

> "Génère une palette de couleurs cohérente pour une app Harry Potter : fond sombre (bleu nuit), accent rouge-rose vif, et 6 couleurs pour chaque maison/type (rouge pour Gryffondor, vert pour Serpentard, bleu pour Serdaigle, jaune pour Poufsouffle, gris foncé pour Auror, noir-vert pour Mage Noir). Donne les codes hex."

### 🔹 Prompt 25 – Guide de style UI

> "Crée un guide de style UI pour l'app quiz sorcier : typographie (tailles, weights), espacements (padding, margins), bordures (radius), élévations (shadows), animations (durées, courbes), et règles de composition. Style moderne, immersif, accessible."

---

## 📊 Prompts analytics

### 🔹 Prompt 26 – Métriques et KPIs

> "Définis les KPIs pertinents pour mesurer le succès d'une app de quiz de personnalité : taux de démarrage, taux de completion, temps moyen, taux de recommencement, distribution des types de résultats, réponses par question, abandons par étape. Propose des objectifs réalistes."

---

## 🔧 Prompts d'optimisation

### 🔹 Prompt 27 – Optimisations performances

> "Liste les optimisations de performance pour une app Flutter de quiz : const constructors, lazy loading des données, optimisation des animations, réduction de la taille de l'APK, obfuscation du code, cache des assets, et state management efficace."

### 🔹 Prompt 28 – Accessibilité

> "Propose des améliorations d'accessibilité pour l'app quiz : labels sémantiques, contraste des couleurs, taille des zones tactiles, support lecteur d'écran, navigation clavier, et alternatives textuelles aux emojis."

---

## 📝 Notes sur l'utilisation des prompts

### Méthodologie

1. **Prompts itératifs** : Chaque prompt s'appuie sur les résultats des précédents
2. **Contexte explicite** : Toujours rappeler le contexte (Harry Potter, quiz, Flutter)
3. **Format structuré** : Demander des formats précis (classes Dart, markdown, etc.)
4. **Langage** : Français pour le contenu, Dart/Flutter pour le code

### Bonnes pratiques

- ✅ Spécifier le langage de programmation et framework
- ✅ Donner des exemples de structure attendue
- ✅ Indiquer les contraintes techniques (Flutter 3.0+, Material Design)
- ✅ Préciser le ton et style (professionnel, immersif, etc.)
- ✅ Demander des commentaires dans le code si nécessaire

### Outils IA utilisés

- **GitHub Copilot** : Génération de code Dart/Flutter
- **ChatGPT** : Documentation, contenu, architecture
- **Claude** : Révision et amélioration du contenu

---

> 🧙‍♂️ *"Un bon prompt est comme un sort bien formulé : précis, intentionnel et puissant."*
