# 🧙 DOCKERWARTS - Infrastructure Big Data Dockerisée

> Infrastructure complète pour le support de projets Big Data, containerisée avec Docker

[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![Compose](https://img.shields.io/badge/Docker%20Compose-3.8-blue.svg)](https://docs.docker.com/compose/)
[![HA](https://img.shields.io/badge/High%20Availability-Yes-green.svg)](https://en.wikipedia.org/wiki/High_availability)

---

## 📋 Table des matières

- [Vue d'ensemble](#-vue-densemble)
- [Architecture](#-architecture)
- [Composants](#-composants)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Configuration](#-configuration)
- [Haute disponibilité](#-haute-disponibilité)
- [Monitoring](#-monitoring)
- [Sauvegardes](#-sauvegardes)
- [Dépannage](#-dépannage)
- [Documentation technique](#-documentation-technique)

---

## 🎯 Vue d'ensemble

DOCKERWARTS est une infrastructure complète dockerisée conçue pour supporter des projets Big Data en production. Elle intègre tous les composants essentiels pour la gestion de tickets, l'indexation et la recherche de données, le monitoring, et le stockage de données massives.

### Caractéristiques principales

- ✅ **Déploiement simplifié** : Installation en une seule commande
- ✅ **Haute disponibilité** : Réplication et health checks sur tous les services critiques
- ✅ **Observabilité complète** : Monitoring avec Grafana + Prometheus
- ✅ **Sécurité** : Pare-feu applicatif avec Traefik
- ✅ **Scalabilité** : Architecture multi-nœuds pour Cassandra et Elasticsearch
- ✅ **Persistance** : Gestion des volumes Docker pour la sauvegarde des données

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND NETWORK                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │  Traefik │  │  Grafana │  │  Kibana  │  │   GLPI   │       │
│  │  (Proxy) │  │  (Viz)   │  │  (UI)    │  │(Tickets) │       │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘       │
│       │             │              │              │              │
└───────┼─────────────┼──────────────┼──────────────┼─────────────┘
        │             │              │              │
┌───────┼─────────────┼──────────────┼──────────────┼─────────────┐
│       │             │              │              │              │
│       │   ┌─────────┴───────┐  ┌──┴─────┐  ┌────┴─────┐        │
│       │   │   Prometheus    │  │  ES    │  │ GLPI DB  │        │
│       │   │   (Metrics)     │  │ Master │  │ (MariaDB)│        │
│       │   └─────────────────┘  └────────┘  └──────────┘        │
│       │                                                          │
│       │   ┌───────────┐  ┌───────────┐                         │
│       │   │ Cassandra │  │ Cassandra │                         │
│       │   │   Node 1  │  │   Node 2  │                         │
│       │   └───────────┘  └───────────┘                         │
│       │                                                          │
│       │   ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│       └───┤   Node   │  │ cAdvisor │  │    ES    │            │
│           │ Exporter │  │(Monitor) │  │   Data   │            │
│           └──────────┘  └──────────┘  └──────────┘            │
│                     BACKEND NETWORK                             │
└─────────────────────────────────────────────────────────────────┘

Legend:
  ━━ Frontend Network (172.20.0.0/24)
  ── Backend Network (172.21.0.0/24)
```

### Réseaux

- **Frontend Network** (`172.20.0.0/24`) : Services exposés via Traefik
- **Backend Network** (`172.21.0.0/24`) : Services internes et bases de données

---

## 🔧 Composants

### 1. Traefik (Pare-feu applicatif & Reverse Proxy)
- **Rôle** : Point d'entrée unique, routage, load balancing
- **Ports** : 80 (HTTP), 443 (HTTPS), 8080 (Dashboard)
- **HA** : Health checks, restart automatique

### 2. GLPI (Outil de ticketing)
- **Version** : Latest (via diouxx/glpi)
- **Base de données** : MariaDB 10.11
- **Accès** : http://glpi.dockerwarts.local
- **HA** : Health checks sur GLPI et MariaDB

### 3. Elasticsearch (Recherche & Indexation)
- **Version** : 8.11.0
- **Architecture** : 2 nœuds (Master + Data)
- **Accès** : Port 9200 (interne)
- **HA** : Cluster multi-nœuds avec découverte automatique

### 4. Kibana (Interface Elasticsearch)
- **Version** : 8.11.0
- **Accès** : http://kibana.dockerwarts.local
- **Features** : Visualisation, recherche, dashboards

### 5. Cassandra (Data Lake)
- **Version** : 4.1
- **Architecture** : Cluster 2 nœuds
- **Accès** : Port 9042 (CQL)
- **HA** : Réplication automatique entre nœuds

### 6. Grafana (Monitoring & Dashboards)
- **Version** : 10.2.0
- **Accès** : http://grafana.dockerwarts.local
- **Credentials** : admin / changeme_grafana_password (à changer)
- **Features** : Dashboards préconfigurés, alertes

### 7. Prometheus (Collecte de métriques)
- **Version** : 2.47.0
- **Scrape interval** : 15 secondes
- **Targets** : Tous les services + node-exporter + cAdvisor

### 8. Monitoring additionnel
- **Node Exporter** : Métriques système (CPU, RAM, disque, réseau)
- **cAdvisor** : Métriques des conteneurs Docker

---

## ⚙️ Prérequis

### Système requis

- **OS** : Linux, macOS, ou Windows avec WSL2
- **RAM** : Minimum 8 GB (16 GB recommandé)
- **Disque** : Minimum 20 GB d'espace libre
- **CPU** : 4 cores minimum

### Logiciels requis

- Docker Engine 20.10+
- Docker Compose 2.0+ (ou docker-compose 1.29+)
- Git

### Installation Docker

**Linux (Ubuntu/Debian) :**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

**macOS :**
```bash
# Installer Docker Desktop depuis https://www.docker.com/products/docker-desktop
```

**Windows (WSL2) :**
```powershell
# Installer Docker Desktop depuis https://www.docker.com/products/docker-desktop
# Activer l'intégration WSL2 dans les paramètres
```

---

## 🚀 Installation

### Installation rapide (recommandée)

```bash
# 1. Cloner le dépôt
git clone <repo-url>
cd infra

# 2. Lancer le script d'installation
make setup
```

Le script `setup.sh` effectue automatiquement :
- ✅ Vérification des prérequis
- ✅ Configuration des variables d'environnement
- ✅ Configuration système pour Elasticsearch
- ✅ Téléchargement des images Docker
- ✅ Démarrage des services
- ✅ Vérification de santé

### Installation manuelle

```bash
# 1. Copier et éditer les variables d'environnement
cp .env.example .env
nano .env  # Éditer les mots de passe

# 2. Configurer le système pour Elasticsearch (Linux seulement)
sudo sysctl -w vm.max_map_count=262144

# 3. Démarrer les services
docker-compose up -d

# 4. Vérifier le statut
docker-compose ps
```

---

## 🎮 Utilisation

### Commandes principales (Makefile)

```bash
make help        # Afficher l'aide
make start       # Démarrer tous les services
make stop        # Arrêter tous les services
make restart     # Redémarrer tous les services
make status      # Voir le statut des services
make logs        # Suivre les logs de tous les services
make health      # Vérifier la santé des services
make backup      # Créer une sauvegarde
make clean       # Nettoyer (conserver les données)
make clean-all   # Nettoyer tout (supprimer les données)
```

### Logs spécifiques

```bash
make logs-grafana      # Logs Grafana
make logs-cassandra    # Logs Cassandra
make logs-elasticsearch # Logs Elasticsearch
make logs-glpi         # Logs GLPI
```

### Accès aux services

Ajouter ces entrées dans `/etc/hosts` :

```bash
echo '127.0.0.1 grafana.dockerwarts.local glpi.dockerwarts.local kibana.dockerwarts.local' | sudo tee -a /etc/hosts
```

Puis accéder aux interfaces :

| Service | URL | Credentials |
|---------|-----|-------------|
| **Grafana** | http://grafana.dockerwarts.local | admin / (voir .env) |
| **GLPI** | http://glpi.dockerwarts.local | (première connexion) |
| **Kibana** | http://kibana.dockerwarts.local | - |
| **Traefik** | http://localhost:8080 | - |
| **Prometheus** | http://localhost:9090 | - |

---

## ⚙️ Configuration

### Variables d'environnement (.env)

```env
# GLPI
GLPI_DB_ROOT_PASSWORD=votre_mot_de_passe_fort
GLPI_DB_PASSWORD=votre_mot_de_passe_glpi

# Grafana
GRAFANA_ADMIN_PASSWORD=votre_mot_de_passe_grafana
```

⚠️ **Important** : Changez tous les mots de passe avant la mise en production !

### Configuration avancée

Voir les fichiers dans `configs/` :
- `traefik/traefik.yml` : Configuration Traefik
- `elasticsearch/elasticsearch.yml` : Configuration Elasticsearch
- `cassandra/cassandra.yaml` : Configuration Cassandra
- `grafana/prometheus.yml` : Targets Prometheus
- `grafana/provisioning/` : Datasources et dashboards Grafana

---

## 🔄 Haute disponibilité

### Mesures HA implémentées

#### 1. Health Checks
Tous les services critiques ont des health checks :
- Intervalle : 30 secondes
- Timeout : 10 secondes
- Retries : 3-5 tentatives
- Start period : adapté à chaque service

#### 2. Restart Policies
Tous les services : `restart: unless-stopped`

#### 3. Multi-nœuds
- **Elasticsearch** : 2 nœuds (master + data)
- **Cassandra** : 2 nœuds avec réplication automatique

#### 4. Dependencies
Services démarrés dans l'ordre avec `depends_on` et `condition: service_healthy`

### Tests de charge

```bash
# Test Elasticsearch
curl -X GET "localhost:9200/_cluster/health?pretty"

# Test Cassandra
docker exec dockerwarts-cassandra-node1 nodetool status

# Test Grafana/Prometheus
curl http://localhost:9090/-/healthy
```

---

## 📊 Monitoring

### Dashboards Grafana

Dashboard **Infrastructure Overview** préconfigurés :
- CPU Usage
- Memory Usage  
- Disk Usage
- Network Traffic
- Container Status
- Elasticsearch Cluster Health

### Accès monitoring

1. Ouvrir Grafana : http://grafana.dockerwarts.local
2. Login : admin / (mot de passe .env)
3. Naviguer vers **Dashboards** → **Dockerwarts**

### Métriques disponibles

- **Node Exporter** : CPU, RAM, disque, réseau
- **cAdvisor** : Métriques par conteneur
- **Prometheus** : Métriques applicatives
- **Traefik** : Métriques HTTP/HTTPS

---

## 💾 Sauvegardes

### Sauvegarde automatique

```bash
make backup
```

Crée une archive `.tar.gz` dans `backups/` contenant tous les volumes :
- Grafana data
- Prometheus data
- Cassandra data (2 nœuds)
- Elasticsearch data (2 nœuds)
- GLPI data
- GLPI database

### Restauration

```bash
make restore
# Suivre les instructions pour sélectionner le backup
```

### Sauvegarde manuelle

```bash
# Copier un volume spécifique
docker run --rm \
  -v dockerwarts_grafana-data:/data \
  -v $(pwd):/backup \
  busybox tar czf /backup/grafana-backup.tar.gz /data
```

---

## 🔧 Dépannage

### Services ne démarrent pas

```bash
# Vérifier les logs
make logs

# Vérifier l'espace disque
df -h

# Vérifier la mémoire
free -h

# Recréer les conteneurs
make clean
make start
```

### Elasticsearch ne démarre pas

```bash
# Vérifier vm.max_map_count
sysctl vm.max_map_count

# Le fixer (doit être >= 262144)
sudo sysctl -w vm.max_map_count=262144
```

### Cassandra lent au démarrage

C'est normal, Cassandra prend 2-3 minutes pour démarrer complètement.

```bash
# Vérifier le statut
docker exec dockerwarts-cassandra-node1 nodetool status
```

### Accès aux services bloqué

```bash
# Vérifier /etc/hosts
cat /etc/hosts | grep dockerwarts

# Ajouter si manquant
echo '127.0.0.1 grafana.dockerwarts.local glpi.dockerwarts.local kibana.dockerwarts.local' | sudo tee -a /etc/hosts
```

---

## 📚 Documentation technique

- [Architecture détaillée](docs/architecture.md)
- [Diagrammes réseau](docs/network.md)
- [Gestion des volumes](docs/volumes.md)
- [Stratégie de sauvegarde](docs/backup-strategy.md)
- [Guide de production](docs/production.md)
- [Sécurité](docs/security.md)

---

## 🎓 Choix technologiques

### Traefik vs Nginx
✅ **Traefik** : Configuration dynamique, intégration Docker native, dashboard

### Elasticsearch vs Solr
✅ **Elasticsearch** : Écosystème ELK, scalabilité, documentation

### Cassandra vs MongoDB
✅ **Cassandra** : Meilleure scalabilité horizontale, HA native, Big Data

### Grafana vs Kibana
✅ **Les deux** : Grafana pour métriques système, Kibana pour logs Elasticsearch

---

## 📝 Licences

- Traefik : MIT License
- Elasticsearch : Elastic License 2.0
- Cassandra : Apache License 2.0
- Grafana : AGPLv3
- GLPI : GPLv2+

---

## 👥 Contributeurs

Projet réalisé dans le cadre du Workshop Poudlard EPSI/WIS - Défi #1 DOCKERWARTS

---

## 🚀 Pour aller plus loin

### Production
- Configurer HTTPS avec Let's Encrypt
- Mettre en place une authentification centralisée
- Ajouter des alertes Grafana
- Configurer des sauvegardes distantes

### Scalabilité
- Ajouter des nœuds Cassandra supplémentaires
- Mettre en place Elasticsearch en cluster
- Load balancing avec plusieurs instances Traefik

### Sécurité
- Activer xpack.security dans Elasticsearch
- Configurer des secrets Docker
- Mettre en place un WAF
- Scanner les vulnérabilités des images

---

**Bon développement ! 🧙✨**
