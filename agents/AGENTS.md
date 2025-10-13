# 🧠 AGENTS.md — Dockerwarts / Standard de Production

> *“Un bon sorcier suit toujours le même rituel avant de lancer un sort.”*

Ce document définit **le protocole standard** que chaque agent (humain ou IA) doit suivre pour produire, documenter, tester et livrer **tout défi du Workshop**.
L’objectif : garantir un rendu **propre, cohérent, automatisé et uniformisé**.

---

## 🪄 SOMMAIRE

1. 🎯 Objectif général
2. 📦 Structure type d’un projet
3. 👤 Rôles des agents
4. 🧾 Format de documentation standard
5. 💬 Prompts IA standardisés
6. 🧪 Stratégie de test
7. 🚀 CI/CD simplifié
8. 🗂️ Checklist de rendu final
9. 📘 Exemple de projet complet
10. ⚙️ Commandes Makefile globales

---

## 🎯 Objectif général

Chaque défi doit être :

* **Autonome** (dockerisable et testable seul)
* **Documenté** (README clair + rendu détaillé)
* **Testé** (script de vérification automatique)
* **Reproductible** (avec `.env` et commandes simples)
* **Traçable** (sources, prompts et logs d’exécution)

---

## 📦 Structure type d’un projet

```
projects/[numero]-[nom-raccourci]/
├── Dockerfile
├── docker-compose.snippet.yml
├── README.md
├── docs/
│   ├── rendu.md
│   ├── prompts_used.md
│   └── notes.md
├── tests/
│   ├── test_smoke.sh
│   └── test_integration.sh
└── src/
    └── ...
```

### 📘 Règles :

* **Convention de nommage :** `projects/[numero de defi]-[nom du defi raccourci avec mots séparés par des tirets]`
  * Exemples : `14-boite-magique`, `16-wizard-quiz-app`
* **`README.md`** → résumé technique et lancement rapide
* **`docs/rendu.md`** → document final pour le jury
* **`docs/prompts_used.md`** → tous les prompts IA utilisés
* **`tests/`** → scripts bash ou pytest selon le langage
* **`src/`** → code source unique et documenté

---

## � Liste des défis et noms de dossiers

Voici la liste des défis avec leurs noms de dossiers proposés selon la convention `projects/[numero]-[nom-raccourci]` :

1. **DOCKERWARTS** → `1-dockerwarts`
2. **PRACADABRA** → `2-pracadabra`
3. **CAPE D’INVISIBILITÉ** → `3-cape-dinvisibilite`
4. **PROTEGO MAXIMA** → `4-protego-maxima`
5. **CI/CD EXPRESS — VOIE 9¾** → `5-cicd-express-voie-974`
6. **SPOOKEPSI** → `6-spookepsi`
7. **HARRY POTTER 9?** → `7-harry-potter-9`
8. **OÙ EST LA CHAMBRE DES SECRETS ?** → `8-chambre-des-secrets`
9. **LE PATRONUS D’EPSI** → `9-patronus-epsi`
10. **OCULUS REPARO** → `10-oculus-reparo`
11. **LE COURS DE FILIUS FLITWICK** → `11-cours-filius-flitwick`
12. **HARRY POTTER STARTER PACK** → `12-harry-potter-starter-pack`
13. **ON N’AVAIT PAS COURS AVEC MCGONAGALL?** → `13-cours-mcgonagall`
14. **LA BOITE MAGIQUE DE SERVERUS ROGUE** → `14-boite-magique`
15. **HEDWIGE** → `15-hedwige`
16. **"TU ES UN SORCIER, HARRY !"** → `16-wizard-quiz-app`
17. **TABLEAU DES SCORES DE POUDLARD** → `17-tableau-scores-poudlard`
18. **LE CADET DE VOTRE ÉCOLE** → `18-cadet-ecole`
19. **PROFESSEUR DUMBLEDORE** → `19-professeur-dumbledore`
20. **IS IT YOU HARRY?** → `20-is-it-you-harry`
21. **LE NIMBUS 3000** → `21-nimbus-3000`
22. **LE PROCÈS DE J.K. ROWLING** → `22-proces-jk-rowling`
23. **EASTER EGGS** → `23-easter-eggs`

---

## �👤 Rôles des agents

| Rôle                       | Objectif                                         | Dossier / Action          |
| -------------------------- | ------------------------------------------------ | ------------------------- |
| **Infrastructure Copilot** | Crée et maintient les Dockerfiles & Compose      | `/infra/` & `/projects/*` |
| **Documentation Copilot**  | Rédige les docs et standardise les rendus        | `/docs/`                  |
| **Test Copilot**           | Gère les tests automatiques (smoke, integration) | `/tests/`                 |
| **Prompt Copilot**         | Archive et reformule les prompts IA              | `/docs/prompts_used.md`   |
| **Design Copilot**         | Crée les visuels et maquettes                    | `/design/`                |
| **Project Lead**           | Valide cohérence + intégration globale           | racine du repo            |

---

## 🧾 Format de documentation standard

Chaque `docs/rendu.md` suit ce gabarit **obligatoire** 👇

````markdown
# 🧾 Rendu – [Nom du défi]

## 🎯 Objectif
Décrire en une phrase l’objectif principal du projet.

## 🧩 Architecture
- Liste des services ou modules
- Diagramme (optionnel)
- Ports et dépendances

