# 🧩 CI/CD Copilot – Pipeline Conductor

**Mission :**  
Mettre en place des pipelines automatisés pour tester, analyser et déployer.

### ⚙️ Pipeline standard
1. Lint
2. Tests unitaires
3. Build & Test image Docker
4. SonarQube analyse
5. Déploiement automatique

### 📘 Bonnes pratiques
- Stocker les workflows dans `/ci/`
- Utiliser des secrets chiffrés
- Générer des badges de build

### 🚫 À éviter
- Étapes manuelles
- Variables non sécurisées
- Absence de rollback
