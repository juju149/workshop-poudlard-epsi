# 🧙‍♂️ POUDLARD À L'EPSI/WIS - Workshop 2025

> *"Le bonheur peut être trouvé même dans les moments les plus sombres, si l'on se souvient d'allumer la lumière."* — Albus Dumbledore

[![Workshop](https://img.shields.io/badge/Workshop-EPSI%2FWIS-purple.svg)](https://www.epsi.fr/)
[![Date](https://img.shields.io/badge/Date-13--17%20Oct%202025-blue.svg)]()
[![Niveau](https://img.shields.io/badge/Niveau-5ème%20année-green.svg)]()
[![Projects](https://img.shields.io/badge/Projets-23%20défis-orange.svg)]()

---

## 📖 Table des matières

- [🎯 Présentation Générale](#-présentation-générale)
- [🏗️ Architecture du Workshop](#️-architecture-du-workshop)
- [📋 Liste des Défis](#-liste-des-défis)
- [🚀 Quick Start](#-quick-start)
- [📊 Statut des Projets](#-statut-des-projets)
- [🤖 Agents & Méthodologie](#-agents--méthodologie)
- [📚 Documentation](#-documentation)
- [🛠️ Technologies Utilisées](#️-technologies-utilisées)
- [👥 Contribution](#-contribution)

---

## 🎯 Présentation Générale

**POUDLARD À L'EPSI/WIS** est un workshop intensif de 5 jours (13-17 octobre 2025) destiné aux étudiants de 5ème année. Il combine **23 défis techniques** inspirés de l'univers Harry Potter, couvrant tous les aspects de l'ingénierie informatique moderne :

- 🐳 **DevOps & Infrastructure** (Docker, Kubernetes, CI/CD)
- 🔒 **Cybersécurité** (Pentesting, défense, forensics)
- 🎨 **Design & Frontend** (UI/UX, animations, 3D)
- 🤖 **Intelligence Artificielle** (Deep Learning, NLP, Computer Vision)
- 📊 **Data Science** (Big Data, visualisation, analyse)
- 📱 **Développement Mobile** (Android, iOS, cross-platform)
- ☁️ **Cloud & Haute Disponibilité** (PRA, monitoring, scalabilité)

### Objectifs Pédagogiques

✅ **Maîtriser les technologies modernes** en conditions réelles  
✅ **Travailler en équipe** sur des projets pluridisciplinaires  
✅ **Produire du code de qualité professionnelle** (tests, docs, CI/CD)  
✅ **Développer la créativité** avec des contraintes techniques  
✅ **Apprendre l'automatisation** et les bonnes pratiques DevOps

---

## 🏗️ Architecture du Workshop

```
workshop-poudlard-epsi/
│
├── 📁 projects/                    # Les 23 défis du workshop
│   ├── 01-dockerwarts/            # Infrastructure Big Data dockerisée
│   ├── 02-pracadabra/             # Plan de Reprise d'Activité
│   ├── 03-cape-invisibilite/      # Pentesting éthique
│   ├── 04-protego-maxima/         # Défense & sécurité
│   ├── 05-voie-9¾/                # Pipeline CI/CD
│   ├── 08-chambre-des-secrets/    # Plan 3D animé (ML Plan2Blend)
│   ├── 13-cours-mcgonagall/       # Scraper emploi du temps
│   ├── 14-boite-magique/          # Outil cross-platform (CMake)
│   ├── 15-hedwige/                # Web app mail + OAuth2
│   ├── 16-wizard-quiz-app/        # App mobile QCM
│   ├── 17-tableau-scores-poudlard/ # App mobile native scores
│   ├── 18-LLM/                    # Déploiement LLM local
│   ├── 19-professeur-dumbledore/  # Reconnaissance vocale NLP
│   ├── 20-is-it-you-harry/        # CNN reconnaissance personnages
│   ├── 21-nimbus-3000/            # Benchmark optimizers ML
│   ├── 22-proces-jk-rowling/      # Data viz & analyse corpus
│   └── 23-easter-eggs/            # Créativité & magie noire
│
├── 📁 agents/                      # Méthodologie & standards
│   ├── AGENTS.md                  # Protocole standard de production
│   ├── roles/                     # Rôles des agents (AI copilots)
│   └── templates/                 # Templates de documentation
│
├── 📁 context/                     # Ressources partagées
│   ├── defis.md                   # Liste complète des défis
│   ├── defis.csv                  # Données des défis
│   ├── books/                     # Livres Harry Potter (corpus)
│   ├── plans/                     # Plans architecturaux
│   └── assets/                    # Assets partagés
│
├── 📄 README.md                    # Ce fichier
└── 📄 extract_thalie_plan_to_json.py # Outil extraction plans
```

---

## 📋 Liste des Défis

### 🐳 **Infrastructure & DevOps**

| # | Défi | Description | Technologies |
|---|------|-------------|--------------|
| **01** | [**DOCKERWARTS**](projects/01-dockerwarts/) | Infrastructure Big Data dockerisée complète | Docker, Cassandra, Elasticsearch, Grafana, GLPI |
| **02** | **PRACADABRA** | Plan de Reprise d'Activité automatisé | Ansible, Terraform, Backup automation |
| **05** | **CI/CD EXPRESS — VOIE 9¾** | Pipeline CI/CD complet | GitHub Actions, SonarQube, Tests |

### 🔒 **Cybersécurité**

| # | Défi | Description | Technologies |
|---|------|-------------|--------------|
| **03** | **CAPE D'INVISIBILITÉ** | Intrusion éthique & pentesting | Kali Linux, Metasploit, Nmap |
| **04** | **PROTEGO MAXIMA** | Défense active contre intrusions | IDS/IPS, WAF, Honeypot |

### 🎨 **Design & Multimédia**

| # | Défi | Description | Technologies |
|---|------|-------------|--------------|
| **06** | **SPOOKEPSI** | Maquette site vitrine Poudlard | Figma, UI/UX, Responsive design |
| **07** | **HARRY POTTER 9?** | Vidéo CGI (30s-3min) | Blender, After Effects |
| **08** | [**CHAMBRE DES SECRETS**](projects/8-chambre-des-secrets/) | Plan 3D animé (ML Plan2Blend) | Python, ML, Blender, 3D |
| **09** | **PATRONUS D'EPSI** | Animation 2D de chargement | Animation 2D, Lottie |

### 📱 **Développement Mobile & Web**

| # | Défi | Description | Technologies |
|---|------|-------------|--------------|
| **13** | [**COURS DE MCGONAGALL**](projects/13-cours-mcgonagall/) | Scraper emploi du temps (exécutable Windows) | Electron, Node.js, Scraping |
| **14** | [**BOITE MAGIQUE**](projects/14-boite-magique/) | Outil cross-platform avec CMake | C++, CMake, Qt |
| **15** | [**HEDWIGE**](projects/15-hedwige/) | Web app mail + OAuth2 | React, Node.js, Gmail API |
| **16** | [**WIZARD QUIZ APP**](projects/16-wizard-quiz-app/) | App mobile QCM (20 questions) | React Native, Expo |
| **17** | [**TABLEAU DES SCORES**](projects/17-tableau-scores-poudlard/) | App native scores des écoles | Kotlin/Swift, API REST |

### 🤖 **Intelligence Artificielle & Machine Learning**

| # | Défi | Description | Technologies |
|---|------|-------------|--------------|
| **18** | [**LE CADET DE VOTRE ÉCOLE**](projects/18-LLM/) | Déploiement LLM local | TinyLlama, Transformers |
| **19** | [**PROFESSEUR DUMBLEDORE**](projects/19-professeur-dumbledore/) | Reconnaissance vocale (8 formules) | spaCy, NLP, Speech Recognition |
| **20** | [**IS IT YOU HARRY?**](projects/20-is-it-you-harry/) | CNN reconnaissance 10 personnages | TensorFlow, Keras, CNN |
| **21** | [**NIMBUS 3000**](projects/21-nimbus-3000/) | Benchmark optimizers ML | PyTorch, scikit-learn |
| **22** | [**PROCÈS DE J.K. ROWLING**](projects/22-proces-jk-rowling/) | Analyse statistique corpus HP | NLP, spaCy, Matplotlib, Plotly |

### 🎯 **Business & Management**

| # | Défi | Description | Technologies |
|---|------|-------------|--------------|
| **10** | [**OCULUS REPARO**](projects/10-oculus-reparo/) | Cahier des charges transformation digitale | Analyse fonctionnelle |
| **11** | **COURS DE FILIUS FLITWICK** | Accompagnement au changement | ADKAR, Kubler-Ross |
| **12** | **HARRY POTTER STARTER PACK** | Starter pack étudiant | Créativité |

### 🔮 **Easter Eggs & Chaos**

| # | Défi | Description | Technologies |
|---|------|-------------|--------------|
| **23** | [**EASTER EGGS**](projects/23-easter-eggs/) | Magie noire & créativité | Reverse engineering, Chaos |

---

## 🚀 Quick Start

### Prérequis Globaux

```bash
# Outils essentiels
- Docker Desktop 20.10+
- Docker Compose 3.8+
- Git 2.30+
- Python 3.10+
- Node.js 18+
- Make (optionnel)
```

### Installation Rapide

```bash
# 1. Cloner le repository
git clone https://github.com/juju149/workshop-poudlard-epsi.git
cd workshop-poudlard-epsi

# 2. Créer le réseau Docker partagé
docker network create poudlard-network

# 3. Lancer un projet spécifique (exemple: DOCKERWARTS)
cd projects/01-dockerwarts
docker compose up -d

# 4. Vérifier le status
docker compose ps
```

### Lancer Plusieurs Projets

```bash
# Script global pour lancer tous les services
cd workshop-poudlard-epsi

# Lancer l'infrastructure de base
cd projects/01-dockerwarts
docker compose up -d

# Lancer un projet ML
cd ../20-is-it-you-harry
docker compose -f docker-compose.snippet.yml up -d

# Lancer l'analyse de données
cd ../22-proces-jk-rowling
docker compose -f docker-compose.snippet.yml up -d
```

---

## 📊 Statut des Projets

| Projet | Statut | Tests | Docker | Documentation |
|--------|--------|-------|--------|---------------|
| 01 - DOCKERWARTS | ✅ Complet | ✅ | ✅ | ✅ 495 lignes |
| 08 - Chambre des Secrets | ✅ Production | ✅ 23 tests | ✅ | ✅ 2303 lignes |
| 13 - Cours McGonagall | ✅ Complet | ✅ Jest | ✅ | ✅ |
| 14 - Boite Magique | ✅ Complet | ✅ | ✅ | ✅ |
| 15 - Hedwige | ✅ Complet | ✅ | ✅ | ✅ 238 lignes |
| 16 - Wizard Quiz | ✅ Complet | ✅ | ✅ | ✅ |
| 17 - Tableau Scores | ✅ Complet | ✅ | ✅ | ✅ |
| 18 - LLM | ✅ Complet | ✅ | ✅ | ✅ |
| 19 - Dumbledore | ✅ Complet | ✅ | ✅ | ✅ |
| 20 - Is It You Harry? | ✅ Complet | ✅ | ✅ | ✅ 263 lignes |
| 21 - Nimbus 3000 | ✅ Complet | ✅ | ✅ | ✅ |
| 22 - Procès JKR | ✅ Complet | ✅ | ✅ | ✅ 195 lignes |

**Légende:**
- ✅ Complet et fonctionnel
- 🔄 En cours de développement
- ⏳ Planifié
- ❌ Non démarré

---

## 🤖 Agents & Méthodologie

Le workshop utilise une **méthodologie standardisée** avec des agents IA spécialisés pour garantir la qualité et la cohérence des projets.

### 📘 [Guide des Agents](agents/AGENTS.md)

**Principes clés:**
- ✅ **Autonomie** : Chaque projet est dockerisable et testable
- ✅ **Documentation** : README + rendu + prompts utilisés
- ✅ **Tests** : Scripts de vérification automatique
- ✅ **Reproductibilité** : `.env` + commandes simples
- ✅ **Traçabilité** : Sources + logs d'exécution

### Rôles des Agents Spécialisés

| Agent | Rôle | Responsabilités |
|-------|------|-----------------|
| [**Project Lead**](agents/roles/project_lead.md) | Chef de projet | Vision globale, planification |
| [**Scrum Master**](agents/roles/scrum_master_copilot.md) | Méthodologie | Suivi, rituels agile |
| [**Frontend Copilot**](agents/roles/frontend_copilot.md) | Interface | UI/UX, React, mobile |
| [**Data Copilot**](agents/roles/data_copilot.md) | Data Science | ML, analyse, visualisation |
| [**Infra Copilot**](agents/roles/infra_copilot.md) | Infrastructure | Docker, K8s, cloud |
| [**Security Copilot**](agents/roles/security_copilot.md) | Sécurité | Pentest, défense, audit |
| [**CI/CD Copilot**](agents/roles/cicd_copilot.md) | Intégration | Pipelines, tests, qualité |
| [**Documentation Copilot**](agents/roles/documentation_copilot.md) | Docs | README, guides, API docs |

---

## 📚 Documentation

### Documentation par Projet

Chaque projet dispose de sa propre documentation complète :

```
projects/[numero]-[nom]/
├── README.md                  # Vue d'ensemble & quick start
├── QUICKSTART.md             # Guide de démarrage rapide
├── docs/
│   ├── rendu.md              # Rapport méthodologique
│   ├── prompts_used.md       # Prompts IA utilisés
│   └── architecture.md       # Architecture technique
└── tests/
    ├── test_smoke.sh         # Tests de validation
    └── test_integration.sh   # Tests d'intégration
```

### Guides Globaux

- 📖 [**Liste des Défis**](context/defis.md) - Cahier des charges complet
- 🤖 [**Guide des Agents**](agents/AGENTS.md) - Méthodologie standard
- 📝 [**Template README**](agents/templates/README_TEMPLATE.md) - Template standard

---

## 🛠️ Technologies Utilisées

### Infrastructure & DevOps
- 🐳 **Docker** & Docker Compose
- ☸️ **Kubernetes** (optionnel)
- 📊 **Grafana** + Prometheus
- 🔍 **Elasticsearch** + Kibana
- 💾 **Cassandra**, PostgreSQL, MongoDB

### Frontend & Mobile
- ⚛️ **React** + Vite
- 📱 **React Native** + Expo
- 🎨 **Tailwind CSS**
- 🔧 **Electron**
- 📐 **Figma**

### Backend & API
- 🟢 **Node.js** + Express
- 🐍 **Python** + FastAPI
- 🔐 **OAuth2** + JWT
- 📧 **Gmail API**

### Intelligence Artificielle
- 🧠 **TensorFlow** + Keras
- 🔥 **PyTorch**
- 🗣️ **spaCy** (NLP)
- 🤖 **Transformers** (Hugging Face)
- 📊 **scikit-learn**

### Data Science & Visualisation
- 📊 **Matplotlib** + Seaborn
- 📈 **Plotly** (interactif)
- 🐼 **Pandas** + NumPy
- 🔬 **Jupyter** Notebooks

### CI/CD & Qualité
- ✅ **GitHub Actions**
- 🔍 **SonarQube**
- 🧪 **Jest**, PyTest, JUnit
- 📋 **ESLint**, Black, Prettier

### Sécurité
- 🔒 **Kali Linux**
- 🛡️ **Snort** (IDS/IPS)
- 🕸️ **Traefik** (reverse proxy)
- 🔐 **Let's Encrypt**

---

## 👥 Contribution

### Workflow Standard

```bash
# 1. Créer une branche pour votre défi
git checkout -b defi/[numero]-[nom]

# 2. Suivre la structure standard
mkdir -p projects/[numero]-[nom]/{src,docs,tests}

# 3. Utiliser le template README
cp agents/templates/README_TEMPLATE.md projects/[numero]-[nom]/README.md

# 4. Développer avec tests
# ... votre code ...

# 5. Documenter les prompts utilisés
echo "# Prompts utilisés" > docs/prompts_used.md

# 6. Valider avec les tests
./tests/test_smoke.sh

# 7. Commit et push
git add .
git commit -m "feat: [numero]-[nom] - description"
git push origin defi/[numero]-[nom]
```

### Standards de Qualité

✅ **Code:**
- Tests unitaires (coverage > 80%)
- Linting (ESLint, Black, etc.)
- Types stricts (TypeScript, mypy)

✅ **Documentation:**
- README complet avec exemples
- Commentaires dans le code
- Architecture documentée

✅ **Docker:**
- Dockerfile optimisé (multi-stage)
- docker-compose.yml fonctionnel
- Variables d'environnement (.env.example)

✅ **Git:**
- Commits conventionnels (feat, fix, docs, etc.)
- Branches par fonctionnalité
- Pull requests avec description

---

## 📊 Statistiques du Workshop

```
📦 23 défis techniques
🐳 15+ services dockerisés
📝 5000+ lignes de documentation
✅ 100+ tests automatisés
🤖 8 agents IA spécialisés
👥 Nombreux étudiants participants
⏱️ 5 jours intensifs
```

---

## 🏆 Critères d'Évaluation

### Critères Transverses

| Critère | Poids | Description |
|---------|-------|-------------|
| **Pertinence Technique** | 30% | Choix technologiques adaptés |
| **Qualité du Code** | 25% | Tests, linting, architecture |
| **Documentation** | 20% | Clarté, complétude, exemples |
| **Reproductibilité** | 15% | Facilité de déploiement |
| **Créativité** | 10% | Originalité des solutions |

### Livrables Minimaux

✅ README détaillé  
✅ Diagrammes d'architecture  
✅ Scripts d'installation/déploiement  
✅ Tests unitaires + rapport coverage (si exigé)  
✅ Documentation utilisateur & développeur  
✅ Fichiers sources et exports

---

## 📞 Support & Ressources

### Liens Utiles

- 📧 **Support:** workshop-poudlard@epsi.fr
- 📚 **Documentation:** [agents/AGENTS.md](agents/AGENTS.md)
- 🐛 **Issues:** GitHub Issues
- 💬 **Discord:** Serveur workshop EPSI

### Ressources Externes

- [Docker Documentation](https://docs.docker.com/)
- [TensorFlow Tutorials](https://www.tensorflow.org/tutorials)
- [React Documentation](https://react.dev/)
- [Python Best Practices](https://docs.python-guide.org/)

---

## 📜 Licence

Ce projet est à usage pédagogique dans le cadre du workshop EPSI/WIS 2025.

**Crédits:**
- Univers Harry Potter © J.K. Rowling / Warner Bros
- Framework pédagogique © EPSI/WIS 2025
- Code & Documentation © Étudiants contributeurs

---

## 🌟 Projets Phares

### 🏗️ [ML Plan2Blend - Chambre des Secrets](projects/8-chambre-des-secrets/)

**Conversion automatique de plans 2D en modèles 3D**

- ✅ **2,654 lignes** de Python
- ✅ **23 tests** unitaires (100% passing)
- ✅ **Production ready** avec Docker
- 🧠 ML-based wall segmentation
- 🎨 Génération Blender automatique

### 🤖 [Is It You Harry? - CNN Recognition](projects/20-is-it-you-harry/)

**Reconnaissance de 10 personnages par deep learning**

- ✅ CNN avec TensorFlow/Keras
- ✅ Dataset custom annoté
- ✅ Métriques détaillées (accuracy, confusion matrix)
- 📊 Visualisations interactives

### ⚖️ [Procès de J.K. Rowling - NLP Analysis](projects/22-proces-jk-rowling/)

**Analyse statistique du corpus Harry Potter**

- ✅ Pipeline NLP avec spaCy
- ✅ 5 notebooks Jupyter
- ✅ Visualisations avancées (Plotly)
- 📄 Rapport HTML/PDF automatique

---

<div align="center">

**🧙‍♂️ Que la magie du code soit avec vous ! ✨**

*"Ce sont nos choix, Harry, qui montrent ce que nous sommes vraiment, bien plus que nos capacités."*
— Albus Dumbledore

---

**[⬆ Retour en haut](#-poudlard-à-lepsiwis---workshop-2025)**

</div>
[To be defined by project maintainers]

## Contact

For questions about ML Plan2Blend, see the [project documentation](ml-plan2blend/README.md).
