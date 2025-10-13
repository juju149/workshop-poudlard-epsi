# 🏗️ Architecture DOCKERWARTS - Documentation détaillée

## Table des matières

1. [Vue d'ensemble](#vue-densemble)
2. [Architecture réseau](#architecture-réseau)
3. [Architecture des services](#architecture-des-services)
4. [Flux de données](#flux-de-données)
5. [Gestion de la persistance](#gestion-de-la-persistance)
6. [Haute disponibilité](#haute-disponibilité)

---

## Vue d'ensemble

L'infrastructure DOCKERWARTS est construite selon une architecture microservices avec isolation réseau et répartition des responsabilités.

### Principes architecturaux

1. **Séparation des préoccupations** : Frontend/Backend sur réseaux distincts
2. **Isolation** : Services groupés par fonction
3. **Scalabilité** : Architecture multi-nœuds pour services critiques
4. **Observabilité** : Monitoring à tous les niveaux
5. **Résilience** : Health checks et restart automatique

---

## Architecture réseau

### Topologie

```
Internet
   │
   ▼
┌──────────────────────────────────────────────────────────┐
│                    HOST MACHINE                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │              Docker Bridge Network                  │ │
│  │                                                      │ │
│  │  ┌────────────────────────────────────────────┐   │ │
│  │  │     FRONTEND NETWORK (172.20.0.0/24)      │   │ │
│  │  │                                             │   │ │
│  │  │  ┌─────────┐  ┌─────────┐  ┌─────────┐   │   │ │
│  │  │  │ Traefik │  │ Grafana │  │  GLPI   │   │   │ │
│  │  │  │  :80    │  │  :3000  │  │  :80    │   │   │ │
│  │  │  │  :443   │  │         │  │         │   │   │ │
│  │  │  │  :8080  │  │         │  │         │   │   │ │
│  │  │  └────┬────┘  └────┬────┘  └────┬────┘   │   │ │
│  │  │       │            │            │         │   │ │
│  │  └───────┼────────────┼────────────┼─────────┘   │ │
│  │          │            │            │              │ │
│  │  ┌───────┼────────────┼────────────┼─────────┐   │ │
│  │  │       │   BACKEND NETWORK (172.21.0.0/24) │   │ │
│  │  │       │            │            │          │   │ │
│  │  │  ┌────┴────┐  ┌───┴────┐  ┌───┴──────┐  │   │ │
│  │  │  │Promeths │  │   ES   │  │ GLPI DB  │  │   │ │
│  │  │  │  :9090  │  │  :9200 │  │  :3306   │  │   │ │
│  │  │  └─────────┘  └────────┘  └──────────┘  │   │ │
│  │  │                                          │   │ │
│  │  │  ┌───────────┐  ┌───────────┐          │   │ │
│  │  │  │ Cassandra │  │ Cassandra │          │   │ │
│  │  │  │  Node 1   │  │  Node 2   │          │   │ │
│  │  │  │  :9042    │  │  :9042    │          │   │ │
│  │  │  └───────────┘  └───────────┘          │   │ │
│  │  │                                          │   │ │
│  │  │  ┌──────────┐  ┌──────────┐           │   │ │
│  │  │  │   Node   │  │ cAdvisor │           │   │ │
│  │  │  │ Exporter │  │  :8080   │           │   │ │
│  │  │  │  :9100   │  │          │           │   │ │
│  │  │  └──────────┘  └──────────┘           │   │ │
│  │  └──────────────────────────────────────┘   │ │
│  └────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────┘
```

### Réseaux Docker

#### Frontend Network (`172.20.0.0/24`)
- **Type** : Bridge
- **Rôle** : Services exposés aux utilisateurs
- **Services** :
  - Traefik (reverse proxy)
  - Grafana (monitoring UI)
  - Kibana (logs UI)
  - GLPI (ticketing UI)

#### Backend Network (`172.21.0.0/24`)
- **Type** : Bridge
- **Rôle** : Services internes et bases de données
- **Services** :
  - Prometheus (métriques)
  - Elasticsearch (cluster)
  - Cassandra (cluster)
  - MariaDB (base GLPI)
  - Node Exporter (métriques système)
  - cAdvisor (métriques containers)

### Ports exposés sur l'hôte

| Service | Port | Protocole | Usage |
|---------|------|-----------|-------|
| Traefik | 80 | HTTP | Entrée principale |
| Traefik | 443 | HTTPS | Entrée principale (SSL) |
| Traefik | 8080 | HTTP | Dashboard Traefik |
| Elasticsearch | 9200 | HTTP | API REST (développement) |

---

## Architecture des services

### Couche Proxy & Firewall

#### Traefik
```yaml
Role: Reverse Proxy + Application Firewall
Function:
  - Routage par domaine (Host-based routing)
  - Terminaison SSL/TLS
  - Load balancing
  - Métriques pour Prometheus
Health Check: traefik healthcheck --ping
Restart: unless-stopped
```

**Justification du choix** :
- Configuration dynamique via labels Docker
- Intégration native avec Docker
- Dashboard intégré
- Support SSL automatique (Let's Encrypt)
- Métriques Prometheus natives

---

### Couche Ticketing

#### GLPI + MariaDB
```yaml
GLPI:
  Image: diouxx/glpi:latest
  Dependencies: MariaDB
  Health Check: curl -f http://localhost/
  Access: http://glpi.dockerwarts.local

MariaDB:
  Image: mariadb:10.11
  Health Check: mysqladmin ping
  Volumes: glpi-db-data (persistent)
```

**Architecture** :
- GLPI sur frontend network (accessible via Traefik)
- MariaDB sur backend network (isolée)
- Communication interne sur backend network

---

### Couche Indexation & Recherche

#### Elasticsearch (Cluster)
```yaml
Architecture: Master-Data
Nodes:
  - elasticsearch-master (coordinating + master)
  - elasticsearch-data (data node)

Configuration:
  - Cluster Name: dockerwarts-cluster
  - Discovery: seed_hosts automatique
  - Memory Lock: activé
  - Security: désactivée (interne)

Health Check: curl /_cluster/health
```

**Haute disponibilité** :
- 2 nœuds minimum pour quorum
- Réplication automatique des shards
- Discovery automatique des nœuds

#### Kibana
```yaml
Role: Interface utilisateur Elasticsearch
Connection: elasticsearch-master:9200
Access: http://kibana.dockerwarts.local
```

---

### Couche Data Lake

#### Cassandra (Cluster)
```yaml
Architecture: Multi-node cluster
Nodes:
  - cassandra-node1 (rack1)
  - cassandra-node2 (rack2)

Configuration:
  - Cluster: DockerwartsCassandraCluster
  - Seeds: cassandra-node1,cassandra-node2
  - Replication: automatique
  - Snitch: GossipingPropertyFileSnitch

Health Check: nodetool status
Start Period: 120s (démarrage long)
```

**Haute disponibilité** :
- 2 nœuds avec réplication
- Gossip protocol pour la découverte
- Rack awareness pour distribution

**Scalabilité** :
- Ajout de nœuds possible sans downtime
- Réplication factor configurable
- Partitionnement automatique

---

### Couche Monitoring

#### Prometheus
```yaml
Role: Time Series Database + Scraper
Scrape Interval: 15s
Targets:
  - prometheus (self)
  - traefik:8080
  - elasticsearch-master:9200
  - elasticsearch-data:9200
  - node-exporter:9100
  - cadvisor:8080

Storage: 30 days retention
```

#### Grafana
```yaml
Role: Visualization & Dashboards
Datasources:
  - Prometheus (default)
  - Elasticsearch

Provisioning:
  - Datasources auto-configurées
  - Dashboards pré-chargés

Access: http://grafana.dockerwarts.local
```

#### Node Exporter
```yaml
Role: Host metrics collector
Metrics:
  - CPU usage
  - Memory usage
  - Disk usage
  - Network traffic
```

#### cAdvisor
```yaml
Role: Container metrics collector
Metrics:
  - Container CPU
  - Container Memory
  - Container Network
  - Container Disk I/O
```

---

## Flux de données

### Flux utilisateur (Frontend)

```
User Request
    │
    ▼
┌─────────┐
│ Traefik │ (Port 80/443)
└────┬────┘
     │ Route by Host header
     ├─── grafana.dockerwarts.local ──▶ Grafana:3000
     ├─── kibana.dockerwarts.local  ──▶ Kibana:5601
     └─── glpi.dockerwarts.local    ──▶ GLPI:80
```

### Flux de monitoring (Backend)

```
┌──────────────┐
│  Prometheus  │ (Scrape every 15s)
└──────┬───────┘
       │
       ├──▶ Traefik:8080/metrics
       ├──▶ Elasticsearch:9200/_prometheus/metrics
       ├──▶ Node Exporter:9100/metrics
       └──▶ cAdvisor:8080/metrics
       
       │ Store in TSDB
       ▼
┌─────────────┐
│  Grafana    │ Query Prometheus
└─────────────┘
```

### Flux de données (Data)

```
Application Data
    │
    ▼
┌─────────────────┐
│  Elasticsearch  │ ◀──▶ Replication
│     Master      │      
└────────┬────────┘      ┌─────────────────┐
         │               │  Elasticsearch  │
         └──────────────▶│      Data       │
                         └─────────────────┘

Application Data
    │
    ▼
┌─────────────────┐
│   Cassandra     │ ◀──▶ Gossip Protocol
│     Node 1      │      + Data Replication
└────────┬────────┘      
         │               ┌─────────────────┐
         └──────────────▶│   Cassandra     │
                         │     Node 2      │
                         └─────────────────┘
```

---

## Gestion de la persistance

### Volumes Docker

| Volume | Service | Type | Backup |
|--------|---------|------|--------|
| `traefik-certs` | Traefik | Certificats SSL | Optionnel |
| `glpi-db-data` | MariaDB | Base de données | **Critique** |
| `glpi-data` | GLPI | Fichiers GLPI | **Critique** |
| `elasticsearch-master-data` | ES Master | Index ES | **Critique** |
| `elasticsearch-data-data` | ES Data | Index ES | **Critique** |
| `kibana-data` | Kibana | Config Kibana | Normal |
| `cassandra-node1-data` | Cassandra 1 | Données | **Critique** |
| `cassandra-node2-data` | Cassandra 2 | Données | **Critique** |
| `grafana-data` | Grafana | Dashboards | Normal |
| `prometheus-data` | Prometheus | Métriques (30j) | Normal |

### Stratégie de sauvegarde

#### Volumes critiques (daily backup)
- GLPI database + data
- Cassandra nodes
- Elasticsearch nodes

#### Volumes normaux (weekly backup)
- Grafana dashboards
- Prometheus data (optionnel, métriques temporaires)

#### Méthode
```bash
# Automatique via Makefile
make backup

# Génère: backups/dockerwarts_YYYYMMDD_HHMMSS.tar.gz
```

---

## Haute disponibilité

### Stratégies HA par service

#### 1. Health Checks
Tous les services critiques :
```yaml
healthcheck:
  test: [CMD, ...]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: XYs
```

#### 2. Restart Policies
```yaml
restart: unless-stopped
```

#### 3. Dependencies avec conditions
```yaml
depends_on:
  service-name:
    condition: service_healthy
```

#### 4. Multi-nœuds
- **Elasticsearch** : 2+ nœuds
- **Cassandra** : 2+ nœuds

### Indicateurs de disponibilité

| Service | SLA Target | HA Mechanism |
|---------|------------|--------------|
| Traefik | 99.9% | Health check + restart |
| Elasticsearch | 99.5% | Cluster 2 nœuds |
| Cassandra | 99.5% | Cluster 2 nœuds |
| Grafana | 99% | Health check + restart |
| GLPI | 99% | Health check + restart + DB réplication possible |

### Points de défaillance uniques (SPOF)

⚠️ **Identifiés** :
- MariaDB (GLPI) : 1 seul nœud
- Prometheus : 1 seule instance

**Mitigation** :
- Sauvegardes automatiques
- Restart automatique
- Monitoring actif

**Pour production** :
- Ajouter réplication MariaDB (Master-Slave)
- Ajouter Thanos pour Prometheus HA

---

## Évolution et scalabilité

### Ajout de nœuds Cassandra

```bash
# Modifier docker-compose.yml
# Ajouter cassandra-node3:
docker-compose up -d cassandra-node3

# Le nœud rejoint automatiquement le cluster
```

### Ajout de nœuds Elasticsearch

```bash
# Ajouter elasticsearch-data-2 dans docker-compose.yml
docker-compose up -d elasticsearch-data-2
```

### Load Balancing Traefik

Pour production :
- Plusieurs instances Traefik derrière un LB (HAProxy, NGINX)
- DNS round-robin
- Keepalived pour IP virtuelle

---

## Sécurité

### Implémenté

1. **Isolation réseau** : Frontend/Backend séparés
2. **Firewall applicatif** : Traefik avec rate limiting possible
3. **Secrets** : Variables d'environnement (.env)
4. **Health monitoring** : Détection rapide des problèmes

### Recommandations production

1. **SSL/TLS** : Activer Let's Encrypt dans Traefik
2. **Authentification** : 
   - Activer xpack.security dans Elasticsearch
   - OAuth2 pour Grafana
   - LDAP pour GLPI
3. **Secrets management** : Docker Secrets ou Vault
4. **Network policies** : Kubernetes Network Policies
5. **Scanning** : Trivy pour scanner les images

---

## Conclusion

L'architecture DOCKERWARTS offre :

✅ **Robustesse** : HA sur services critiques
✅ **Scalabilité** : Architecture multi-nœuds
✅ **Observabilité** : Monitoring complet
✅ **Sécurité** : Isolation réseau + firewall applicatif
✅ **Maintenabilité** : Configuration claire et documentée

**Prêt pour la production avec quelques ajustements de sécurité.**