## ⚙️ Technologies utilisées
- Docker / Compose
- [Langage ou Framework]
- [Librairies principales]

## 🚀 Lancement rapide
```bash
docker compose -f docker-compose.snippet.yml up -d
````

## 🧪 Tests

```bash
bash tests/test_smoke.sh
```

## 💾 PRA / Backup

Résumé des stratégies de sauvegarde et reprise (PRA).

## 🧠 Notes & Retours

Idées, limites, et perspectives d’amélioration.

````

---

## 💬 Prompts IA standardisés

Chaque défi doit inclure dans `docs/prompts_used.md` **tous les prompts** ayant servi à générer :
- du code  
- des textes  
- de la documentation  
- des schémas  
- des musiques ou visuels IA

### Exemple :
```markdown
# 💬 Prompts utilisés – Défi DOCKERWARTS

### 🔹 Prompt 1 – Création du docker-compose
> “Écris un docker-compose complet pour un projet Big Data incluant GLPI, Grafana, ElasticSearch et Cassandra, avec monitoring Grafana.”

### 🔹 Prompt 2 – Génération du README
> “Crée un README clair et professionnel expliquant comment lancer et monitorer le projet Dockerwarts.”

### 🔹 Prompt 3 – Tests automatiques
> “Écris un test bash minimal qui vérifie le démarrage des containers et leur arrêt sans erreur.”
````

---

## 🧪 Stratégie de test

Chaque projet doit contenir **au moins 2 niveaux de tests :**

| Type                 | Fichier                     | Objectif                                               |
| -------------------- | --------------------------- | ------------------------------------------------------ |
| **Smoke Test**       | `tests/test_smoke.sh`       | Vérifie que le projet se lance et se stoppe sans crash |
| **Integration Test** | `tests/test_integration.sh` | Vérifie qu’un service communique bien avec un autre    |

### Exemple de test :

```bash
#!/bin/bash
set -e
echo "🚀 Lancement du projet..."
docker compose -f docker-compose.snippet.yml up -d
sleep 10
echo "✅ Containers actifs :"
docker ps
echo "🧪 Test d’accès HTTP"
curl -f http://localhost:3000 || exit 1
docker compose -f docker-compose.snippet.yml down -v
echo "🎉 Tous les tests sont passés avec succès"
```

---

## 🚀 CI/CD simplifié

**CI globale** : `ci/pipeline.yml`

* Exécute automatiquement les tests de chaque projet.
* Vérifie les Dockerfile (`hadolint`), le code (`lint`), et la documentation.
* Génère un artefact zip avec `docs/rendu.md` + logs.

### Exemple de section CI :

```yaml
jobs:
  build-test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        project: [1-dockerwarts, 2-pracadabra, 4-protego-maxima]
    steps:
      - uses: actions/checkout@v4
      - run: bash projects/${{ matrix.project }}/tests/test_smoke.sh
```

---

## 🗂️ Checklist de rendu final

| Étape | Élément                  | Fichier / Action             | Statut |
| ----- | ------------------------ | ---------------------------- | ------ |
| ✅     | Documentation complète   | `docs/rendu.md`              |        |
| ✅     | Prompts IA archivés      | `docs/prompts_used.md`       |        |
| ✅     | Dockerfile fonctionnel   | `projects/<numero>-<nom>/Dockerfile` |        |
| ✅     | Compose testé            | `docker-compose.snippet.yml` |        |
| ✅     | Tests automatisés        | `tests/test_smoke.sh`        |        |
| ✅     | PRA et backup notés      | `docs/pra.md`                |        |
| ✅     | Capture d’écran ou vidéo | `/docs/screens/`             |        |

---

## 📘 Exemple de projet complet

```
projects/15-hedwige/
├── Dockerfile
├── docker-compose.snippet.yml
├── README.md
├── docs/
│   ├── rendu.md
│   ├── prompts_used.md
│   └── notes.md
├── tests/
│   ├── test_smoke.sh
│   └── test_integration.sh
└── src/
    ├── app.py
    └── requirements.txt
```

* Lancement : `docker compose -f docker-compose.snippet.yml up -d`
* Test : `bash tests/test_smoke.sh`
* Rendu final : `/docs/rendu.md`
* Historique IA : `/docs/prompts_used.md`

---

## ⚙️ Commandes Makefile globales

```makefile
up-%:
	docker compose -f projects/$*/docker-compose.snippet.yml up -d

down-%:
	docker compose -f projects/$*/docker-compose.snippet.yml down -v

test-%:
	bash projects/$*/tests/test_smoke.sh

doc-%:
	code projects/$*/docs/rendu.md
```

### Exemples :

```bash
make up-1-dockerwarts
make test-15-hedwige
make doc-4-protego-maxima
```

---

## 💡 Recommandation finale

* Chaque défi doit être **indépendant** mais **suivre la même charte**.
* Tous les `README.md` doivent être clairs, lisibles et testables sans toi.
* Les **prompts IA** sont obligatoires pour prouver ton usage intelligent des outils.
* À la fin, ton dossier `/services/` deviendra une bibliothèque de mini-projets réutilisables.

---

> 🧙‍♂️ *“Le code, la doc et les tests sont les trois Reliques de la DevMagie.
> Celui qui les réunit devient invincible face au jury.”*
