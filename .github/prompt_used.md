# Prompts utilisés pour le projet Hedwige Frontend

Ce fichier regroupe tous les prompts utilisés lors de la configuration et du développement CI/CD :

---

1. **CI/CD complet JS**
   > Assurer l’intégralité du CI/CD de vos défis. Votre CI/CD doit contenir : Un lancement de tests unitaires. Un lancement de tests de non-régression. Une vérification de norme de code (Airbnb pour projet JS, PEP8 pour projet python). Un test de votre image docker. Une compilation de votre projet (si besoin). Implémentation de sonarQube et vérification de la qualité du projet. Déploiement du projet si toutes les étapes précédentes sont validées.
   **Résultat :**
   → Création du workflow `.github/workflows/hedwige-frontend.yml` avec toutes les étapes demandées (tests unitaires, non-régression, lint Airbnb, build Docker, compilation, SonarCloud, déploiement).

2. **Déploiement GitHub Pages**
   > Assure moi un déploiement avec github pages
   **Résultat :**
   → Déploiement intégré dans le workflow via `peaceiris/actions-gh-pages@v4` sur le dossier `dist` du frontend.

3. **Changement de dossier frontend**
   > Nickel, mets toi dans le dossier /frontend dans le projet 15, src/frontend
   **Résultat :**
   → Toutes les étapes du workflow CI/CD sont maintenant exécutées dans `projects/15-hedwige/src/frontend`.

4. **Ajout des prompts dans un README**
   > Ajoute tous mes prompts dans un readme prompt_used dans le dossier .gitflow
   **Résultat :**
   → Création du fichier `.github/prompt_used.md` regroupant tous les prompts et leurs résultats.

---
