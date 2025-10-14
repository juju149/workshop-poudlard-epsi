# CI/CD Workflow Documentation

Ce dossier contient le workflow GitHub Actions pour l’intégration et le déploiement continu du projet.

## Résumé du pipeline
- **Install dependencies** : Installation des dépendances Node.js dans `projects/13-cours-mcgonagall`.
- **Lint** : Vérification du code avec Airbnb.
- **Tests unitaires** : Exécution des tests Jest.
- **Build** : Construction du projet (Vite/Electron).
- **Docker** : Build et test de l’image Docker.
- **SonarQube** : Analyse de la qualité du code.
- **Déploiement** : Étape de déploiement (placeholder).

## Historique des prompts et actions

### Prompt 1
**Prompt** : Assurer l’intégralité du CI/CD de vos défis. Votre CI/CD doit contenir :
- Un lancement de tests unitaires.
- Un lancement de tests de non-régression.
- Une vérification de norme de code (Airbnb pour projet JS, PEP8 pour projet python).
- Un test de votre image docker.
- Une compilation de votre projet (si besoin).
- Implémentation de sonarQube et vérification de la qualité du projet.
- Déploiement du projet si toutes les étapes précédentes sont validées.
- Afin que ce défi soit validé il faut que cette CI/CD soit fonctionnelle et implémenté sur au moins un autre défi compatible avec l’implémentation de ce processus
**Action** : Création d’un workflow CI/CD complet avec toutes les étapes demandées, et adaptation pour d’autres projets compatibles.

### Prompt 2
**Prompt** : on fait toutes ces actions dans le dossier projects/13-cours-mcgonagall
**Action** : Ajout de working-directory à chaque étape du workflow
