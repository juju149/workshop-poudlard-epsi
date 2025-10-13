# POUDLARD À L’EPSI/WIS

**Workshop — 13/10/2025 → 17/10/2025**

> **Résumé**
> Document centralisé listant tous les défis du workshop "Poudlard à l'EPSI/WIS" (DOCKERWARTS). Chaque défi contient : description, exigences techniques, livrables attendus, critères d'évaluation et un emplacement pour le **N°** du groupe.

---

## 🚩 Informations générales

* **Dates du workshop :** 13/10/2025 — 17/10/2025
* **Niveau :** 5ème année EPSI/WIS
* **Thème global :** *POUDLARD À L’EPSI/WIS* (inspiration Harry Potter appliquée à des challenges informatiques et ingénierie)

---

## Table des matières

1. DOCKERWARTS
2. PRACADABRA (PRA / HAUTE DISPONIBILITÉ)
3. CAPE D’INVISIBILITÉ (intrusion éthique)
4. PROTEGO MAXIMA (défense aux intrusions)
5. CI/CD EXPRESS — VOIE 9¾
6. SPOOKEPSI (maquette site vitrine)
7. HARRY POTTER 9? (vidéo CGI)
8. OÙ EST LA CHAMBRE DES SECRETS ? (plan 3D animé)
9. LE PATRONUS D’EPSI (animation 2D)
10. OCULUS REPARO (cahier des charges transformation digitale)
11. LE COURS DE FILIUS FLITWICK (accompagnement au changement)
12. HARRY POTTER STARTER PACK
13. ON N’AVAIT PAS COURS AVEC MCGONAGALL? (exécutable emploi du temps)
14. LA BOITE MAGIQUE DE SERVERUS ROGUE (outil cross‑platform)
15. HEDWIGE (web app mail + OAuth)
16. "TU ES UN SORCIER, HARRY !" (application mobile QCM)
17. TABLEAU DES SCORES DE POUDLARD (app mobile points écoles)
18. LE CADET DE VOTRE ÉCOLE (déployer LLM local)
19. PROFESSOR DUMBLEDORE (reconnaissance vocale de formules)
20. IS IT YOU HARRY? (CNN reconnaissance personnages)
21. LE NIMBUS 3000 (benchmark d'optimizers)
22. LE PROCÈS DE J.K. ROWLING (data‑viz statistique corpus)
23. EASTER EGGS (section chaos)

---

# 1) DOCKERWARTS

**Objectif :** Monter une infrastructure dockerisée complète capable de supporter un projet *big data*.

**Composants minimaux exigés :**

* Outil de ticketing (ex. GLPI)
* Outil d’historisation / recherche (ElasticSearch)
* Monitoring (Grafana)
* Data lake (Cassandra)
* Pare‑feu (applicatif ou autre, justifier le choix)
* Mesures de haute disponibilité

**Livrables attendus :**

* Repo Git contenant :

  * Dockerfiles & `docker-compose` ou manifests Kubernetes (charts / manifests)
  * Scripts d’installation et d’orchestration
  * Fichiers de configuration pour ELK/Grafana/Cassandra/etc.
* Documentation d’architecture (diagrammes : infra, réseau, volumes, sauvegardes)
* Liste des commandes pour démarrer l’infra localement et en prod

**Critères d’évaluation :**

* Cohérence des choix technos
* Déployabilité (instructions claires)
* Observabilité (dashboards Grafana pertinents)
* Robustesse HA et gestion des volumes/persistences

**N° :**

---

# 2) PRACADABRA (PRA — Plan de Reprise d’Activité)

**Objectif :** Fournir un PRA permettant l’installation complète du SI et le lancement de tous les projets (dockerisation incluse).

**Exigences :**

* Sauvegarde des projets (backups automatisés)
* Scripts Ansible / Terraform pour automatiser le provisioning et l’infrastructure
* Garantir haute disponibilité (réplication, basculement)
* Monitoring & health checks

**Livrables :**

* Playbooks Ansible et / ou scripts Terraform
* Procédure de restauration (step by step)
* Diagramme PRA et justification des choix

**Remarques :**

* Le document PRA n’est pas obligatoire pour validation du défi, mais il doit être opérationnel et compatible avec au moins 1 autre défi.
* Le jury vérifiera la viabilité professionnelle du PRA.

**N° :**

---

# 3) CAPE D’INVISIBILITÉ (Intrusion éthique)

**Objectif :** Réaliser une intrusion éthique dans un système d’une école concurrente et fournir un rapport (sans collecter de données personnelles).

**Important / contraintes :**

* La collecte de données personnelles est **interdite** -> perte de points / disqualification.
* **Ne pas gêner** la progression des autres groupes.

**Livrables :**

* Rapport technique détaillant la méthode (outils, vecteurs, PoC), preuves non sensibles (logs anonymisés, hash), captures et timeline des actions
* Remédiations proposées

**N° :**

---

# 4) PROTEGO MAXIMA (Défense)

**Objectif :** Implémenter des défenses ingénieuses contre intrusions (TOUS les coups permis pour la défense dans le cadre éthique du workshop).

**Livrables :**

* Code/configurations des mécanismes de défense (IDS/IPS, WAF, honeypot, sandboxing, etc.)
* Documentation de chaque action
* Rapport d’intégration au SI (impact et compatibilité)

**Récompense :** Les défenses les plus ingénieuses seront mieux notées.

**N° :**

---

# 5) CI/CD EXPRESS — VOIE 9¾

**Objectif :** Assurer l’intégralité du pipeline CI/CD pour vos défis.

**Étapes obligatoires :**

* Lancer tests unitaires
* Lancer tests de non‑régression
* Vérification des normes de code (Airbnb pour JS, PEP8 pour Python)
* Test de l’image Docker
* Compilation (si applicable)
* Implémentation SonarQube et vérification qualité
* Déploiement automatisé si tout est validé

**Livrables :**

* Fichiers CI (ex : GitHub Actions / GitLab CI / Jenkinsfiles)
* Documentation d’utilisation et configuration SonarQube
* Preuve du pipeline fonctionnel (logs, captures, liens vers runs)

**Remarque :** Doit être appliqué à au moins un autre défi pour être validé.

**N° :**

---

# 6) SPOOKEPSI (Maquette site vitrine)

**Objectif :** Maquetter la page campus de l’EPSI revisitée façon Poudlard.

**Exigences :**

* Contenir tous les éléments présents sur `https://www.epsi.fr/campus/<votre_ville>`
* Responsive / mobile compatible
* Figma : maquette complète + charte graphique

**Charte graphique attendue :**

* Déclinaisons de couleurs
* Polices utilisées
* Boutons et états (hover, active, disabled)
* Animations
* Pictogrammes et logos
* Format des components (taille, spacing)

**Livrables :**

* Fichier Figma prêt à livrer au dev
* Document charte graphique

**N° :**

---

# 7) HARRY POTTER 9? (Vidéo CGI)

**Objectif :** Réaliser une vidéo de présentation (30s — 3min) entièrement générée en synthèse d’images.

**Exigences :**

* Utiliser des logiciels/engins tiers (animation 3D, compositing)
* Attention particulière au détail si durée courte

**Livrables :**

* Fichier vidéo final + assets sources (scènes, textures)
* Rapport technique sur la chaîne de production

**N° :**

---

# 8) OÙ EST LA CHAMBRE DES SECRETS ? (Plan 3D animé)

**Objectif :** Générer un objet 3D du plan de Poudlard et mettre en évidence la Chambre des Secrets (animation de rotation / zoom).

**Éléments obligatoires :**

* Bonne répartition des surfaces
* Murs et portes visibles

**Bonus :**

* Bureaux, tableaux, mobilier

**Livrables :**

* Fichier 3D exportable (GLTF/FBX) + animation
* Visualisation (vidéo ou viewer Web)

**N° :**

---

# 9) LE PATRONUS D’EPSI (Animation 2D)

**Objectif :** Créer le patronus de l’EPSI et une animation de chargement 2D (pour site ou logiciel).

**Bonus :** Intégration avec un autre défi (ex : page d’accueil SpookEPSI)

**Livrables :**

* Animation exportée (GIF / MP4 / Lottie) + fichier source

**N° :**

---

# 10) OCULUS REPARO (Cahier des charges)

**Objectif :** Rédiger un cahier des charges complet pour la transformation digitale d’un outil interne de Poudlard.

**Exigences :**

* Liste complète des fonctionnalités existantes
* Enquête (parties prenantes) et recommandations
* Axes commerciaux mis en avant

**Livrables :**

* Cahier des charges PDF
* Synthèse commerciale (pitch + ROI estimé)

**N° :**

---

# 11) LE COURS DE FILIUS FLITWICK (Accompagnement au changement)

**Objectif :** Définir un scénario d’accompagnement au changement pour une transformation digitale.

**Cadres acceptés :**

* Courbe de Kubler‑Ross
* Framework ADKAR (ou 7S McKinsey)

**Livrables :**

* Plan d’accompagnement détaillé
* Identification des parties prenantes
* Matrices des risques et actions d’atténuation

**N° :**

---

# 12) HARRY POTTER STARTER PACK

**Objectif :** Créer le starter pack d’un étudiant (original ou drôle).

**Livrables :**

* Présentation / visuel du pack
* Liste d’items et justification

**N° :**

---

# 13) ON N’AVAIT PAS COURS AVEC MCGONAGALL? (Exécutable emploi du temps)

**Objectif :** Générer un exécutable Windows qui récupère l’emploi du temps via l’API `wigorservices` (avec credentials).

**Exigences :**

* Tests unitaires (coverage > 80%)
* Documentation et justification technologique

**Livrables :**

* Exécutable Windows + code source
* Suite de tests & rapports de coverage

**N° :**

---

# 14) LA BOITE MAGIQUE DE SERVERUS ROGUE (Outil cross‑platform)

**Objectif :** Développer un outil cross‑platform (Linux/Windows) avec CMake pour rassembler sources et documents du Workshop.

**Livrables :**

* Binaire cross‑platform + CMakeLists
* Documentation d’usage

**N° :**

---

# 15) HEDWIGE (Web app mail + OAuth)

**Objectif :** Créer une web app pour réception/envoi d’e‑mails (mail étudiant) et connexion OAuth2 à services externes.

**Exigences :**

* Front + middleware (API)
* Tests unitaires

**Livrables :**

* Repo front + backend
* Documentation d’API et scénarios de test

**N° :**

---

# 16) "TU ES UN SORCIER, HARRY !" (App mobile QCM)

**Objectif :** Application mobile cross‑platform (Android/iOS) avec QCM 20 questions pour déterminer le type de sorcier.

**Exigences :**

* Au moins 4 types de sorciers
* Documenter gamification et chemins utilisateurs

**Livrables :**

* APK / IPA ou build expo + code source
* Document gamification

**N° :**

---

# 17) TABLEAU DES SCORES DE POUDLARD (App mobile native)

**Objectif :** Application native (Kotlin/Swift) pour compter les points des 4 écoles.

**Exigences :**

* Front, API, base de données (BaaS exclu)
* Tests unitaires (coverage > 80%)

**Livrables :**

* App native + API
* Documentation technique

**N° :**

---

# 18) LE CADET DE VOTRE ÉCOLE (Déployer LLM local)

**Objectif :** Déployer la plus petite version d’un LLM local sur une machine (modèle à faible paramètres).

**Livrables :**

* Script de déploiement local
* Guide d’utilisation

**N° :**

---

# 19) PROFESSEUR DUMBLEDORE (Reconnaissance vocale)

**Objectif :** Créer une IA de reconnaissance vocale capable d’identifier au moins 8 formules magiques (NLU/NLP).

**Livrables :**

* Notebook ou repo d’entraînement + dataset (méthodologie de création)
* Modèle entrainé et métriques

**N° :**

---

# 20) IS IT YOU HARRY? (CNN reconnaissance personnages)

**Objectif :** Réseau de neurones convolutif pour reconnaître au moins 10 personnages.

**Livrables :**

* Notebook Jupyter + dataset
* Rapport de validation

**N° :**

---

# 21) LE NIMBUS 3000 (Benchmark optimizers)

**Objectif :** Benchmark des optimizers (Adadelta, Adagrad, RMSProp, Adam, SGD, Adan, AdamW) sur un réseau donné.

**Livrables :**

* Rapport type papier avec expérimentations et analyses
* Scripts de reproduction

**N° :**

---

# 22) LE PROCÈS DE J.K. ROWLING (Data‑viz livre)

**Objectif :** Extraire statistiques textuelles des livres et visualiser tendances (ex : occurrences, prises de parole, actes discutables).

**Livrables :**

* Pipeline d’analyse (scripts)
* Visualisations (charts) et rapport méthodologique

**N° :**

---

# 23) EASTER EGGS (Section Chaos)

**Objectif :** Réalisations risquées / créatives (magie noire) — la plus grande prudence est requise.

**Exemples :**

* Faire planter une IA (preuve scientifique exigée)
* Reverse engineering de jeux de données (rapport complet exigé)
* Fork bomb expérimentale (ATTENTION : risques et interdictions à vérifier)

**N° :**

---

## Annexes & Checklist commune (à fournir par projet)

* README détaillé
* Diagrammes d’architecture
* Scripts d’installation / déploiement
* Tests unitaires & rapport coverage (si exigé)
* Documentation utilisateur & développeur
* Fichiers sources et exports (vidéo, 3D, binaire, etc.)

---

## Notes jury & critères transverses

* Pertinence technologique et professionnalisme
* Qualité de la documentation
* Reproductibilité (scripts / automation)
* Tests & qualité du code
* Originalité et créativité

---

> Si tu veux, je peux :
>
> * générer des templates README / Dockerfile / GitHub Actions pour n’importe quel défi
> * produire des diagrammes d’architecture (mermaid) prêts à intégrer
> * créer une checklist de validation pour le jury

*Document généré automatiquement — personnalise les sections N° avec vos numéros de groupe.*
